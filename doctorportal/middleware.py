from django.shortcuts import redirect
from django.urls import reverse
from .models import Doctor


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Skip middleware for non-authenticated users or superusers
        if not request.user.is_authenticated or request.user.is_superuser:
            return response

        # Redirect to profile creation if no doctor profile exists
        if (
            not hasattr(request.user, "doctor_profile")
            and not Doctor.objects.filter(user=request.user).exists()
        ):
            if request.path not in [
                reverse("doctor_add"),
                reverse("logout"),
                reverse("login"),
                reverse(
                    "admin:index"
                ),  # Make sure this is the correct reverse for your admin index
            ]:
                return redirect("doctor_add")

        return response
