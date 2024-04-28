from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Day(models.Model):
    name = models.CharField(max_length=9, unique=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    whatsapp_number = models.CharField(max_length=15)
    alternate_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    speciality = models.CharField(max_length=100)
    registration_number = models.CharField(max_length=50)
    available_days = models.ManyToManyField(Day)
    start_time = models.TimeField(default="00:00:00")
    end_time = models.TimeField(default="23:59:59")
    geographical_areas = models.TextField()
    photo = models.ImageField(upload_to="doctors_photos/")
    degree_certificate = models.ImageField(upload_to="doctors_certificates/")
    profile_completed = models.BooleanField(default=False)


# class TimeRange(models.Model):
#     doctor = models.ForeignKey(
#         Doctor, on_delete=models.CASCADE, related_name="time_ranges"
#     )
#     day = models.ForeignKey(Day, on_delete=models.CASCADE)
#     start_time = models.TimeField()
#     end_time = models.TimeField()

#     def __str__(self):
#         return f"{self.day.name}: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=100)
    appointment_time = models.DateTimeField()
    number_of_sessions = models.IntegerField()
    rx_complete = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=50, blank=True, null=True
    )  # gpay, cash, etc.

    def __str__(self):
        return f"{self.patient_name} - {self.appointment_time}"
