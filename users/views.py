from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


def register(request):
    """Đăng ký tài khoản"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Tạo profile cho user mới
            Profile.objects.create(user=user)
            messages.success(request, 'Đăng ký thành công! Bạn có thể đăng nhập ngay bây giờ.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    """Trang profile của user"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    return render(request, 'users/profile.html', {'profile': profile})


@login_required
def edit_profile(request):
    """Chỉnh sửa profile"""
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Cập nhật thông tin User
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        # Cập nhật thông tin Profile
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.bio = request.POST.get('bio', '')
        profile.user_type = request.POST.get('user_type', 'student')
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            profile.date_of_birth = date_of_birth
        
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        messages.success(request, 'Cập nhật profile thành công!')
        return redirect('profile')
    
    return render(request, 'users/edit_profile.html', {'profile': profile})