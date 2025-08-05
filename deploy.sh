#!/bin/bash

# Deployment script for URL Shortener to Vercel
# Run this script to deploy your application

echo "🚀 Deploying URL Shortener to Vercel..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI is not installed."
    echo "📦 Please install it first:"
    echo "   npm install -g vercel"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ app.py not found. Please run this script from the project directory."
    exit 1
fi

echo "✅ Vercel CLI found"
echo "✅ Project files found"

# Deploy to Vercel
echo "🔄 Starting deployment..."
vercel --prod

echo "✅ Deployment complete!"
echo "🌐 Your URL shortener is now live!"
echo ""
echo "📝 Next steps:"
echo "1. Test your live application"
echo "2. Update any hardcoded URLs if needed"
echo "3. Set up a custom domain (optional)"
echo ""
echo "📊 To view deployment logs and manage your project:"
echo "   Visit: https://vercel.com/dashboard"
