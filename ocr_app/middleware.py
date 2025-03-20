from django.http import JsonResponse
from django.conf import settings

class APIKeyMiddleware:
    """
    Middleware for API key authentication.
    
    Requires X-API-Key header for all /api/ routes.
    Set API_KEY in settings.py or environment variables.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            api_key = request.headers.get('X-API-Key')
            if not api_key:
                return JsonResponse({'error': 'API key is required'}, status=401)
            
            valid_api_key = getattr(settings, 'API_KEY', '')
            if api_key != valid_api_key:
                return JsonResponse({'error': 'Invalid API key'}, status=403)
        
        return self.get_response(request)