from django_tools.middlewares.ThreadLocal import get_current_user, get_current_request
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from django.db import models
import os

class Generic(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField(_("created"), default=datetime.now())
    updated = models.DateTimeField(_("updated"), default=datetime.now())
    creator = models.ForeignKey(User, null=True, blank=True, related_name="+")
    updater = models.ForeignKey(User, null=True, blank=True, related_name="+")

    def save(self):
        self.updated = datetime.now()
        super(Generic, self).save()

class Step(Generic):

    class Meta:
        verbose_name = _("step")
        verbose_name_plural = _("steps")

    type = models.ForeignKey("Type")
    title = models.CharField(_("title"), max_length=255)
    parent = models.ForeignKey('Step', blank=True, null=True)
    finish = models.BooleanField(_('finish step?'))
    pending = models.BooleanField(_('pending step?'))
    close = models.BooleanField(_('close step?'))
    allow_edit = models.BooleanField(_('allow register edition?'))

    def __unicode__(self):
        return unicode(self.title)

class Type(Generic):

    class Meta:
        verbose_name = _("type")
        verbose_name_plural = _("types")

    title = models.CharField(_("title"), max_length=255)

    def __unicode__(self):
        return unicode(self.title)

class TypeSubmission(Generic):

    TYPE_CHOICES = (
        ('Revista', _('Revista')),
        ('Monografia', _('Monografia')),
        ('Express', _('LILACS Express')),
    )

    VERSION_CHOICES = (
        ('1.5', '1.5'),
        ('1.6', '1.6'),
        ('1.7', '1.7'),
        ('1.7a', '1.7a'),
        ('1.7b', '1.7b'),
    )

    class Meta:
        verbose_name = _('type in submission')
        verbose_name_plural = _('types in submission')

    submission = models.ForeignKey("Submission", unique=True)

    def iso_filename(self):
        return os.path.basename(self.iso_file.name)

    # Function that remove spaces and special characters from filenames
    def new_filename(instance, filename):
        user = get_current_user()
        request = get_current_request()
        fname, dot, extension = filename.rpartition('.')

        type = request.POST.get('type')
        extension = "iso"

        try:
            submissions = TypeSubmission.objects.all()
            last = submissions.reverse()[0]
            id = last.id + 1
        except:
            id = 1

        dir = os.path.join(settings.MEDIA_ROOT, 'attac')
        dir = os.path.join(dir, unicode(user))
        dir = os.path.join(dir, type)
        fname = slugify("%s-%s" % (type, id))
        fname = "%s-%s" % (user.get_profile().center.code, fname)
        
        return os.path.join(dir, '%s.%s' % (fname, extension))
        
    
    # iso    
    type = models.CharField(_("Type of Records"), max_length=10, choices=TYPE_CHOICES, default='e', null=True, blank=True)
    total_records = models.CharField(_("total of records"), max_length=255, blank=True, null=True, default=0)
    certified = models.CharField(_("total of certified records"), max_length=255, blank=True, null=True, default=0)
    iso_file = models.FileField(_('iso file'), upload_to=new_filename, blank=True, null=True)
    lildbi_version = models.CharField(_("Lildbi version"), max_length=255, choices=VERSION_CHOICES, blank=True, null=True)

    def get_iso_url(self):
        return unicode(reverse('submission.views.download') + "?filename=" + self.iso_file.name.replace(settings.MEDIA_ROOT, settings.MEDIA_URL))

class Submission(Generic):

    class Meta:
        verbose_name = _("submission")
        verbose_name_plural = _("submissions")

    type = models.ForeignKey("Type")
    current_status = models.ForeignKey("Step", verbose_name="Current Status")
    observation = models.TextField(_("observation"), blank=True, null=True)

    def __unicode__(self):
        return unicode(self.type)

class FollowUp(Generic):

    class Meta:
        verbose_name = _("follow up")
        verbose_name_plural = _("follow ups")

    # Function that remove spaces and special characters from filenames
    def new_filename(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        fname = slugify(fname)
        return settings.MEDIA_ROOT + '/attac/' + '%s.%s' % (fname, extension)

    submission = models.ForeignKey('Submission')
    previous_status = models.ForeignKey('Step', related_name="+")
    current_status = models.ForeignKey('Step', related_name="+")
    message = models.TextField(_("message"), blank=True, null=True)
    attachment = models.FileField(_('attachment'), upload_to=new_filename, blank=True, null=True)
    staff_message = models.TextField(_('staff message'), blank=True, null=True)

    def __unicode__(self):
        return unicode(self.submission)

    def get_attachment_url(self):
        return unicode(self.attachment.name.replace(settings.MEDIA_ROOT, settings.MEDIA_URL))