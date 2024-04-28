from doctorportal.models import Doctor
from django.urls import reverse


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.user.is_authenticated:
            return response

        if request.user.is_superuser:
            return response

        if Doctor.objects.filter(user=request.user).exists():
            return response

        if request.path not in [
            reverse("doctor_add"),
            reverse("logout"),
            reverse("login"),
        ]:
            return redirect("doctor_add")

        return response
