import logging
from django.http import HttpResponseForbidden

logger = logging.getLogger(__name__)

class BlockGitAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '.git' in request.path:
            logger.warning(f"Blocked git path access attempt: {request.path}")
            return HttpResponseForbidden()
        return self.get_response(request)