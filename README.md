# URL Shortener

A simple and elegant URL shortener built with Python Flask, SQLite, and deployed on Vercel Serverless Functions.

## Features

- 🔗 **URL Shortening**: Convert long URLs into short, manageable links
- 📊 **Click Tracking**: Track visit counts for each shortened URL
- 💻 **Minimal UI**: Clean and responsive web interface
- 🚀 **Serverless Deployment**: Deployed on Vercel for scalability
- 📱 **Mobile Friendly**: Responsive design that works on all devices

## Tech Stack

- **Backend**: Python 3.9 + Flask
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Deployment**: Vercel Serverless Functions

## Local Development

### Prerequisites

- Python 3.9+
- pip (Python package manager)

### Setup

1. Clone or download this repository
2. Navigate to the project directory:
   ```bash
   cd "url shorter"
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Run the application:
   ```bash
   python app.py
   ```

7. Open your browser and navigate to `http://localhost:5000`

## API Endpoints

### POST `/shorten`
Shorten a long URL.

**Request Body:**
```json
{
  "url": "https://example.com/very/long/url"
}
```

**Response:**
```json
{
  "original_url": "https://example.com/very/long/url",
  "short_url": "https://yourapp.vercel.app/abc123",
  "short_code": "abc123"
}
```

### GET `/<short_code>`
Redirect to the original URL and increment click count.

### GET `/stats/<short_code>`
Get statistics for a shortened URL.

**Response:**
```json
{
  "original_url": "https://example.com/very/long/url",
  "short_code": "abc123",
  "created_at": "2023-01-01 12:00:00",
  "click_count": 42,
  "short_url": "https://yourapp.vercel.app/abc123"
}
```

### GET `/api/stats`
Get statistics for all URLs (admin endpoint).

## Deployment on Vercel

### Prerequisites

- [Vercel CLI](https://vercel.com/download) installed
- Vercel account

### Deploy Steps

1. Install Vercel CLI globally:
   ```bash
   npm i -g vercel
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Deploy the application:
   ```bash
   vercel
   ```

4. Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? Choose your account
   - Link to existing project? **N**
   - Project name? Press Enter for default or enter a custom name
   - In which directory is your code located? **.**

5. Your app will be deployed and you'll get a live URL!

### Environment Variables

No environment variables are required for basic functionality. The app uses SQLite which creates a local database file.

## Database Schema

The application uses a simple SQLite database with one table:

```sql
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_url TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    click_count INTEGER DEFAULT 0
);
```

## Project Structure

```
url shorter/
├── api/
│   └── index.py          # Vercel serverless entry point
├── templates/
│   ├── index.html        # Main page
│   └── 404.html          # Error page
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── runtime.txt          # Python version specification
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Features in Detail

### URL Validation
- Automatically adds `https://` if no protocol is specified
- Validates URL format before processing
- Handles edge cases and malformed URLs

### Short Code Generation
- Generates random 6-character codes using letters and numbers
- Ensures uniqueness by checking against existing codes
- Case-sensitive codes for maximum combinations

### Click Tracking
- Increments counter each time a short URL is accessed
- Stores creation timestamp for analytics
- Provides statistics endpoint for detailed analytics

### Error Handling
- Graceful handling of invalid URLs
- User-friendly error messages
- 404 page for non-existent short codes

## Customization

### Changing Short Code Length
Edit the `generate_short_code()` function in `app.py`:
```python
def generate_short_code(length=6):  # Change 6 to desired length
```

### Custom Domain
Update the Vercel configuration to use your custom domain in the Vercel dashboard.

### Styling
Modify the CSS in `templates/index.html` to match your brand colors and style preferences.

## Security Considerations

- Input validation prevents malicious URLs
- No user authentication required (stateless)
- Rate limiting can be added for production use
- Consider adding HTTPS redirect for production

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

If you encounter any issues or have questions, please create an issue in the repository or contact the maintainer.
