from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.gis.db import models

class User(AbstractUser):
    location = models.PointField(null=True, blank=True, srid=4326, verbose_name="Location")
    

    def __unicode__(self):
        return u"{}".format(self.username)