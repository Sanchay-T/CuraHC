from django.urls import path
from .views import *

urlpatterns = [
    path("admin/dashboard/", AdminDashboardView.as_view(), name="admin_dashboard"),
    path(
        "admin/appointments/", AdminAppointmentView.as_view(), name="admin_appointments"
    ),
    path(
        "admin/doctors/<int:doctor_id>/appointments/",
        DoctorAppointmentsView.as_view(),
        name="doctor_appointments",
    ),
]

