from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Plan(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    max_category = models.IntegerField(default=0)
    max_staff = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
        


class Pos(models.Model):
    pos_name = models.CharField(max_length=250, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'pos'

    def __str__(self):
        return str(self.pos_name)


class CustomUser(AbstractUser):
    pos = models.ForeignKey(Pos, on_delete=models.SET_NULL, blank=True, null=True)
    is_admin = models.BooleanField(default = False)
    is_sub_admin = models.BooleanField(default = False)
    is_work_staff = models.BooleanField(default = False)
    phone_number = models.CharField(max_length = 100)
    address = models.CharField(max_length = 200)
    is_subscribed = models.BooleanField(default=True)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

class LoggedIn(models.Model):
    staff = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add = True)
    login_id = models.CharField(max_length = 100)

    def __str__(self):
        return str(self.staff)