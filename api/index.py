from flask import Flask, request, redirect, render_template, jsonify, url_for, send_from_directory
import string
import random
from urllib.parse import urlparse
import json
import os
from functools import wraps

app = Flask(__name__, template_folder='templates')

# Configure template folder based on environment
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app.template_folder = template_dir

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use in-memory storage for Vercel deployment
url_storage = {}

def handle_errors(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            app.logger.error(f"Error: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    return decorated_function

def generate_short_code(length=6):
    """Generate a random short code for URLs"""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        if code not in url_storage:
            return code

def is_valid_url(url):
    """Validate if the provided URL is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and '.' in result.netloc
    except:
        return False

@app.route('/')
@handle_errors
def index():
    """Main page with URL shortening form"""
    try:
        return render_template('index.html')
    except Exception as e:
        app.logger.error(f"Template error: {str(e)}")
        return jsonify({'error': 'Template not found'}), 500

@app.route('/shorten', methods=['POST'])
@handle_errors
def shorten_url():
    """API endpoint to shorten a URL"""
    data = request.get_json() if request.is_json else request.form
    original_url = data.get('url', '').strip()
    
    if not original_url:
        return jsonify({'error': 'URL is required'}), 400
    
    temp_url = original_url
    if not temp_url.startswith(('http://', 'https://')):
        temp_url = 'https://' + temp_url
    
    if not is_valid_url(temp_url):
        return jsonify({'error': 'Invalid URL format'}), 400
    
    original_url = temp_url
    
    # Check if URL already exists
    for code, url_data in url_storage.items():
        if url_data['original_url'] == original_url:
            return jsonify({
                'original_url': original_url,
                'short_url': f"{request.host_url.rstrip('/')}/{code}",
                'short_code': code
            })
    
    # Generate new short code
    short_code = generate_short_code()
    url_storage[short_code] = {
        'original_url': original_url,
        'created_at': '',  # Could add timestamp if needed
        'click_count': 0
    }
    
    base_url = request.host_url.rstrip('/')
    short_url = f"{base_url}/{short_code}"
    
    return jsonify({
        'original_url': original_url,
        'short_url': short_url,
        'short_code': short_code
    })

@app.route('/<short_code>')
@handle_errors
def redirect_url(short_code):
    """Redirect to the original URL and increment click count"""
    try:
        if short_code in url_storage:
            url_data = url_storage[short_code]
            url_data['click_count'] += 1
            return redirect(url_data['original_url'])
        return render_template('404.html'), 404
    except Exception as e:
        app.logger.error(f"Redirect error: {str(e)}")
        return jsonify({'error': 'Redirect failed'}), 500

@app.route('/stats/<short_code>')
@handle_errors
def get_stats(short_code):
    """Get statistics for a shortened URL"""
    try:
        if short_code in url_storage:
            url_data = url_storage[short_code]
            return jsonify({
                'original_url': url_data['original_url'],
                'short_code': short_code,
                'created_at': url_data.get('created_at', ''),
                'click_count': url_data['click_count'],
                'short_url': f"{request.host_url.rstrip('/')}/{short_code}"
            })
        return jsonify({'error': 'Short URL not found'}), 404
    except Exception as e:
        app.logger.error(f"Stats error: {str(e)}")
        return jsonify({'error': 'Could not retrieve stats'}), 500

@app.route('/api/stats')
@handle_errors
def get_all_stats():
    """Get statistics for all URLs (admin endpoint)"""
    return jsonify([{
        'original_url': data['original_url'],
        'short_code': code,
        'created_at': data.get('created_at', ''),
        'click_count': data['click_count'],
        'short_url': f"{request.host_url.rstrip('/')}/{code}"
    } for code, data in url_storage.items()])

# Debug endpoint to check environment
@app.route('/debug/env')
@handle_errors
def debug_env():
    """Debug endpoint to check environment variables and paths"""
    if os.environ.get('VERCEL_ENV') != 'production':
        return jsonify({
            'template_folder': app.template_folder,
            'static_folder': app.static_folder,
            'env': dict(os.environ),
            'paths': {
                'current': os.getcwd(),
                'files': os.listdir('.')
            }
        })
    return jsonify({'error': 'Debug endpoint not available in production'}), 403
