# File: apps/users/views.py
from django.contrib.auth import login
from django.http import JsonResponse
from ratelimit.decorators import ratelimit

@ratelimit(key="post:username", rate="3/m", method="POST")
def user_login(request):
    # ... existing login logic
    was_limited = getattr(request, 'limited', False)
    if was_limited:
        return JsonResponse({"error": "rate_limited"}, status=429)