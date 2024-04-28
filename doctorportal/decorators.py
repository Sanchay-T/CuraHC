# decorators.py
from django.shortcuts import redirect
from django.http import HttpResponseForbidden



def not_for_admins(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('admin_dashboard')  # Redirect admins to the admin dashboard
        return view_func(request, *args, **kwargs)

    return wrapped_view