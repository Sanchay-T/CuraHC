from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from doctorportal.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("adminapp.urls")),  # add this line
    # Custom admin dashboard should come before the default 'admin/' path
    # Default admin URLs
    # Include authentication URLs from Django
    path("accounts/", include("django.contrib.auth.urls")),
    # Your custom login and logout views
    path(
        "",
        CustomLoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="logged_out.html"),
        name="logout",
    ),
    # Doctor specific URLs
    path("doctor/add/", DoctorCreateView.as_view(), name="doctor_add"),
    path("doctor/<int:pk>/", DoctorDetailView.as_view(), name="doctor_detail"),
    path("doctor/<int:pk>/update/", DoctorUpdateView.as_view(), name="doctor_update"),
    # Other paths
    path("add-appointments/", add_appointment, name="add_appointments"),
    path("view-appointments/", view_appointments, name="view_appointments"),
    path(
        "appointments/<int:appointment_id>/edit/",
        update_appointment,
        name="edit_appointment",
    ),
    path(
        "appointments/<int:appointment_id>/delete/",
        delete_appointment,
        name="delete_appointment",
    ),
    # Include any other URL patterns here
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
