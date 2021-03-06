from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from submission.views import HEADERS
from django.http import Http404, HttpResponse
from submission.models import *
from bireme.submission.views import HEADERS
from django.core.paginator import Paginator
from django.conf import settings

def search(request):
    
    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'
    submissions = TypeSubmission.objects.all().order_by('submission__updated')
    output = {}

    if not 'q' in request.GET:
        raise Http404

    if 'admins' in user_groups:
        user_type = 'admin'

    if user_type == 'user':
        profile = request.user.get_profile()
        submissions = submissions.filter(submission__creator__userprofile__center=profile.center)
    
    query = request.GET.get('q')
    output['q'] = query
    filters = Step.objects.all()
    filters_type = BibliographicType.objects.all()

    try:
        submissions = submissions.filter(submission__id=query)
    except:
        submissions = submissions.filter(submission__creator__userprofile__center__code__icontains=query)

    # requests of interface
    order_by = 'id'
    order_type = ''
    filtr = ""
    page = 1
    filtr_type = ""
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

        if 'filtr_type' in request.REQUEST and request.REQUEST['filtr_type'] != "":
            filtr_type = int(request.REQUEST['filtr_type'])
            submissions = submissions.filter(bibliographic_type=filtr_type)

        if 'page' in request.REQUEST and request.REQUEST['page'] != "":
            page = request.REQUEST['page']

    submissions = submissions.order_by("%s%s" % (order_type, order_by))
    total = len(submissions)

    # pagination
    pagination = {}
    paginator = Paginator(submissions, settings.ITEMS_PER_PAGE)
    pagination['paginator'] = paginator
    pagination['page'] = paginator.page(page)
    submissions = pagination['page'].object_list
    
    output['headers'] = HEADERS
    output['submissions'] = submissions
    output['order_by'] = order_by
    output['order_type'] = order_type
    output['filters'] = filters
    output['filtr'] = filtr
    output['filters_type'] = filters_type
    output['filtr_type'] = filtr_type
    output['pagination'] = pagination
    output['total'] = total

    return render_to_response('main/search.html', output, context_instance=RequestContext(request))


def cookie_lang(request):

    language = request.REQUEST.get('language')
    request.COOKIES[settings.LANGUAGE_COOKIE_NAME] = language
    request.session[settings.LANGUAGE_COOKIE_NAME] = language

    response = HttpResponse(language)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)

    return response
