from doctorportal.models import Doctor
from django.urls import reverse


class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request before view (and other middleware) are called.
        response = self.get_response(request)

        # Check if the user is authenticated and is not a superuser.
        if request.user.is_authenticated and not request.user.is_superuser:
            # Check if the user has a Doctor profile.
            if not Doctor.objects.filter(user=request.user).exists():
                # Check if the current path is not one of the specified paths.
                if request.path not in [
                    reverse("doctor_add"),
                    reverse("logout"),
                    reverse("login"),
                    reverse("admin:index"),  # Ensure to include the admin index path
                ]:
                    # Redirect to the doctor profile creation page.
                    return redirect("doctor_add")

        # Otherwise, return the response.
        return response
