from django.conf import settings
from django.db import models

class FitbitUser(models.Model):
    """Adds a token to a custom User model."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fitbit_id = models.CharField(max_length=1024)
    access_token = models.CharField(max_length=1024)
    refresh_token = models.CharField(max_length=1024)
    expires_in = models.IntegerField(null=True)

    def __str__(self):
        return self.user.username
