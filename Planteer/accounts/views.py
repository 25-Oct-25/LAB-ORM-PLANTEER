from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views import View
from .forms import SignUpForm
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib import messages

class SignUpView(View):
    template_name = "accounts/signup.html"
    form_class = SignUpForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your account has been created.")
            return redirect("main:index_view")
        else:
            messages.error(request, "Please fix the errors below.")
        return render(request, self.template_name, {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True  # redirect if already logged in

    def get_success_url(self):
        # Redirect to 'next' if present, otherwise home
        return self.get_redirect_url() or reverse_lazy("main:index_view")


# Logout view must be outside the class
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect(reverse_lazy("main:index_view"))
    response.delete_cookie(settings.SESSION_COOKIE_NAME)  # optional, clears session cookie
    return response