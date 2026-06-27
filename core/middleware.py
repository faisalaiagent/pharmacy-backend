class AuditLogMiddleware:
    """
    Attaches request metadata (IP, user agent) to the request object so
    views/signals can create AuditLog entries without re-parsing headers.
    Actual AuditLog.objects.create() calls happen in model signals / view
    mixins (see core/mixins.py), not here — this middleware only captures
    context, keeping it dependency-free and side-effect-free.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.client_ip = self._get_client_ip(request)
        request.client_user_agent = request.META.get("HTTP_USER_AGENT", "")[:512]
        response = self.get_response(request)
        return response

    @staticmethod
    def _get_client_ip(request):
        forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
