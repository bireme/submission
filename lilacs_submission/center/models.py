from django.db import models

class Center(models.Model):

    class Meta:
        verbose_name = "Center"
        verbose_name_plural = "Centers"

    name = models.CharField('name', max_length=255)
    code = models.CharField('code', max_length=255)

    def __unicode__(self):
        return unicode(self.code)
