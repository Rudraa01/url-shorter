from flask import Flask, request, redirect, render_template, jsonify, url_for
import string
import random
from urllib.parse import urlparse
import json
import os

app = Flask(__name__)
app.template_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

# Use in-memory storage for Vercel deployment
url_storage = {}

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
def index():
    """Main page with URL shortening form"""
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
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
def redirect_url(short_code):
    """Redirect to the original URL and increment click count"""
    if short_code in url_storage:
        url_data = url_storage[short_code]
        url_data['click_count'] += 1
        return redirect(url_data['original_url'])
    return render_template('404.html'), 404

@app.route('/stats/<short_code>')
def get_stats(short_code):
    """Get statistics for a shortened URL"""
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

@app.route('/api/stats')
def get_all_stats():
    """Get statistics for all URLs (admin endpoint)"""
    return jsonify([{
        'original_url': data['original_url'],
        'short_code': code,
        'created_at': data.get('created_at', ''),
        'click_count': data['click_count'],
        'short_url': f"{request.host_url.rstrip('/')}/{code}"
    } for code, data in url_storage.items()])
