from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Define choices for blood groups
BLOOD_GROUPS = [
    ('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'),
    ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
    ('AB+', 'AB+'), ('AB-', 'AB-')
]

from datetime import timedelta
from django.utils import timezone

class User(AbstractUser):
    # Additional fields for custom user
    phone = models.CharField(max_length=15, unique=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    last_donation_date = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True
    )

    def __str__(self):
        return self.username
    
    @property
    def is_available(self):
        """Returns True if the user is available to donate based on the last donation date."""
        if not self.last_donation_date:
            return True  # If no donation has been made yet, the user is available
        return timezone.now().date() >= self.last_donation_date + timedelta(days=120)





class DonationHistory(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donor_history')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient_history')
    donation_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Donor: {self.donor.username}, Recipient: {self.recipient.username}"
