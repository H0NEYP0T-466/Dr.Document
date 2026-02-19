#!/bin/bash
# Start Dr. Document Frontend

echo "🏥 Starting Dr. Document Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "ℹ️  No .env file found. Using default backend URL (http://localhost:8000)"
    echo "   Create .env from .env.example to customize"
fi

# Start the development server
echo "🚀 Starting development server on http://localhost:5173"
npm run dev
