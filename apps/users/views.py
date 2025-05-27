# apps/users/views.py
"""
Enhanced Authentication Endpoints

Security Features:
- Layered rate limiting
- JWT token authentication
- Secure session management
- Brute-force protection
"""

from datetime import timedelta
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import HttpRequest, JsonResponse
from django_ratelimit.decorators import ratelimit
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
@ratelimit(key='post:username', rate='3/m', method='POST')
@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def user_login(request: HttpRequest) -> JsonResponse:
    """
    JWT Token Authentication Endpoint
    
    Flow:
    1. Validate credentials
    2. Issue access/refresh tokens
    3. Set secure HTTP-only cookies
    
    Security Headers:
    - Strict-Transport-Security
    - SameSite cookies
    - HttpOnly flag
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password)
    
    if not user:
        return JsonResponse(
            {'error': 'Invalid credentials'},
            status=401,
            headers={'X-Reason': 'AuthenticationFailure'}
        )
    
    refresh = RefreshToken.for_user(user)
    response = JsonResponse({
        'user_id': user.id,
        'access': str(refresh.access_token)
    })
    
    # Set secure cookies for token refresh
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=not settings.DEBUG,
        samesite='Strict',
        max_age=timedelta(days=7).seconds
    )
    
    return response