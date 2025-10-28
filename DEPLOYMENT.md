# Hướng dẫn Deploy LMS lên Ubuntu Server với Nginx

## 📋 Yêu cầu hệ thống
- Ubuntu 20.04+ hoặc Ubuntu 22.04+
- RAM: Tối thiểu 2GB (khuyến nghị 4GB+)
- CPU: 2 cores+
- Disk: 20GB+ trống
- Domain name: lms-vn.com

## 🚀 Cài đặt nhanh

### Bước 1: Chuẩn bị server
```bash
# Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# Cài đặt các package cần thiết
sudo apt install -y nginx python3 python3-pip python3-venv python3-dev \
    mysql-server libmysqlclient-dev build-essential pkg-config \
    certbot python3-certbot-nginx git ufw
```

### Bước 2: Cấu hình MySQL
```bash
# Khởi động MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Tạo database và user
sudo mysql -e "CREATE DATABASE lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'lms_user'@'localhost' IDENTIFIED BY 'your_strong_password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON lms_db.* TO 'lms_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### Bước 3: Deploy ứng dụng
```bash
# Clone project
git clone https://github.com/HuyNguyen1977/LMS.git /var/www/lms
cd /var/www/lms

# Tạo virtual environment
python3 -m venv venv
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
pip install gunicorn

# Cấu hình Django
export DJANGO_SETTINGS_MODULE=lms_project.settings_production
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Bước 4: Cấu hình Nginx
```bash
# Copy file cấu hình
sudo cp nginx-lms-production.conf /etc/nginx/sites-available/lms-vn.com
sudo ln -s /etc/nginx/sites-available/lms-vn.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test cấu hình
sudo nginx -t
```

### Bước 5: Cấu hình Gunicorn
```bash
# Copy service file
sudo cp lms-gunicorn.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lms-gunicorn
sudo systemctl start lms-gunicorn
```

### Bước 6: Cài đặt SSL
```bash
# Cài đặt Let's Encrypt SSL
sudo certbot --nginx -d lms-vn.com -d www.lms-vn.com
```

### Bước 7: Cấu hình Firewall
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow ssh
sudo ufw enable
```

## 🔧 Cấu hình chi tiết

### File cấu hình Django Production
Tạo file `lms_project/settings_production.py`:
```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['lms-vn.com', 'www.lms-vn.com', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lms_db',
        'USER': 'lms_user',
        'PASSWORD': 'your_strong_password',
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
```

### Cấu hình Nginx
File `nginx-lms-production.conf` đã được tạo với:
- SSL/TLS configuration
- Static files serving
- Gzip compression
- Security headers
- Proxy to Gunicorn

### Cấu hình Gunicorn
File `gunicorn.conf.py` với:
- 4 worker processes
- Proper logging
- Security settings
- Performance tuning

## 📊 Monitoring và Logs

### Xem logs
```bash
# Gunicorn logs
sudo journalctl -u lms-gunicorn -f

# Nginx logs
sudo tail -f /var/log/nginx/lms-vn.com.access.log
sudo tail -f /var/log/nginx/lms-vn.com.error.log

# Gunicorn access logs
sudo tail -f /var/log/gunicorn/lms-access.log
sudo tail -f /var/log/gunicorn/lms-error.log
```

### Restart services
```bash
# Restart Gunicorn
sudo systemctl restart lms-gunicorn

# Restart Nginx
sudo systemctl restart nginx

# Reload Nginx config
sudo nginx -s reload
```

## 🔄 Backup và Maintenance

### Backup database
```bash
# Backup MySQL
mysqldump -u lms_user -p lms_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore database
mysql -u lms_user -p lms_db < backup_file.sql
```

### Backup media files
```bash
# Backup media directory
tar -czf media_backup_$(date +%Y%m%d_%H%M%S).tar.gz /var/www/lms/media/
```

### Update application
```bash
cd /var/www/lms
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
sudo systemctl restart lms-gunicorn
```

## 🛡️ Security Checklist

- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Database password strong
- [ ] Django DEBUG = False
- [ ] Security headers enabled
- [ ] Regular backups scheduled
- [ ] System updates automated
- [ ] Log monitoring setup

## 📞 Troubleshooting

### Common issues:
1. **502 Bad Gateway**: Check Gunicorn status
2. **Static files not loading**: Check file permissions
3. **Database connection error**: Verify MySQL credentials
4. **SSL issues**: Check certificate validity

### Debug commands:
```bash
# Check service status
sudo systemctl status lms-gunicorn
sudo systemctl status nginx

# Test Django
cd /var/www/lms && python manage.py check --deploy

# Check disk space
df -h

# Check memory usage
free -h
```

## 🌐 DNS Configuration

Cấu hình DNS records:
- A record: lms-vn.com → Server IP
- A record: www.lms-vn.com → Server IP
- CNAME: www → lms-vn.com (optional)

Sau khi deploy thành công, truy cập:
- Website: https://lms-vn.com
- Admin: https://lms-vn.com/admin/
