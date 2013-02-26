from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db import models
from center.models import *

class UserProfile(models.Model):

    user = models.ForeignKey(User, unique=True)
    center = models.ForeignKey(Center, null=True)
    is_admin = models.BooleanField(_("is center administrator?"))
    is_ccn = models.BooleanField(_("is national center?"))
    receive_email = models.BooleanField(_("Allow to receive emails?"), default=True)
