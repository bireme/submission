#! coding: utf-8
from django_tools.middlewares.ThreadLocal import get_current_user, get_current_request
from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string
from django.template import RequestContext
from django.core.mail import EmailMessage
from django.db.models import signals
from django.conf import settings
from datetime import datetime
from models import *
import logging
import models

def send_email(sender, instance, created, **kwargs):

    followup = instance
    user = instance.submission.creator
    request = get_current_request()
    submission = models.TypeSubmission.objects.get(submission=followup.submission)
    url = submission.get_absolute_url()
    try:
        profile = user.get_profile() 
    except:
        profile = None

    output = {
        'url': url,
        'previous_status': followup.previous_status,
        'current_status': followup.current_status,
    }

    if followup.message:
        output['message'] = followup.message


    EMAIL_SUBJECT = u"[BIREME Submission] %s" % _("Update in submission #%s" % followup.submission.id)
    EMAIL_CONTENT = render_to_string('email/send_submission_body.html', output, context_instance=RequestContext(request))

    if profile and profile.receive_email:
        if user.email:
            try:
                msg = EmailMessage(EMAIL_SUBJECT, EMAIL_CONTENT, settings.EMAIL_FROM, [user.email])
                msg.content_subtype = "html"
                msg.send()
            except Exception as e:
                logger_logins = logging.getLogger('logview.userlogins')
                logger_logins.error(e)



def send_to_external(sender, instance, created, **kwargs):
    
    request = get_current_request()
    
    if created:
        print instance.iso_file
        if instance.external:
            external = instance.external

            output = {
                'url': instance.get_iso_url(),
                'date': instance.created,
                'message': instance.txt_external,
                'external': external,
            }

            EMAIL_SUBJECT = u"[BIREME Submission] %s" % _("New Submission")
            EMAIL_CONTENT = render_to_string('email/send-to-external-database.html', output, context_instance=RequestContext(request))

            if external.email:

                try:
                    msg = EmailMessage(EMAIL_SUBJECT, EMAIL_CONTENT, settings.EMAIL_FROM, [external.email])
                    msg.content_subtype = "html"
                    msg.send()
                except Exception as e:
                    logger_logins = logging.getLogger('logview.userlogins')
                    logger_logins.error(e)

signals.post_save.connect(send_email, sender=FollowUp, dispatch_uid="some.unique.string.id")
signals.post_save.connect(send_to_external, sender=TypeSubmission, dispatch_uid="some.unique.string.id")