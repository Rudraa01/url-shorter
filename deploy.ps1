# PowerShell deployment script for URL Shortener to Vercel

Write-Host "🚀 Deploying URL Shortener to Vercel..." -ForegroundColor Green

# Check if Vercel CLI is installed
$vercelPath = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelPath) {
    Write-Host "❌ Vercel CLI is not installed." -ForegroundColor Red
    Write-Host "📦 Please install it first:" -ForegroundColor Yellow
    Write-Host "   npm install -g vercel" -ForegroundColor Cyan
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "app.py")) {
    Write-Host "❌ app.py not found. Please run this script from the project directory." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Vercel CLI found" -ForegroundColor Green
Write-Host "✅ Project files found" -ForegroundColor Green

# Deploy to Vercel
Write-Host "🔄 Starting deployment..." -ForegroundColor Yellow
vercel --prod

Write-Host "✅ Deployment complete!" -ForegroundColor Green
Write-Host "🌐 Your URL shortener is now live!" -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Yellow
Write-Host "1. Test your live application"
Write-Host "2. Update any hardcoded URLs if needed"
Write-Host "3. Set up a custom domain (optional)"
Write-Host ""
Write-Host "📊 To view deployment logs and manage your project:" -ForegroundColor Yellow
Write-Host "   Visit: https://vercel.com/dashboard" -ForegroundColor Cyan
