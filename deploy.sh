#!/bin/bash

# LMS Deployment Script for Ubuntu Server
# Usage: ./deploy.sh

set -e

echo "🚀 Starting LMS deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/var/www/lms"
DOMAIN="lms-vn.com"
NGINX_SITES="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"
SERVICE_FILE="/etc/systemd/system/lms-gunicorn.service"

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Update system packages
print_status "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
print_status "Installing required packages..."
sudo apt install -y nginx python3 python3-pip python3-venv python3-dev \
    mysql-server libmysqlclient-dev build-essential pkg-config \
    certbot python3-certbot-nginx git

# Create project directory
print_status "Creating project directory..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Clone or update project
if [ -d "$PROJECT_DIR/.git" ]; then
    print_status "Updating existing project..."
    cd $PROJECT_DIR
    git pull origin main
else
    print_status "Cloning project..."
    git clone https://github.com/HuyNguyen1977/LMS.git $PROJECT_DIR
fi

# Create virtual environment
print_status "Setting up virtual environment..."
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn

# Configure MySQL
print_status "Configuring MySQL..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'lms_user'@'localhost' IDENTIFIED BY 'lms_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON lms_db.* TO 'lms_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Update Django settings
print_status "Configuring Django settings..."
cat > $PROJECT_DIR/lms_project/settings_production.py << EOF
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['$DOMAIN', 'www.$DOMAIN', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lms_db',
        'USER': 'lms_user',
        'PASSWORD': 'lms_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_ROOT = '/var/www/lms/staticfiles'
MEDIA_ROOT = '/var/www/lms/media'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
EOF

# Run Django migrations
print_status "Running Django migrations..."
export DJANGO_SETTINGS_MODULE=lms_project.settings_production
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
print_warning "Do you want to create a superuser? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    python manage.py createsuperuser
fi

# Configure Nginx
print_status "Configuring Nginx..."
sudo cp nginx-lms-production.conf $NGINX_SITES/$DOMAIN
sudo ln -sf $NGINX_SITES/$DOMAIN $NGINX_ENABLED/

# Remove default Nginx site
sudo rm -f $NGINX_ENABLED/default

# Configure Gunicorn service
print_status "Configuring Gunicorn service..."
sudo cp lms-gunicorn.service $SERVICE_FILE
sudo systemctl daemon-reload
sudo systemctl enable lms-gunicorn

# Set proper permissions
print_status "Setting permissions..."
sudo chown -R www-data:www-data $PROJECT_DIR
sudo chmod -R 755 $PROJECT_DIR

# Create log directories
sudo mkdir -p /var/log/gunicorn
sudo chown www-data:www-data /var/log/gunicorn

# Test Nginx configuration
print_status "Testing Nginx configuration..."
sudo nginx -t

# Start services
print_status "Starting services..."
sudo systemctl start lms-gunicorn
sudo systemctl restart nginx

# Setup SSL with Let's Encrypt
print_warning "Do you want to setup SSL with Let's Encrypt? (y/n)"
read -r ssl_response
if [[ "$ssl_response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    print_status "Setting up SSL certificate..."
    sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
fi

# Setup firewall
print_status "Configuring firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw --force enable

print_status "Deployment completed successfully!"
print_status "Your LMS is now available at: https://$DOMAIN"
print_status "Admin panel: https://$DOMAIN/admin/"

echo ""
print_warning "Next steps:"
echo "1. Update DNS records to point to this server"
echo "2. Configure email settings in Django"
echo "3. Set up regular backups"
echo "4. Monitor logs: sudo journalctl -u lms-gunicorn -f"
