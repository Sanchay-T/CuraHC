from django import forms
from .models import Doctor, Appointment, Day
from django.forms import MultiWidget, TimeInput
from django.forms.widgets import SelectDateWidget, TimeInput
from django.forms import DateTimeInput


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = ["name"]


class DoctorForm(forms.ModelForm):
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={"type": "time"}))

    class Meta:
        model = Doctor
        exclude = ["user","profile_completed"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "available_days": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(DoctorForm, self).__init__(*args, **kwargs)
        # Set form-control class selectively, exclude checkboxes
        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"
        self.fields["available_days"].required = False

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time and end_time <= start_time:
            raise forms.ValidationError("End time must be after the start time.")
        return cleaned_data


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "patient_name",
            "appointment_time",
            "number_of_sessions",
            "rx_complete",
            "amount",
            "payment_method",
        ]
        widgets = {
            "appointment_time": DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
        }

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.fields["appointment_time"].input_formats = ("%Y-%m-%dT%H:%M",)
