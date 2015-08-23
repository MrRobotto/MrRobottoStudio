from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models
from rest_framework.authtoken.models import Token


class AndroidDevice(models.Model):
    android_id = models.CharField(max_length=120)
    name = models.CharField(default="", max_length=30)
    user = models.ForeignKey(to=User)
    last_connection = models.DateTimeField(default=timezone.now)
    is_connected = models.BooleanField(default=False)
    #is_updated, last_mrr, last_update

class RegistrationAttemp(models.Model):
    user = models.ForeignKey(to=User)
    date = models.DateField(default=timezone.now)
    is_used = models.BooleanField(default=False)

#Cambiar blendfile por mrrfile
class MrrFile(models.Model):
    user = models.ForeignKey(to=User)
    filename = models.CharField(max_length=80)
    blend_file = models.FileField()
    mrr_file = models.FileField()
    is_selected = models.BooleanField(default=False)
    upload_date = models.DateTimeField(default=timezone.now)

