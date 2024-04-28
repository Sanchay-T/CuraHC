from django.shortcuts import redirect
from django.urls import reverse

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not hasattr(request.user, 'doctor_profile'):
            if request.path not in [reverse('doctor_add'), reverse('logout'), reverse('login')]:
                return redirect('doctor_add')
        response = self.get_response(request)
        return response
