from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # male=True female=False
    preference = models.BooleanField(default=False)
    gender = models.BooleanField(default=True)
    # want to give them an initial datetimefield that is now, then update it when they hit the chat site
    online = models.DateTimeField(auto_now_add=True)
    banned = models.BooleanField(default=False)
    # Boolean to check if they have at least 50 friends
    fifty = models.BooleanField(default=True)
    new_link = models.BigIntegerField(null=True, blank=True)


    def __unicode__(self):
        return u"{}".format(self.username)


class Chat(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User, related_name='user_sender')
    recipient = models.ForeignKey(User, related_name='user_recipient')
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"{} messaged {}".format(self.sender, self.recipient)


class Match(models.Model):
    # initial is null, liked is true, disliked is false

    logged_user = models.ForeignKey(User, related_name='user_match_logged')
    chosen_user = models.ForeignKey(User, related_name='user_match_chosen')
    user1_select = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{} rated {} {}".format(self.logged_user, self.chosen_user, self.user1_select)


class Flag(models.Model):
    offensive_user = models.ForeignKey(User, related_name="flag_offensive")
    offended_user = models.ForeignKey(User, related_name="flag_offended")

    def __unicode__(self):
        return u"{} offended {}".format(self.offensive_user, self.offended_user)