from django.shortcuts import render_to_response
from django.template import RequestContext
from submission.views import HEADERS
from django.http import Http404
from submission.models import *
from django.db.models import Q

def search(request):
    output = {}

    if not 'q' in request.GET:
        raise Http404
    
    query = request.GET.get('q')
    output['q'] = query

    try:
        submissions = TypeSubmission.objects.filter(id=query)
    except:
        submissions = TypeSubmission.objects.filter(submission__creator__userprofile__center__code__icontains=query)

    # requests of interface
    order_by = 'id'
    order_type = ''
    filtr = ""
    page = 1
    if request.REQUEST:
        # interface
        if 'order_by' in request.REQUEST and request.REQUEST['order_by'] != "":
            order_by = request.REQUEST['order_by']
        
        if 'order_type' in request.REQUEST and request.REQUEST['order_type'] != "":
            order_type = request.REQUEST['order_type']

        if 'filter' in request.REQUEST and request.REQUEST['filter'] != "":
            filtr = request.REQUEST['filter']
            filtr = get_object_or_404(Step, pk=filtr)
            submissions = submissions.filter(submission__current_status=filtr)
        
        if 'page' in request.REQUEST and request.REQUEST['page'] != "":
            page = request.REQUEST['page']

    submissions = submissions.order_by("%s%s" % (order_type, order_by))
    
    output['headers'] = HEADERS
    output['order_by'] = order_by
    output['order_type'] = order_type
    output['filtr'] = filtr
    output['submissions'] = submissions

    return render_to_response('main/search.html', output, context_instance=RequestContext(request))
