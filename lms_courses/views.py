from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Course, Category, Enrollment, Lesson, Assignment, Quiz


def home(request):
    """Trang chủ"""
    featured_courses = Course.objects.filter(status='published')[:6]
    categories = Category.objects.all()[:8]
    
    context = {
        'featured_courses': featured_courses,
        'categories': categories,
    }
    return render(request, 'lms_courses/home.html', context)


def course_list(request):
    """Danh sách khóa học"""
    courses = Course.objects.filter(status='published')
    categories = Category.objects.all()
    
    # Lọc theo danh mục
    category_id = request.GET.get('category')
    if category_id:
        courses = courses.filter(category_id=category_id)
    
    # Tìm kiếm
    search_query = request.GET.get('search')
    if search_query:
        courses = courses.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # Phân trang
    paginator = Paginator(courses, 12)
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)
    
    context = {
        'courses': courses,
        'categories': categories,
        'current_category': category_id,
        'search_query': search_query,
    }
    return render(request, 'lms_courses/course_list.html', context)


def course_detail(request, course_id):
    """Chi tiết khóa học"""
    course = get_object_or_404(Course, id=course_id, status='published')
    lessons = course.lessons.all()
    assignments = course.assignments.all()
    quizzes = course.quizzes.all()
    
    # Kiểm tra xem user đã đăng ký chưa
    is_enrolled = False
    enrollment = None
    if request.user.is_authenticated:
        try:
            enrollment = Enrollment.objects.get(student=request.user, course=course)
            is_enrolled = True
        except Enrollment.DoesNotExist:
            pass
    
    context = {
        'course': course,
        'lessons': lessons,
        'assignments': assignments,
        'quizzes': quizzes,
        'is_enrolled': is_enrolled,
        'enrollment': enrollment,
    }
    return render(request, 'lms_courses/course_detail.html', context)


@login_required
def enroll_course(request, course_id):
    """Đăng ký khóa học"""
    course = get_object_or_404(Course, id=course_id, status='published')
    
    # Kiểm tra xem đã đăng ký chưa
    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
        defaults={'status': 'active'}
    )
    
    if created:
        messages.success(request, f'Bạn đã đăng ký thành công khóa học "{course.title}"')
    else:
        messages.info(request, f'Bạn đã đăng ký khóa học "{course.title}" rồi')
    
    return redirect('course_detail', course_id=course_id)


@login_required
def my_courses(request):
    """Khóa học của tôi"""
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    
    context = {
        'enrollments': enrollments,
    }
    return render(request, 'lms_courses/my_courses.html', context)


@login_required
def course_learning(request, course_id):
    """Trang học khóa học"""
    course = get_object_or_404(Course, id=course_id)
    
    # Kiểm tra xem user có đăng ký khóa học này không
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'Bạn chưa đăng ký khóa học này')
        return redirect('course_detail', course_id=course_id)
    
    lessons = course.lessons.all()
    assignments = course.assignments.all()
    quizzes = course.quizzes.all()
    
    context = {
        'course': course,
        'enrollment': enrollment,
        'lessons': lessons,
        'assignments': assignments,
        'quizzes': quizzes,
    }
    return render(request, 'lms_courses/course_learning.html', context)


@login_required
def lesson_detail(request, course_id, lesson_id):
    """Chi tiết bài học"""
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    
    # Kiểm tra xem user có đăng ký khóa học này không
    try:
        enrollment = Enrollment.objects.get(student=request.user, course=course)
    except Enrollment.DoesNotExist:
        messages.error(request, 'Bạn chưa đăng ký khóa học này')
        return redirect('course_detail', course_id=course_id)
    
    # Lấy bài học trước và sau
    previous_lesson = Lesson.objects.filter(
        course=course, order__lt=lesson.order
    ).order_by('-order').first()
    
    next_lesson = Lesson.objects.filter(
        course=course, order__gt=lesson.order
    ).order_by('order').first()
    
    context = {
        'course': course,
        'lesson': lesson,
        'enrollment': enrollment,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
    }
    return render(request, 'lms_courses/lesson_detail.html', context)


@login_required
def instructor_dashboard(request):
    """Dashboard cho giảng viên"""
    if not request.user.profile.user_type == 'instructor':
        messages.error(request, 'Bạn không có quyền truy cập trang này')
        return redirect('home')
    
    courses = Course.objects.filter(instructor=request.user)
    total_students = Enrollment.objects.filter(course__instructor=request.user).count()
    
    context = {
        'courses': courses,
        'total_students': total_students,
    }
    return render(request, 'lms_courses/instructor_dashboard.html', context)