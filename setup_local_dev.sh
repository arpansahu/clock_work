#!/bin/bash

# ============================================
# Clock Work - Local Development Setup Script
# ============================================

set -e  # Exit on error

echo "🚀 Starting Clock Work local development setup..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3.9 -m venv venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    if [ -f "env.example" ]; then
        echo "📝 Copying env.example to .env..."
        cp env.example .env
        echo "⚠️  Please edit .env and update the values as needed"
        echo "⚠️  Set DEBUG=1 for local development"
        echo "⚠️  Set SERVER_NAME=localhost"
    else
        echo "❌ Error: No .env file found!"
        echo "Please create .env from env.example and fill in the values"
        exit 1
    fi
else
    echo "✅ .env file already exists"
fi

# Check database configuration
echo "🗄️  Checking database configuration..."
DB_URL=$(grep DATABASE_URL .env | cut -d '=' -f2)
if [[ $DB_URL == *"sqlite"* ]]; then
    echo "✅ Using SQLite database (local development)"
elif [[ $DB_URL == *"postgresql"* ]]; then
    echo "✅ Using PostgreSQL database"
    echo "⚠️  Make sure PostgreSQL is running and accessible"
else
    echo "⚠️  Unknown database type in DATABASE_URL"
fi

# Check Redis configuration
echo "🔴 Checking Redis configuration..."
REDIS_URL=$(grep REDIS_CLOUD_URL .env | cut -d '=' -f2)
if [[ $REDIS_URL == *"localhost"* ]]; then
    echo "✅ Using local Redis"
    echo "⚠️  Make sure Redis is running: redis-server"
else
    echo "✅ Using remote Redis"
fi

# Run migrations
echo "🔄 Running database migrations..."
python manage.py migrate

# Create superuser (optional)
echo ""
read -p "📝 Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Review and update .env file with your local configuration"
echo "  2. Start Redis (if using local): redis-server"
echo "  3. Start Celery worker: celery -A clock_work worker -l info"
echo "  4. Start Celery beat: celery -A clock_work beat -l info"
echo "  5. Start Django server: python manage.py runserver 0.0.0.0:8012"
echo ""
echo "🌐 Access the application at: http://localhost:8012"
echo "👤 Admin panel: http://localhost:8012/admin"
echo ""
