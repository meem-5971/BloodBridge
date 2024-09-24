from django.db import models
from user.models import User

class BloodRequest(models.Model):
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests')
    blood_group = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='accepted_requests')
    status = models.CharField(max_length=20, default="Pending")

    def __str__(self):
        return f"Requester: {self.requester.username}, Blood Group: {self.blood_group}"
