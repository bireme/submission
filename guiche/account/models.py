from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)

# signal to ato-create an userprofile
def create_user_profile(sender, instance, created, **kwargs):
    if created: UserProfile(user=instance).save()
post_save.connect(create_user_profile, sender=User)
