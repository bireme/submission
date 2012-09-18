from django.template.defaultfilters import slugify
from django_tools.middlewares.ThreadLocal import get_current_user, get_current_request
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from django.db import models
import os

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

class TypeSubmission(Generic):

    TYPE_CHOICES = (
        ('rev', 'Revista'),
        ('mono', 'Monografia'),
        ('express', 'LILACS Express'),
    )

    VERSION_CHOICES = (
        ('1.5', '1.5'),
        ('1.6', '1.6'),
        ('1.7', '1.7'),
        ('1.7a', '1.7a'),
        ('1.7b', '1.7b'),
    )

    class Meta:
        verbose_name = 'type in submission'
        verbose_name_plural = 'types in submission'

    submission = models.ForeignKey("Submission", unique=True)

    def iso_filename(self):
        return os.path.basename(self.iso_file.name)

    # Function that remove spaces and special characters from filenames
    def new_filename(instance, filename):
        user = get_current_user()
        request = get_current_request()
        fname, dot, extension = filename.rpartition('.')

        type = request.POST.get('type')        

        dir = os.path.join(settings.MEDIA_ROOT, 'attac')
        dir = os.path.join(dir, unicode(user))
        dir = os.path.join(dir, type)
        try:
            path, dirs, files = os.walk(dir).next()
            next_number = len(files) + 1
        except:
            next_number = 1
        fname = slugify("%s-%s-%s" % (user, type, next_number))
        
        return os.path.join(dir, '%s.%s' % (fname, extension))
        
    
    # iso    
    type = models.CharField("Type of Records", max_length=10, choices=TYPE_CHOICES, default='e', null=True, blank=True)
    total_records = models.CharField("total of records", max_length=255, blank=True, null=True, default=0)
    certified = models.CharField("total of certified records", max_length=255, blank=True, null=True, default=0)
    iso_file = models.FileField('iso file', upload_to=new_filename, blank=True, null=True)
    lildbi_version = models.CharField("Lildbi version", max_length=255, choices=VERSION_CHOICES, blank=True, null=True)

    def get_iso_url(self):
        return unicode(self.iso_file.name.replace(settings.MEDIA_ROOT, settings.MEDIA_URL))

class Submission(Generic):

    class Meta:
        verbose_name = "submission"
        verbose_name_plural = "submissions"

    type = models.ForeignKey("Type")
    current_status = models.ForeignKey("Step", verbose_name="Current Status")
    observation = models.TextField("observation", blank=True, null=True)

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
        return settings.MEDIA_ROOT + '/attac/' + '%s.%s' % (fname, extension)

    submission = models.ForeignKey('Submission')
    previous_status = models.ForeignKey('Step', related_name="+")
    current_status = models.ForeignKey('Step', related_name="+")
    message = models.TextField("message", blank=True, null=True)
    attachment = models.FileField('attachment', upload_to=new_filename, blank=True, null=True)
    staff_message = models.TextField('staff message', blank=True, null=True)

    def __unicode__(self):
        return unicode(self.submission)

    def get_attachment_url(self):
        return unicode(self.attachment.name.replace(settings.MEDIA_ROOT, settings.MEDIA_URL))