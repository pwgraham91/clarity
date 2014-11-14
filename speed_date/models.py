from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # username is RTC's userID
    # full name will be first_name + last_name and be RTC's userName

    def __unicode__(self):
        return u"{}".format(self.username)