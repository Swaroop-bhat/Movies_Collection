from django.conf import settings


# class RequestCounterMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#         if not hasattr(settings, 'REQUEST_COUNT'):
#             settings.REQUEST_COUNT = 0

#     def __call__(self, request):
#         settings.REQUEST_COUNT = settings.REQUEST_COUNT + 1
#         response = self.get_response(request)
#         return response
    
class RequestCounterMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0

    def __call__(self, request):
        self.request_count += 1
        response = self.get_response(request)
        return response
