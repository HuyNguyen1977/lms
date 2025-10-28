# LMS - Hệ thống quản lý học tập

Hệ thống LMS (Learning Management System) được xây dựng bằng Django và MySQL, cung cấp các tính năng cơ bản cho việc dạy và học trực tuyến.

## Tính năng chính

### Cho học viên:
- Đăng ký/đăng nhập tài khoản
- Duyệt và tìm kiếm khóa học
- Đăng ký khóa học
- Học bài học trực tuyến
- Làm bài tập và bài kiểm tra
- Theo dõi tiến độ học tập

### Cho giảng viên:
- Tạo và quản lý khóa học
- Thêm bài học, bài tập, bài kiểm tra
- Theo dõi học viên
- Chấm điểm và đánh giá

### Cho quản trị viên:
- Quản lý người dùng
- Quản lý danh mục khóa học
- Thống kê hệ thống

## Cài đặt

### Yêu cầu hệ thống:
- Python 3.8+
- MySQL 5.7+
- pip

### Các bước cài đặt:

1. **Clone repository:**
```bash
git clone <repository-url>
cd LMS
```

2. **Tạo virtual environment:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

4. **Cấu hình database:**
- Tạo database MySQL với tên `lms_db`
- Cập nhật thông tin database trong `lms_project/settings.py`:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'lms_db',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

5. **Chạy migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Tạo superuser:**
```bash
python manage.py createsuperuser
```

7. **Chạy server:**
```bash
python manage.py runserver
```

8. **Truy cập ứng dụng:**
- Website: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## Cấu trúc dự án

```
LMS/
├── lms_project/          # Django project settings
├── lms_courses/          # App quản lý khóa học
├── users/                # App quản lý người dùng
├── templates/            # HTML templates
├── static/               # CSS, JS, images
├── media/                # Uploaded files
├── requirements.txt       # Python dependencies
└── manage.py            # Django management script
```

## Models chính

- **User**: Người dùng hệ thống (học viên, giảng viên, admin)
- **Profile**: Thông tin bổ sung của người dùng
- **Course**: Khóa học
- **Lesson**: Bài học trong khóa học
- **Assignment**: Bài tập
- **Quiz**: Bài kiểm tra
- **Enrollment**: Đăng ký khóa học

## API Endpoints

- `/` - Trang chủ
- `/courses/` - Danh sách khóa học
- `/course/<id>/` - Chi tiết khóa học
- `/my-courses/` - Khóa học của tôi
- `/users/register/` - Đăng ký
- `/users/login/` - Đăng nhập
- `/admin/` - Admin panel

## Phát triển thêm

### Tính năng có thể thêm:
- Video streaming
- Chat/forum
- Payment integration
- Mobile app
- Advanced analytics
- Certificate generation
- Email notifications

### Cải thiện:
- Responsive design
- Performance optimization
- Security enhancements
- Testing coverage
- Documentation

## Đóng góp

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Liên hệ

- Email: huycnn@gmail.com
- Phone: 0123 456 789
