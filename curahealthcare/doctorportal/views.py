# views.py

from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.contrib.auth.decorators import login_required
from doctorportal.forms import AppointmentForm, DoctorForm
from django.contrib import messages
from .models import Appointment, Doctor, Day
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from .decorators import not_for_admins
from django.utils.decorators import method_decorator


@method_decorator([login_required, not_for_admins], name="dispatch")
class CustomLoginView(LoginView):
    template_name = "registration/login.html"

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        login(self.request, form.get_user())

        # Check if the user is an administrator
        if self.request.user.is_superuser:
            # Redirect admin users to the admin-specific dashboard
            return redirect(resolve_url("admin_dashboard"))
        elif not Doctor.objects.filter(user=self.request.user).exists():
            # Redirect non-admin users without a Doctor profile to the profile creation page
            return redirect(resolve_url("doctor_add"))
        else:
            # Redirect non-admin users who already have a Doctor profile to the user-specific dashboard
            return redirect(self.get_success_url())

    def get_success_url(self):
        """
        This method returns the URL to which a regular, non-admin user should be redirected.
        You can define this based on your application's logic.
        """
        # Redirect to a user-specific dashboard or appointments view
        return resolve_url("view_appointments")


@method_decorator([login_required], name="dispatch")
class DoctorDetailView(DetailView):
    model = Doctor
    template_name = "user_viewonly.html"  # path to your template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


@method_decorator([login_required, not_for_admins], name="dispatch")
class DoctorCreateView(CreateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "user_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["button_text"] = "Create Profile"  # Dynamically set the button text
        return context

    def form_valid(self, form):
        # Associate the logged-in user with the form instance
        form.instance.user = self.request.user

        # Save the form instance and set self.object to the newly created doctor
        self.object = form.save(commit=False)
        self.object.profile_completed = True  # Mark profile as completed
        self.object.save()

        # Save many-to-many data for the form.
        form.save_m2m()

        # Since the object is saved, redirect to get_success_url
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        # Iterate over the form errors
        for field, errors in form.errors.items():
            for error in errors:
                # Add the error as a Django message
                messages.error(self.request, f"Error in {field}: {error}")

        # Return the form to the template with the non-field and field errors
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        # Make sure self.object is correctly set
        if self.object and hasattr(self.object, "pk"):
            return reverse_lazy("doctor_detail", kwargs={"pk": self.object.pk})
        else:
            # Fallback if self.object is not set
            return reverse_lazy("home")  # Adjust to appropriate fallback URL

    def dispatch(self, request, *args, **kwargs):
        # Check if the user already has a completed profile
        if (
            hasattr(request.user, "doctor_profile")
            and request.user.doctor_profile.profile_completed
        ):
            # Redirect to the detail page of the existing profile
            return redirect(
                reverse_lazy(
                    "doctor_detail", kwargs={"pk": request.user.doctor_profile.pk}
                )
            )
        return super().dispatch(request, *args, **kwargs)


@method_decorator([login_required], name="dispatch")
class DoctorUpdateView(UpdateView):
    model = Doctor
    form_class = DoctorForm
    template_name = "user_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:  # If a Doctor instance is being updated
            context["form_title"] = "Update Doctor Profile"
            context["button_text"] = "Update Profile"
        else:  # If a new Doctor instance is being created
            context["form_title"] = "Register Doctor"
            context["button_text"] = "Create Profile"
        return context

    def get_object(self):
        # Get the Doctor object for the current user
        return get_object_or_404(Doctor, user=self.request.user)

    def get_success_url(self):
        # Redirect to the doctor's detail page
        return reverse_lazy("doctor_detail", kwargs={"pk": self.object.pk})


@login_required
def view_appointments(request):
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        return render(request, "error_page.html", {"error": "Doctor profile not found"})

    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, "view_appointments.html", {"appointments": appointments})


@login_required
@not_for_admins
def add_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if not form.is_valid():
            print(
                form.errors.as_data()
            )  # This will provide more detailed error information

        if form.is_valid():
            print(form.cleaned_data)
            try:
                doctor = Doctor.objects.get(user=request.user)
                print(doctor)
                appointment = form.save(commit=False)
                appointment.doctor = doctor
                appointment.save()
                return redirect("view_appointments")
            except Doctor.DoesNotExist:
                return render(request, "error_page.html", {"error": "Doctor not found"})
        else:
            return render(
                request,
                "add_appointment.html",
                {"form": form, "error": "Form is not valid"},
            )
    else:
        form = AppointmentForm()
    return render(request, "add_appointment.html", {"form": form})


@login_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect(
                "view_appointments"
            )  # Redirect to a view that shows all appointments
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, "edit_appointment.html", {"form": form})


@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    if request.method == "POST":  # Confirming the user really wants to delete
        appointment.delete()
        return redirect("view_appointments")  # Redirect to the appointment listing
    return render(request, "confirm_delete.html", {"appointment": appointment})
