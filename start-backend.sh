#!/bin/bash
# Start Dr. Document Backend

echo "🏥 Starting Dr. Document Backend..."

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
else
    echo "✅ Virtual environment found"
fi

# Activate virtual environment
source backend/venv/bin/activate

# Check for .env file
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your LONGCAT_API_KEY"
    exit 1
fi

# Check for API key
if ! grep -q "your_longcat_api_key_here" backend/.env; then
    echo "✅ API key configured"
else
    echo "⚠️  Please edit backend/.env and add your LONGCAT_API_KEY"
    exit 1
fi

# Create storage directory
mkdir -p backend/storage

# Start the backend server
echo "🚀 Starting FastAPI server on http://localhost:8000"
cd backend
python3 main.py
