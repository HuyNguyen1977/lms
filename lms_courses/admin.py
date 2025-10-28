from django.contrib import admin
from .models import (
    Category, Course, Enrollment, Lesson, Assignment, 
    Submission, Quiz, Question, Answer, QuizAttempt, QuizResponse
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'instructor', 'category', 'price', 'status', 'created_at']
    list_filter = ['status', 'difficulty_level', 'category', 'created_at']
    search_fields = ['title', 'description', 'instructor__username']
    ordering = ['-created_at']
    raw_id_fields = ['instructor']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'status', 'enrolled_at']
    list_filter = ['status', 'enrolled_at']
    search_fields = ['student__username', 'course__title']
    ordering = ['-enrolled_at']
    raw_id_fields = ['student', 'course']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order', 'duration_minutes', 'is_free']
    list_filter = ['is_free', 'course']
    search_fields = ['title', 'course__title']
    ordering = ['course', 'order']
    raw_id_fields = ['course']


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'due_date', 'max_points']
    list_filter = ['due_date', 'course']
    search_fields = ['title', 'course__title']
    ordering = ['-created_at']
    raw_id_fields = ['course']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['student', 'assignment', 'submitted_at', 'points']
    list_filter = ['submitted_at', 'assignment__course']
    search_fields = ['student__username', 'assignment__title']
    ordering = ['-submitted_at']
    raw_id_fields = ['student', 'assignment']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'time_limit_minutes', 'max_attempts']
    list_filter = ['course', 'created_at']
    search_fields = ['title', 'course__title']
    ordering = ['-created_at']
    raw_id_fields = ['course']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'question_type', 'points', 'order']
    list_filter = ['question_type', 'quiz']
    search_fields = ['text', 'quiz__title']
    ordering = ['quiz', 'order']
    raw_id_fields = ['quiz']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct', 'order']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['text', 'question__text']
    ordering = ['question', 'order']
    raw_id_fields = ['question']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'started_at', 'completed_at', 'score']
    list_filter = ['started_at', 'quiz']
    search_fields = ['student__username', 'quiz__title']
    ordering = ['-started_at']
    raw_id_fields = ['student', 'quiz']


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'is_correct']
    list_filter = ['is_correct', 'question__quiz']
    search_fields = ['attempt__student__username', 'question__text']
    raw_id_fields = ['attempt', 'question', 'answer']