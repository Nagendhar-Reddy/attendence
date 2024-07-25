from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class Shift(models.Model):
    DAY_CHOICES = (
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    )
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'staff'})
    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

class WeeklyOff(models.Model):
    DAY_CHOICES = (
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    )
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'staff'})
    day = models.CharField(max_length=3, choices=DAY_CHOICES)

class Attendance(models.Model):
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'staff'})
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='attendance_images/')
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE)



from django.utils import timezone

class ShiftChangeRequest(models.Model):
    REQUEST_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    staff1 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requesting_staff')
    staff2 = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiving_staff')
    day = models.CharField(max_length=3, choices=Shift.DAY_CHOICES)
    status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Request from {self.staff1.username} to {self.staff2.username} for {self.day}"