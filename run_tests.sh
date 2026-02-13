#!/bin/bash

# Django Test Runner Script
# This script runs tests with various options

set -e  # Exit on error

echo "🧪 Clock Work Test Runner"
echo "=============================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${2}${1}${NC}"
}

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    print_status "⚠️  Warning: Virtual environment not activated" "$YELLOW"
    echo "Activate it with: source venv/bin/activate"
    echo ""
fi

# Parse command line arguments
TEST_TYPE=${1:-all}
VERBOSITY=${2:-2}

case $TEST_TYPE in
    all)
        print_status "Running all tests..." "$GREEN"
        python manage.py test --verbosity=$VERBOSITY
        ;;
    
    quick)
        print_status "Running quick tests (fail fast)..." "$GREEN"
        python manage.py test --failfast --verbosity=$VERBOSITY
        ;;
    
    coverage)
        print_status "Running tests with coverage..." "$GREEN"
        if ! command -v pytest &> /dev/null; then
            print_status "❌ pytest not installed. Install with: pip install pytest pytest-cov" "$RED"
            exit 1
        fi
        pytest --cov=. --cov-report=html --cov-report=term-missing
        print_status "✅ Coverage report generated in htmlcov/index.html" "$GREEN"
        ;;
    
    account)
        print_status "Running account tests..." "$GREEN"
        python manage.py test account --verbosity=$VERBOSITY
        ;;
    
    tasks)
        print_status "Running tasks tests..." "$GREEN"
        python manage.py test tasks --verbosity=$VERBOSITY
        ;;
    
    clock_work)
        print_status "Running clock_work tests..." "$GREEN"
        python manage.py test clock_work --verbosity=$VERBOSITY
        ;;
    
    services)
        print_status "Running service health checks..." "$GREEN"
        python manage.py test_all_services
        ;;
    
    pytest)
        print_status "Running pytest..." "$GREEN"
        if ! command -v pytest &> /dev/null; then
            print_status "❌ pytest not installed. Install with: pip install pytest" "$RED"
            exit 1
        fi
        pytest -v
        ;;
    
    ci)
        print_status "Running CI tests (fail fast, no warnings)..." "$GREEN"
        python manage.py test --failfast --no-input --verbosity=2
        ;;
    
    *)
        print_status "❌ Unknown test type: $TEST_TYPE" "$RED"
        echo ""
        echo "Usage: ./run_tests.sh [test_type] [verbosity]"
        echo ""
        echo "Test Types:"
        echo "  all           - Run all tests (default)"
        echo "  quick         - Run tests with fail-fast"
        echo "  coverage      - Run tests with coverage report"
        echo "  account       - Run only account tests"
        echo "  tasks         - Run only tasks tests"
        echo "  clock_work    - Run only clock_work tests"
        echo "  services      - Run service health checks"
        echo "  pytest        - Run using pytest"
        echo "  ci            - Run in CI mode (fail-fast, no-input)"
        echo ""
        echo "Verbosity: 0, 1, 2, or 3 (default: 2)"
        echo ""
        echo "Examples:"
        echo "  ./run_tests.sh all 2"
        echo "  ./run_tests.sh quick"
        echo "  ./run_tests.sh coverage"
        echo "  ./run_tests.sh services"
        exit 1
        ;;
esac

print_status "✅ Tests completed!" "$GREEN"
