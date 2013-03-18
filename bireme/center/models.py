from django.utils.translation import ugettext_lazy as _
from django.db import models

class Center(models.Model):

    class Meta:
        verbose_name = _("Center")
        verbose_name_plural = _("Centers")

    name = models.CharField('name', max_length=255)
    code = models.CharField('code', max_length=255)

    def __unicode__(self):
        return unicode(self.code)

class ExternalDatabase(models.Model):

    class Meta:
        verbose_name = _("External Database")
        verbose_name_plural = _("External Databases")

    name = models.CharField(_('name'), max_length=255)
    email = models.CharField(_("email"), max_length=255)
    center = models.ForeignKey(Center, blank=True, null=True)

    def __unicode__(self):
        if self.center:
            return unicode("%s - %s" % (self.center, self.name))
        return unicode(self.name)

