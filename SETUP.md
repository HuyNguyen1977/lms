# Hướng dẫn cài đặt nhanh LMS

## Bước 1: Cài đặt Python và MySQL
- Cài đặt Python 3.8+ từ https://python.org
- Cài đặt MySQL Server từ https://dev.mysql.com/downloads/mysql/

## Bước 2: Tạo database MySQL
```sql
CREATE DATABASE lms_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'lms_user'@'localhost' IDENTIFIED BY 'lms_password';
GRANT ALL PRIVILEGES ON lms_db.* TO 'lms_user'@'localhost';
FLUSH PRIVILEGES;
```

## Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

## Bước 4: Cấu hình database trong settings.py
Cập nhật thông tin database trong `lms_project/settings.py`:
```python
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
```

## Bước 5: Chạy migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## Bước 6: Tạo superuser
```bash
python manage.py createsuperuser
```

## Bước 7: Tạo dữ liệu mẫu (tùy chọn)
```bash
python manage.py shell < create_sample_data.py
```

## Bước 8: Chạy server
```bash
python manage.py runserver
```

## Truy cập ứng dụng
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Tài khoản mẫu (nếu đã chạy create_sample_data.py)
- Giảng viên: instructor1 / password123
- Học viên: student1 / password123
