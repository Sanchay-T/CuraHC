from django.urls import path
from .views import *

urlpatterns = [
    # The base path for "admin/dashboard/"
    path("", AdminDashboardView.as_view(), name="admin_dashboard"),
    # The path for "admin/dashboard/appointments/"
    path("appointments/", AdminAppointmentView.as_view(), name="admin_appointments"),
    # The path for "admin/dashboard/doctors/<int:doctor_id>/appointments/"
    path(
        "doctors/<int:doctor_id>/appointments/",
        DoctorAppointmentsView.as_view(),
        name="doctor_appointments",
    ),
]
