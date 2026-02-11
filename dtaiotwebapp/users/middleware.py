from django.http import HttpResponseForbidden

class AppOnlyAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow API paths always
        if request.path.startswith('/api/'):
            return self.get_response(request)

        # Check User-Agent
        ua = request.META.get('HTTP_USER_AGENT', '').lower()
        if 'wv' not in ua and 'android' not in ua:
            return HttpResponseForbidden("Only accessible via mobile app")

        # Check secret header
        if request.headers.get("X-APP") != "AIOT_APP":
            return HttpResponseForbidden("Unauthorized app access")

        return self.get_response(request)
