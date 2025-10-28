#!/usr/bin/env python
"""
Script để tạo dữ liệu mẫu cho LMS
Chạy: python manage.py shell < create_sample_data.py
"""

from django.contrib.auth.models import User
from lms_courses.models import Category, Course, Lesson
from users.models import Profile as UserProfile

# Tạo categories
categories_data = [
    {'name': 'Lập trình', 'description': 'Các khóa học về lập trình và phát triển phần mềm'},
    {'name': 'Thiết kế', 'description': 'Thiết kế đồ họa, UI/UX, web design'},
    {'name': 'Marketing', 'description': 'Digital marketing, SEO, social media'},
    {'name': 'Kinh doanh', 'description': 'Khởi nghiệp, quản lý, tài chính'},
    {'name': 'Ngoại ngữ', 'description': 'Tiếng Anh, tiếng Nhật, tiếng Hàn'},
]

categories = []
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'description': cat_data['description']}
    )
    categories.append(category)
    if created:
        print(f"Tạo category: {category.name}")

# Tạo users
users_data = [
    {
        'username': 'instructor1',
        'email': 'instructor1@example.com',
        'first_name': 'Nguyễn',
        'last_name': 'Văn A',
        'user_type': 'instructor'
    },
    {
        'username': 'instructor2',
        'email': 'instructor2@example.com',
        'first_name': 'Trần',
        'last_name': 'Thị B',
        'user_type': 'instructor'
    },
    {
        'username': 'student1',
        'email': 'student1@example.com',
        'first_name': 'Lê',
        'last_name': 'Văn C',
        'user_type': 'student'
    },
    {
        'username': 'student2',
        'email': 'student2@example.com',
        'first_name': 'Phạm',
        'last_name': 'Thị D',
        'user_type': 'student'
    },
]

users = []
for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
        }
    )
    if created:
        user.set_password('password123')
        user.save()
        
        # Tạo profile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={'user_type': user_data['user_type']}
        )
        
        users.append(user)
        print(f"Tạo user: {user.username} ({profile.get_user_type_display()})")

# Tạo courses
courses_data = [
    {
        'title': 'Python Cơ Bản',
        'description': 'Khóa học Python từ cơ bản đến nâng cao, phù hợp cho người mới bắt đầu.',
        'instructor': users[0],  # instructor1
        'category': categories[0],  # Lập trình
        'price': 500000,
        'duration_hours': 20,
        'difficulty_level': 'beginner',
        'status': 'published'
    },
    {
        'title': 'Django Web Development',
        'description': 'Học Django để xây dựng các ứng dụng web chuyên nghiệp.',
        'instructor': users[0],  # instructor1
        'category': categories[0],  # Lập trình
        'price': 800000,
        'duration_hours': 30,
        'difficulty_level': 'intermediate',
        'status': 'published'
    },
    {
        'title': 'UI/UX Design Fundamentals',
        'description': 'Nguyên lý thiết kế giao diện người dùng và trải nghiệm người dùng.',
        'instructor': users[1],  # instructor2
        'category': categories[1],  # Thiết kế
        'price': 600000,
        'duration_hours': 25,
        'difficulty_level': 'beginner',
        'status': 'published'
    },
    {
        'title': 'Digital Marketing Strategy',
        'description': 'Chiến lược marketing số hiệu quả cho doanh nghiệp.',
        'instructor': users[1],  # instructor2
        'category': categories[2],  # Marketing
        'price': 700000,
        'duration_hours': 15,
        'difficulty_level': 'intermediate',
        'status': 'published'
    },
]

courses = []
for course_data in courses_data:
    course, created = Course.objects.get_or_create(
        title=course_data['title'],
        defaults=course_data
    )
    courses.append(course)
    if created:
        print(f"Tạo course: {course.title}")

# Tạo lessons cho course đầu tiên
python_course = courses[0]
lessons_data = [
    {
        'title': 'Giới thiệu Python',
        'content': 'Python là một ngôn ngữ lập trình cấp cao, dễ học và mạnh mẽ...',
        'duration_minutes': 30,
        'order': 1,
        'is_free': True
    },
    {
        'title': 'Cài đặt Python và IDE',
        'content': 'Hướng dẫn cài đặt Python và các công cụ phát triển...',
        'duration_minutes': 45,
        'order': 2,
        'is_free': True
    },
    {
        'title': 'Biến và Kiểu dữ liệu',
        'content': 'Tìm hiểu về các kiểu dữ liệu cơ bản trong Python...',
        'duration_minutes': 60,
        'order': 3,
        'is_free': False
    },
    {
        'title': 'Cấu trúc điều khiển',
        'content': 'If-else, vòng lặp for và while trong Python...',
        'duration_minutes': 90,
        'order': 4,
        'is_free': False
    },
]

for lesson_data in lessons_data:
    lesson_data['course'] = python_course
    lesson, created = Lesson.objects.get_or_create(
        course=python_course,
        title=lesson_data['title'],
        defaults=lesson_data
    )
    if created:
        print(f"Tạo lesson: {lesson.title}")

print("\n=== Dữ liệu mẫu đã được tạo thành công! ===")
print("Bạn có thể đăng nhập với:")
print("- instructor1 / password123 (Giảng viên)")
print("- student1 / password123 (Học viên)")
print("- Hoặc tạo superuser: python manage.py createsuperuser")
