from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default = False)
    is_sub_admin = models.BooleanField(default = False)
    is_work_staff = models.BooleanField(default = False)
    phone_number = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200)
    is_subscribed = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)

class LoggedIn(models.Model):
    staff = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    login_id = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.staff)

class Pos(models.Model):
    name = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    staff = models.ManyToManyField(CustomUser)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'pos'

    def __str__(self):
        return str(self.name)