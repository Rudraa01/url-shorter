import os
import sqlite3
import string
import random
from flask import Flask, request, redirect, render_template, jsonify, url_for
from urllib.parse import urlparse

app = Flask(__name__, template_folder='../templates')

# Database setup
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'urls.db')

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the URLs table"""
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)
    conn = sqlite3.connect(DATABASE)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            click_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def generate_short_code(length=6):
    """Generate a random short code for URLs"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

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
    conn = get_db_connection()
    
    existing = conn.execute('SELECT short_code FROM urls WHERE original_url = ?', 
                           (original_url,)).fetchone()
    
    if existing:
        short_code = existing['short_code']
    else:
        while True:
            short_code = generate_short_code()
            existing_code = conn.execute('SELECT id FROM urls WHERE short_code = ?', 
                                       (short_code,)).fetchone()
            if not existing_code:
                break
        
        conn.execute('INSERT INTO urls (original_url, short_code) VALUES (?, ?)',
                    (original_url, short_code))
        conn.commit()
    
    conn.close()
    
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
    conn = get_db_connection()
    
    url_data = conn.execute('SELECT original_url FROM urls WHERE short_code = ?', 
                           (short_code,)).fetchone()
    
    if url_data:
        conn.execute('UPDATE urls SET click_count = click_count + 1 WHERE short_code = ?',
                    (short_code,))
        conn.commit()
        conn.close()
        return redirect(url_data['original_url'])
    else:
        conn.close()
        return render_template('404.html'), 404

@app.route('/stats/<short_code>')
def get_stats(short_code):
    """Get statistics for a shortened URL"""
    conn = get_db_connection()
    
    url_data = conn.execute('''
        SELECT original_url, short_code, created_at, click_count 
        FROM urls WHERE short_code = ?
    ''', (short_code,)).fetchone()
    
    conn.close()
    
    if url_data:
        return jsonify({
            'original_url': url_data['original_url'],
            'short_code': url_data['short_code'],
            'created_at': url_data['created_at'],
            'click_count': url_data['click_count'],
            'short_url': f"{request.host_url.rstrip('/')}/{short_code}"
        })
    else:
        return jsonify({'error': 'Short URL not found'}), 404

@app.route('/api/stats')
def get_all_stats():
    """Get statistics for all URLs (admin endpoint)"""
    conn = get_db_connection()
    
    urls = conn.execute('''
        SELECT original_url, short_code, created_at, click_count 
        FROM urls 
        ORDER BY created_at DESC
    ''').fetchall()
    
    conn.close()
    
    return jsonify([{
        'original_url': url['original_url'],
        'short_code': url['short_code'],
        'created_at': url['created_at'],
        'click_count': url['click_count'],
        'short_url': f"{request.host_url.rstrip('/')}/{url['short_code']}"
    } for url in urls])

# Initialize database
init_db()
