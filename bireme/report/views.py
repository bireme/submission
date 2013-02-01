#! coding: utf-8
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.template import RequestContext
from index import search as whoosh_search
from django.conf import settings
from index import WHOOSH_SCHEMA
from datetime import datetime
from submission.models import *
import mimetypes
import os

@login_required
def search(request):

    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'

    if not 'admins' in user_groups:
        return Http404

    fields = [item for item in WHOOSH_SCHEMA.names()]
    checked_fields = [field for field in request.GET.getlist('fields')]

    if not checked_fields:
        checked_fields = ['id', 'center', 'current_status']

    if request.GET.getlist('fields_search'):
        fields_search = [field for field in request.GET.getlist('fields_search')]

    order_by = "id"
    if request.GET.get('order_by'):
        order_by = request.GET.get('order_by')


    results = None
    if request.GET.get('q'):
        query = request.GET.get('q')
        results = whoosh_search(query, sortedby=order_by)

    output = {
        'results': results,
        'fields': fields,
        'checked_fields': checked_fields,
    }

    if request.GET.get('output') == 'print':
        output['print'] = True
    
    if request.GET.get('output') == 'csv':
        return render_to_response('report/index.csv', output, context_instance=RequestContext(request), mimetype="application/csv")
    

    return render_to_response('report/index.html', output, context_instance=RequestContext(request))

def index_all(request):

    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'

    if not 'admins' in user_groups:
        return Http404

    for submission in TypeSubmission.objects.all():
        submission.save()

    return redirect(reverse("report.views.search"))

