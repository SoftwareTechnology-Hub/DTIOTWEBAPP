from django.http import HttpResponseForbidden

class AppOnlyAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Always allow API paths
        if request.path.startswith('/api/'):
            return self.get_response(request)

        if request.path.startswith('/admin/'):
            return self.get_response(request)


        # Always allow POST requests (login/signup forms)
        if request.method == "POST":
            return self.get_response(request)

        # Allow if header is correct
        if request.headers.get("X-APP") == "AIOT_APP":
            return self.get_response(request)

        # Allow if request comes from WebView / Android
        ua = request.META.get('HTTP_USER_AGENT', '').lower()
        if "wv" in ua or "android" in ua:
            return self.get_response(request)

        # Otherwise block
        return HttpResponseForbidden("App access only")
