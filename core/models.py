
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class Facility(models.Model):
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=32, unique=True)
    def __str__(self):
        return f"{self.name} ({self.code})"

class User(AbstractUser):
    email = models.EmailField(unique=True)
    facility = models.ForeignKey(Facility, null=True, blank=True, on_delete=models.SET_NULL)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class PublishRequest(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)
    created_by = models.ForeignKey('User', on_delete=models.CASCADE)
    match_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.consent:
            raise ValidationError({'consent': 'İzin kutusu işaretlenmeli'})
        if self.end_time <= self.start_time:
            raise ValidationError({'end_time': 'Bitiş saati başlangıçtan sonra olmalı'})