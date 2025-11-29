from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
# تم حذف استيرادات forms و UserCreationForm الزائدة
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.models import Profile
from plants.models import Comment 
# استيراد النماذج من ملف forms.py الذي أنشأناه
from .forms import CustomUserForm, ProfileUpdateForm 
from django.db import transaction

User = get_user_model()

@transaction.atomic
def signup_view(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST) 
        profile_form_check = ProfileUpdateForm(request.POST, request.FILES) 
        
        if user_form.is_valid() and profile_form_check.is_valid():
            
            # 1. إنشاء المستخدم
            user = user_form.save(commit=True) 

            # 2. تحديث الملف الشخصي الحالي
            try:
                profile_instance = user.profile
            except Profile.DoesNotExist:
                profile_instance = Profile(user=user)

            # 3. نستخدم النموذج لتحديث الملف الشخصي الحالي ببيانات النموذج
            profile_form_update = ProfileUpdateForm(request.POST, request.FILES, instance=profile_instance)
            
            if profile_form_update.is_valid():
                profile_form_update.save() 
                
                login(request, user)
                messages.success(request, 'Account created successfully!')
                return redirect('main:home_view')
            else:
                user.delete() 
                context = {
                    'user_form': user_form,
                    'profile_form': profile_form_update
                }
                return render(request, 'accounts/signup.html', context)
        else:
            context = {
                'user_form': user_form,
                'profile_form': profile_form_check
            }
            return render(request, 'accounts/signup.html', context)
            
    else:
        user_form = CustomUserForm()
        profile_form = ProfileUpdateForm()
        
        context = {
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'accounts/signup.html', context)

# --- profile_update_view (تعديل الملف الشخصي) ---
@login_required(login_url='accounts:login')
def profile_update_view(request):
    profile_instance = get_object_or_404(Profile, user=request.user)

    if request.method == 'POST':
        profile_form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=profile_instance
        )

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            
            return redirect('accounts:user_profile_view', user_name=request.user.username)
    else:
        profile_form = ProfileUpdateForm(instance=profile_instance)

    context = {
        'form': profile_form, 
        'user_profile': profile_instance,
        'user': request.user, 
        'page_title': 'Update Profile'
    }
    
    return render(request, 'accounts/profile.html', context)

# --- user_profile_view (عرض ملف مستخدم آخر) ---
def user_profile_view(request, user_name):
    # نبحث عن المستخدم باستخدام user_name
    user = get_object_or_404(User, username=user_name) 
    
    # نحصل على الملف الشخصي (Profile)
    user_profile = get_object_or_404(Profile, user=user)
    
    # نحصل على تقييمات/تعليقات المستخدم
    user_reviews = Comment.objects.filter(user=user).order_by('-created_at')

    context = {
        'target_user': user,
        'user_profile': user_profile,
        'user_reviews': user_reviews,
        'page_title': f'{user_name} Profile',
        'user': user, 
    }
    return render(request, 'accounts/profile.html', context)