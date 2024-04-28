from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from doctorportal.models import Appointment, Doctor, Day
from django.views.generic import TemplateView, ListView


# Create your views here.
class AdminDashboardView(UserPassesTestMixin, TemplateView):
    template_name = "admin_dashboard.html"

    def test_func(self):
        return (
            self.request.user.is_superuser
        )  # Ensure only superusers can access this view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all doctors and their associated user data
        context["doctors"] = Doctor.objects.select_related("user").all()
        return context


class AdminAppointmentView(UserPassesTestMixin, TemplateView):
    template_name = "doctor_view_appointments.html"

    def test_func(self):
        return (
            self.request.user.is_superuser
        )  # Ensure only superusers can access this view

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Fetch all doctors and their associated user data
        context["doctors"] = Doctor.objects.select_related("user").all()
        return context


class DoctorAppointmentsView(UserPassesTestMixin, ListView):
    model = Appointment
    template_name = "doctor_appointments.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        doctor_id = self.kwargs["doctor_id"]
        return Appointment.objects.filter(doctor_id=doctor_id).select_related("doctor")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctor"] = Doctor.objects.get(id=self.kwargs["doctor_id"])
        return context
