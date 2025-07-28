import logging
from datetime import datetime
from django.http import HttpResponseForbidden, JsonResponse
import time
from django.http import JsonResponse
from collections import defaultdict

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Configure logger to write to requests.log
        logging.basicConfig(
            filename='requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'AnonymousUser'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow only between 18:00 (6PM) and 21:00 (9PM)
        if current_hour < 18 or current_hour >= 21:
            return HttpResponseForbidden("Access to the chat is only allowed between 6PM and 9PM.")
        return self.get_response(request)

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track request count and first request timestamp per IP
        self.request_log = defaultdict(lambda: {"count": 0, "start_time": time.time()})

    def __call__(self, request):
        # Apply only to POST requests to /messages/ endpoint
        if request.method == "POST" and "/messages" in request.path:
            ip = self.get_client_ip(request)
            now = time.time()
            data = self.request_log[ip]

            # Reset if more than 60 seconds has passed
            if now - data["start_time"] > 60:
                data["count"] = 0
                data["start_time"] = now

            data["count"] += 1

            if data["count"] > 5:
                return JsonResponse(
                    {"error": "Rate limit exceeded: Only 5 messages per minute allowed."},
                    status=429
                )

        return self.get_response(request)

    def get_client_ip(self, request):
        """Handle proxy headers if any"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        protected_paths = ['/messages/', '/conversations/']

        if any(path in request.path for path in protected_paths):
            user = request.user

            if not user.is_authenticated:
                return JsonResponse(
                    {"error": "Authentication required."},
                    status=403
                )

            # Custom role check (assuming 'role' field is on User model)
            user_role = getattr(user, 'role', None)

            if user_role not in ['admin', 'moderator']:
                return JsonResponse(
                    {"error": "Access denied. Insufficient permissions."},
                    status=403
                )

        return self.get_response(request)
