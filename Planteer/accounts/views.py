from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import RegisterForm

# Helper to get redirect target safely
def get_redirect_target(request):
    """
    Return the redirect URL for login/register success:
    1. Check POST "next"
    2. Check GET "next"
    3. Fallback to LOGIN_REDIRECT_URL
    """
    return request.POST.get("next") or request.GET.get("next") or settings.LOGIN_REDIRECT_URL

# -------------------
# REGISTER
# -------------------
def register_view(request):
    next_url = request.GET.get("next", "")  # Get next param from URL

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in immediately

            messages.success(request, f"Welcome, {user.username}! Your account has been created.")

            # Redirect to 'next' if provided, otherwise fallback to home
            return redirect(request.POST.get('next') or 'main:home_view')
        else:
            # Add form errors as messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return redirect(request.path_info)

    else:
        form = RegisterForm()

    return render(request, 'accounts/signup.html', {'form': form, 'next': next_url})

# -------------------
# LOGIN
# -------------------
def login_view(request):
    next_url = request.GET.get("next", "")
    """
    Handle user login.
    Authenticates user, sets session, redirects to 'next' or fallback.
    """
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(get_redirect_target(request))
        else:
            messages.error(request, "Invalid username or password.")
            return redirect(request.path_info)

    # For GET request or failed login
    return render(request, 'accounts/signin.html', {'next': next_url})

# -------------------
# LOGOUT
# -------------------
@login_required
def logout_view(request):
    """
    Log out the user and redirect to home page.
    """
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect(settings.LOGOUT_REDIRECT_URL or '/')

# -------------------
# PROFILE
# -------------------
@login_required
def profile_view(request):
    """
    Show user profile page.
    """
    return render(request, 'accounts/profile.html', {'user': request.user})
