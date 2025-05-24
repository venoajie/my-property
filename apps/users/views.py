# File: apps/users/views.py
from django.contrib.auth import login
from django.http import JsonResponse
from django_ratelimit.decorators import ratelimit
from django.views.decorators.http import require_POST

@require_POST
@ratelimit(key="post:username", rate="3/m", method="POST")
def user_login(request):
    """Handle user login with username-based rate limiting"""
    was_limited = getattr(request, 'limited', False)
    
    if was_limited:
        return JsonResponse(
            {"error": "Too many login attempts. Please try again later."},
            status=429
        )
        
@require_POST
@ratelimit(key="ip", rate="5/m", block=True)  # Stricter than default (3/m)
def user_login(request):
    """Handle user login with IP-based rate limiting"""
    # Your authentication logic here
    return JsonResponse({"status": "login successful"}, status=200)

@require_POST
@ratelimit(key="post:email", rate="3/h", method="POST")
def password_reset(request):
    """Password reset with email-based rate limiting"""
    return JsonResponse({"status": "reset email sent"}, status=200)