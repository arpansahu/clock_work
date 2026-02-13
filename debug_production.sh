#!/bin/bash
# Script to debug and fix Clock Work production issues
# ⚠️  MUST BE RUN ON SERVER WITH KUBECTL ACCESS (Jenkins/K8s node)
# Usage: ./debug_production.sh [command]
# Commands: logs, migrations, showmigrations, check-env, check-users, restart

set -e

echo "========================================"
echo "Clock Work Production Debug Script"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get pod name
echo "🔍 Finding Clock Work pod..."
POD_NAME=$(kubectl get pods -l app=clock-work -o jsonpath='{.items[0].metadata.name}')

if [ -z "$POD_NAME" ]; then
    echo -e "${RED}❌ No pod found with label app=clock-work${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Found pod: $POD_NAME${NC}"
echo

# Function to run command in pod
run_in_pod() {
    kubectl exec -it $POD_NAME -- bash -c "$1"
}

# Check what user is asking to do
case "${1:-help}" in
    logs)
        echo "📋 Fetching last 100 lines of pod logs..."
        echo "========================================"
        kubectl logs $POD_NAME --tail=100
        ;;
        
    logs-full)
        echo "📋 Fetching all pod logs..."
        echo "========================================"
        kubectl logs $POD_NAME
        ;;
        
    migrations)
        echo "🔄 Running Django migrations..."
        echo "========================================"
        run_in_pod "cd /app && python manage.py migrate"
        echo -e "${GREEN}✅ Migrations completed${NC}"
        ;;
        
    showmigrations)
        echo "📋 Showing migration status..."
        echo "========================================"
        run_in_pod "cd /app && python manage.py showmigrations"
        ;;
        
    check-env)
        echo "🔍 Checking environment variables..."
        echo "========================================"
        run_in_pod "cd /app && python -c \"
from django.conf import settings
import os
print(f'DEBUG: {settings.DEBUG}')
print(f'DOMAIN: {settings.DOMAIN}')
print(f'PROTOCOL: {settings.PROTOCOL}')
print(f'ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
print(f'SECURE_PROXY_SSL_HEADER: {getattr(settings, \\\"SECURE_PROXY_SSL_HEADER\\\", \\\"Not set\\\")}')
print(f'SESSION_COOKIE_SECURE: {getattr(settings, \\\"SESSION_COOKIE_SECURE\\\", \\\"Not set\\\")}')
print(f'CSRF_COOKIE_SECURE: {getattr(settings, \\\"CSRF_COOKIE_SECURE\\\", \\\"Not set\\\")}')
\""
        ;;
        
    check-users)
        echo "👥 Checking user accounts..."
        echo "========================================"
        run_in_pod "cd /app && python manage.py shell -c \"
from account.models import Account
print(f'Total users: {Account.objects.count()}')
print(f'Active users: {Account.objects.filter(is_active=True).count()}')
print(f'Inactive users: {Account.objects.filter(is_active=False).count()}')
print('\\\\nRecent users:')
for user in Account.objects.order_by('-date_joined')[:5]:
    print(f'  - {user.email} (username: {user.username}, active: {user.is_active})')
\""
        ;;
        
    check-services)
        echo "🔍 Running service health checks..."
        echo "========================================"
        run_in_pod "cd /app && python manage.py test_all_services"
        ;;
        
    shell)
        echo "💻 Opening Django shell..."
        echo "========================================"
        kubectl exec -it $POD_NAME -- python manage.py shell
        ;;
        
    bash)
        echo "💻 Opening bash shell in pod..."
        echo "========================================"
        kubectl exec -it $POD_NAME -- bash
        ;;
        
    restart)
        echo "🔄 Restarting deployment..."
        echo "========================================"
        kubectl rollout restart deployment clock-work-app
        echo "Waiting for rollout to complete..."
        kubectl rollout status deployment clock-work-app
        echo -e "${GREEN}✅ Deployment restarted${NC}"
        ;;
        
    pod-info)
        echo "📊 Pod Information..."
        echo "========================================"
        kubectl describe pod $POD_NAME
        ;;
        
    help)
        echo "Usage: ./debug_production.sh [command]"
        echo ""
        echo "Available commands:"
        echo "  logs              - Show last 100 lines of pod logs"
        echo "  logs-full         - Show all pod logs"
        echo "  migrations        - Run Django migrations"
        echo "  showmigrations    - Show migration status"
        echo "  check-env         - Check environment variables"
        echo "  check-users       - List user accounts"
        echo "  check-services    - Run all service health checks"
        echo "  shell             - Open Django shell"
        echo "  bash              - Open bash shell in pod"
        echo "  restart           - Restart deployment"
        echo "  pod-info          - Show pod information"
        echo "  help              - Show this help message"
        ;;
        
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        echo ""
        echo "Usage: ./debug_production.sh [command]"
        echo "Run './debug_production.sh help' for available commands"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}✅ Done!${NC}"
