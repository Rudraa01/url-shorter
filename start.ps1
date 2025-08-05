# PowerShell script to start the URL Shortener development server

Write-Host "🚀 Starting URL Shortener Development Server..." -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "❌ app.py not found. Please run this script from the project directory." -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
$venvPath = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $venvPath)) {
    Write-Host "❌ Virtual environment not found." -ForegroundColor Red
    Write-Host "📦 Please run setup first:" -ForegroundColor Yellow
    Write-Host "   python -m venv .venv" -ForegroundColor Cyan
    Write-Host "   .\.venv\Scripts\activate" -ForegroundColor Cyan
    Write-Host "   pip install -r requirements.txt" -ForegroundColor Cyan
    exit 1
}

Write-Host "✅ Virtual environment found" -ForegroundColor Green
Write-Host "🔄 Starting Flask development server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "🌐 Your URL shortener will be available at:" -ForegroundColor Cyan
Write-Host "   http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "⏹️  Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Start the Flask application
& $venvPath app.py
