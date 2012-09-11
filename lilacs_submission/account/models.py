from django.contrib.auth.models import User
from django.db import models
from center.models import *

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)
    center = models.ForeignKey(Center, null=True)
    is_admin = models.BooleanField("is center administrator?")
