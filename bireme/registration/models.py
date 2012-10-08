import datetime

from django_tools.middlewares.ThreadLocal import get_current_user
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from account.models import *


class RegistrationManager(models.Manager):

    
    def create_user(self, username, password, email,
                             send_email=True, profile_callback=None):

        current_user = get_current_user()
        
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = True
        new_user.save()

        profile = UserProfile(user=new_user)
        profile.center = current_user.get_profile().center
        profile.save()
    
        return new_user


class RegistrationProfile(models.Model):
    
    ACTIVATED = u"ALREADY_ACTIVATED"
    
    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    
    objects = RegistrationManager()
    
    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')
    
    def __unicode__(self):
        return u"Registration information for %s" % self.user
    
    def activation_key_expired(self):
        
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == self.ACTIVATED or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True
