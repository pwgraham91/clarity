from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # male=True female=False
    preference = models.BooleanField(default=False)
    gender = models.BooleanField(default=True)

    def __unicode__(self):
        return u"{}".format(self.username)


class Chat(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, related_name='user_sender')
    recipient = models.ForeignKey(User, related_name='user_recipient')
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{} messaged {}".format(self.sender, self.recipient)