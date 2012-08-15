from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.conf import settings
import os

TYPE_CHOICES = (
    ('iso', "ISO File"),
    ('oai', "OAI PMH"),
)

STATUS_CHOICES = (
    ('a', 'approved'),
    ('p', 'pending'),
    ('d', 'declined'),
)

class Submission(models.Model):

    class Meta:
        verbose_name = "submission"
        verbose_name_plural = "submissions"

    created = models.DateTimeField("created", default=datetime.now())
    updated = models.DateTimeField("updated", default=datetime.now())
    creator = models.ForeignKey(User, null=True, blank=True, related_name="+")
    updater = models.ForeignKey(User, null=True, blank=True, related_name="+")

    type = models.CharField('type', max_length=255, choices=TYPE_CHOICES)
    status = models.CharField('status', max_length=1, choices=STATUS_CHOICES, default='p')
    file = models.FileField("file", null=True, blank=True, upload_to=os.path.join(settings.MEDIA_ROOT, 'files'))
    oai_link = models.URLField("OAI-PMH link", null=True, blank=True)

    def __unicode__(self):
        return unicode(self.type)

    # rewrite to update the last modification's time
    def save(self):
        self.updated = datetime.now()
        super(Submission, self).save()