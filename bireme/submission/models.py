#! coding: utf-8
from django_tools.middlewares.ThreadLocal import get_current_user, get_current_request
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import RequestContext
from center.models import ExternalDatabase
from django.core.mail import EmailMessage
from django.db.models import signals
from django.conf import settings
from datetime import datetime
from django.db import models
import logging
import os

LANGUAGES_CHOICES = (
    ('en', 'English'),
    ('pt-br', 'Brazilian Portuguese'),
    ('es', 'Spanish'),
) 

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

    def get_translation(self, lang_code):
        translation = StepLocal.objects.filter(step=self.id, language=lang_code)
        if translation:
            return translation[0].title
        else:
            return self.title

    def __unicode__(self):
        return unicode(self.title)

    def get_all_steps(self):
        return len(Step.objects.all().exclude(close=True).exclude(pending=True))

    def get_step_number(self, number=1, step=None):

        if not step:
            step = self

        if step.parent:
            number = number+1
            return self.get_step_number(number=number, step=step.parent)

        return number  

    def get_current_progress(self):
        return (self.get_step_number() * 100) / self.get_all_steps()

class StepLocal(Generic):
    
    class Meta:
        verbose_name = _("step translation")
        verbose_name_plural = _("step translations")

    step = models.ForeignKey("Step")
    language = models.CharField(_('language'), max_length=255, choices=LANGUAGES_CHOICES, default="pt-br")
    title = models.CharField(_("title"), max_length=255)

class LildbiVersion(Generic):

    class Meta:
        verbose_name = _("lildbi version")
        verbose_name_plural = _("lildbi versions")

    title = models.CharField(_("title"), max_length=255)

    def __unicode__(self):
        return unicode(self.title)

class Type(Generic):

    class Meta:
        verbose_name = _("type")
        verbose_name_plural = _("types")

    title = models.CharField(_("title"), max_length=255)

    def __unicode__(self):
        return unicode(self.title)

class BibliographicType(Generic):

    class Meta:
        verbose_name = _("bibliographic type")
        verbose_name_plural = _("bibliographic types")

    title = models.CharField(_("title"), max_length=255)

    def get_translation(self, lang_code):
        translation = BibliographicTypeLocal.objects.filter(bibliographic_type=self.id, language=lang_code)
        if translation:
            return translation[0].title
        else:
            return self.title

    def __unicode__(self):
        return unicode(self.title)

class BibliographicTypeLocal(Generic):

    class Meta:
        verbose_name = _("bibliographic type translation")
        verbose_name_plural = _("bibliographic types translations")

    bibliographic_type = models.ForeignKey(BibliographicType)
    language = models.CharField(_('language'), max_length=255, choices=LANGUAGES_CHOICES, default="pt-br")
    title = models.CharField(_("title"), max_length=255)

    def __unicode__(self):
        return unicode(self.title)    

class TypeSubmission(Generic):

    TYPE_CHOICES = (
        ('revista', _('Revista')),
        ('monografia', _('Monografia')),
        ('express', _('LILACS Express')),
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

    @models.permalink
    def get_absolute_url(self):
        return ('submission.views.show', [str(self.id)])

    def iso_title(self):
        return os.path.basename(self.iso_file.name)

    # Function that remove spaces and special characters from filenames
    def iso_filename(instance, filename):
        
        user = get_current_user()
        request = get_current_request()
        fname, dot, extension = filename.rpartition('.')
        extension = "iso"

        try:
            submissions = Submission.objects.all().order_by('-id')
            id = submissions[0].id
        except:
            id = 1

        dir = settings.MEDIA_ROOT
        dir = os.path.join(dir, unicode(user.get_profile().center.code))
        fname = "%s-%s" % (user.get_profile().center.code, id)
        
        return os.path.join(dir, '%s.%s' % (fname, extension))

    # Function that remove spaces and special characters from filenames
    def file_filename(instance, filename):
        
        user = get_current_user()
        request = get_current_request()
        fname, dot, extension = filename.rpartition('.')

        dir = settings.MEDIA_ROOT
        dir = os.path.join(dir, unicode(user.get_profile().center.code))
        fname = slugify(fname)
        
        return os.path.join(dir, '%s.%s' % (fname, extension))
        
    
    # iso    
    bibliographic_type = models.ForeignKey(BibliographicType, null=True, verbose_name=_("bibliographic type"))
    total_records = models.CharField(_("total of records"), max_length=255, blank=True, null=True, default=0)
    certified = models.CharField(_("total of certified records"), max_length=255, blank=True, null=True, default=0)
    iso_file = models.FileField(_('iso file'), max_length=510, upload_to=iso_filename, blank=True, null=True)
    lildbi_version = models.ForeignKey('LildbiVersion', null=True, blank=True)
    observation = models.TextField(_('Observation'), null=True, blank=True)
    file = models.FileField(_('attachment'), max_length=510, upload_to=file_filename, blank=True, null=True)
    external = models.ForeignKey(ExternalDatabase, null=True, blank=True, verbose_name=_('External Database'))

    def get_iso_url(self):

        current_site = Site.objects.get_current()
        domain = current_site.domain
        
        filename = self.iso_file.name
        url = filename.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
        url = "http://%s/%s" % (domain, url)
        
        if not os.path.exists(filename):
            logger_logins = logging.getLogger('logview.userlogins')
            logger_logins.error('File %s do not exists.', url)

        return unicode(url)

    def get_attac_url(self):

        filename = self.file.name
        url = filename.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)
        
        if not os.path.exists(filename):
            logger_logins = logging.getLogger('logview.userlogins')
            logger_logins.error('File %s do not exists.', url)

        return unicode(url)

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