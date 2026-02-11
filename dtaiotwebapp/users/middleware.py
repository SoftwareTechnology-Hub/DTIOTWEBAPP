from django.http import HttpResponseForbidden

class AppOnlyAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow API paths always
        if request.path.startswith('/api/'):
            return self.get_response(request)

        # Allow POST requests (login/signup)
        if request.method == "POST":
            return self.get_response(request)

        # Allow requests with correct app header
        if request.headers.get("X-APP") == "AIOT_APP":
            return self.get_response(request)

        # Otherwise block browsers
        ua = request.META.get("HTTP_USER_AGENT", "").lower()
        if "wv" in ua or "android" in ua:
            return self.get_response(request)  # Allow Android WebView GETs

        return HttpResponseForbidden("App access only")
