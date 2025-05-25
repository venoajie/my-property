# apps/core/middleware.py
"""
Git Access Protection Middleware

Security Purpose:
- Blocks all requests containing '.git' in the URL path
- Prevents exposure of version control metadata
- Logs access attempts for security auditing

Implementation Details:
- Case-insensitive path matching
- URL-decoding validation
- Security headers injection
- Dedicated security logging
"""

import logging
from urllib.parse import unquote
from django.http import HttpResponseForbidden
from django.conf import settings

# Initialize security logger
security_logger = logging.getLogger('apps.security')

class BlockGitAccessMiddleware:
    """
    Middleware to block requests accessing Git-related paths
    
    Security Features:
    1. Case-insensitive path checking
    2. URL decoding detection
    3. Security headers injection
    4. Detailed attempt logging
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.blocked_patterns = getattr(settings, 'BLOCKED_PATH_PATTERNS', [r'\.git'])

    def __call__(self, request):
        try:
            return self._process_request(request)
        except Exception as e:
            security_logger.error(f"Middleware error: {str(e)}", 
                                extra={'ip': request.META.get('REMOTE_ADDR')})
            return HttpResponseForbidden()

    def _process_request(self, request):
        """Main request processing logic with enhanced security checks"""
        decoded_path = unquote(request.path).lower()
        
        if any(pattern.lower() in decoded_path for pattern in self.blocked_patterns):
            return self._block_request(request, decoded_path)
            
        return self.get_response(request)

    def _block_request(self, request, decoded_path):
        """Handle blocked requests with security logging and headers"""
        client_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown')
        
        security_logger.warning(
            "Blocked Git path access attempt",
            extra={
                'path': request.path,
                'decoded_path': decoded_path,
                'ip': client_ip,
                'user_agent': user_agent,
                'method': request.method
            }
        )
        
        response = HttpResponseForbidden()
        self._add_security_headers(response)
        return response

    def _add_security_headers(self, response):
        """Inject security headers for blocked responses"""
        response.headers['Content-Type'] = 'text/plain'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'none'"
        response.headers['Cache-Control'] = 'no-store, max-age=0'