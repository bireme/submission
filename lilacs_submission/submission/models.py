from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from django.db import models
import os, md5

TYPE_CHOICES = (
    ('iso', "ISO File"),
    ('oai', "OAI PMH"),
)

STATUS_CHOICES = (
    ('a', 'approved'),
    ('p', 'pending'),
    ('d', 'declined'),
)

class Generic(models.Model):

    class Meta:
        abstract = True

    created = models.DateTimeField("created", default=datetime.now())
    updated = models.DateTimeField("updated", default=datetime.now())
    creator = models.ForeignKey(User, null=True, blank=True, related_name="+")
    updater = models.ForeignKey(User, null=True, blank=True, related_name="+")

    def save(self):
        self.updated = datetime.now()
        super(Generic, self).save()

class Step(Generic):

    class Meta:
        verbose_name = "step"
        verbose_name_plural = "steps"

    type = models.ForeignKey("Type")
    title = models.CharField("title", max_length=255)
    parent = models.ForeignKey('Step', blank=True, null=True)
    finish = models.BooleanField('finish step?')
    pending = models.BooleanField('pending step?')
    close = models.BooleanField('close step?')

    def __unicode__(self):
        return unicode(self.title)

class Type(Generic):

    class Meta:
        verbose_name = "type"
        verbose_name_plural = "types"

    title = models.CharField("title", max_length=255)

    def __unicode__(self):
        return unicode(self.title)

class Submission(Generic):

    class Meta:
        verbose_name = "submission"
        verbose_name_plural = "submissions"

    # Function that remove spaces and special characters from filenames
    def new_filename(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        fname = slugify(fname)
        fname = fname + "_" + md5.new(fname).hexdigest()
        return settings.MEDIA_ROOT + '/iso/' + '%s.%s' % (fname, extension)

    type = models.ForeignKey("Type")
    current_status = models.ForeignKey("Step", verbose_name="Current Status")
    iso_file = models.FileField('iso file', upload_to=new_filename, blank=True, null=True)
    observation = models.TextField("observation", blank=True, null=True)

    def get_iso_url(self):
        return unicode(self.iso_file).replace(settings.MEDIA_ROOT, '')

    def __unicode__(self):
        return unicode(self.type)

class FollowUp(Generic):

    class Meta:
        verbose_name = "follow up"
        verbose_name_plural = "follow ups"

    # Function that remove spaces and special characters from filenames
    def new_filename(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        fname = slugify(fname)
        fname = fname + "_" + md5.new(fname).hexdigest()
        return settings.MEDIA_ROOT + '/attac/' + '%s.%s' % (fname, extension)

    submission = models.ForeignKey('Submission')
    previous_status = models.ForeignKey('Step', related_name="+")
    current_status = models.ForeignKey('Step', related_name="+")
    message = models.TextField("message", blank=True, null=True)
    attachment = models.FileField('attachment', upload_to=new_filename, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.submission)

    def get_attachment_url(self):
        return unicode(self.attachment).replace(settings.MEDIA_ROOT, '')