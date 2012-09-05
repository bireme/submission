#! coding: utf-8
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from django.template import RequestContext
from django.conf import settings
from django.http import Http404
from models import *
from forms import *

@login_required
def index(request):
    
    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'

    output = {}
    submissions = Submission.objects.all().order_by('updated').exclude(current_status__finish=True).exclude(current_status__close=True)
    filters = Step.objects.all().exclude(finish=True).exclude(close=True)

    if 'admins' in user_groups: user_type = 'admin'
    if user_type == 'user': submissions = submissions.filter(creator=request.user)

    # submission actions
    if request.POST:
        if 'action' in request.POST and request.POST['action'] != "":
            action = request.POST['action']
            ids = request.POST.getlist('submissions')
            if action == 'approve':
                for item in ids:
                    item = Submission.objects.get(pk=item)
                    status = item.current_status
                    next = Step.objects.filter(parent=status)
                    if next:
                        item.current_status = next[0]
                        item.save()
            if action == 'decline':
                for item in ids:
                    item = Submission.objects.get(pk=item)
                    close = Step.objects.get(close=True)
                    item.current_status = close
                    item.save()
    
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
            submissions = submissions.filter(current_status=filtr)
        
        if 'page' in request.REQUEST and request.REQUEST['page'] != "":
            page = request.REQUEST['page']

    submissions = submissions.order_by("%s%s" % (order_type, order_by))

    # pagination
    pagination = {}
    paginator = Paginator(submissions, settings.ITEMS_PER_PAGE)
    pagination['paginator'] = paginator
    pagination['page'] = paginator.page(page)
    submissions = pagination['page'].object_list

    headers = (
        ('id', '#'),
        ('creator', 'Created by'),
        ('updated', "Last Update"),
        ('current_status', "Status"),        
    )
            
    output['headers'] = headers
    output['submissions'] = submissions
    output['order_by'] = order_by
    output['order_type'] = order_type
    output['filters'] = filters
    output['filtr'] = filtr
    output['pagination'] = pagination

    return render_to_response('submission/index.html', output, context_instance=RequestContext(request))
        

@login_required
def create(request, type=None):
    types = Type.objects.all()
    form = SubmissionForm()
    success = False

    output = {
        'types': types,
        'form': form,
        'success': success,
    }
    
    if type:
        type = get_object_or_404(Type, pk=type)
        submission = Submission(type=type)
        status = Step.objects.filter(type=type)

        if type.title.lower() == 'iso':
            form = SubmissionIsoForm(instance=submission)

        if request.POST:
            submission.creator = request.user
            submission.updater = request.user
            submission.current_status = status.filter(parent=None)[0]
            submission.save()

            type_submission = TypeSubmission(submission=submission)
            form = SubmissionIsoForm(request.POST, request.FILES, instance=type_submission)

            if form.is_valid():
                submission.save()
                form.save()

                message = "ISO registrada com sucesso!"
                type = 'success'
                return redirect(reverse("submission.views.index") + "?message=%s&type=%s" % (message, type))

        output = {
            'type': type,
            'form': form,
        }

        return render_to_response('submission/create-%s.html' % type.title.lower(), output, context_instance=RequestContext(request))        
    
    return render_to_response('submission/create.html', output, context_instance=RequestContext(request))

@login_required
def exclude(request, id):
    return

@login_required
def show(request, id):

    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'
    finish = False
    if 'admins' in user_groups:
        user_type = 'admin'

    submission = get_object_or_404(Submission, pk=id)
    type_submission = TypeSubmission.objects.get(submission=submission)

    if user_type != 'admin' and submission.creator != request.user:
        return Http404

    metadata = None
    followup_form = FollowUpForm()
    followups = FollowUp.objects.filter(submission=id).order_by('created')
    steps = Step.objects.filter(type=submission.type)
    pending = steps.filter(pending=True)[0]
    close = steps.filter(close=True)[0]
    next_step = steps.filter(parent=submission.current_status)
    is_pre_finish = False
    if next_step and next_step[0].finish: is_pre_finish = True

    print next_step
    
    if not next_step:
        if submission.current_status.finish:
            finish = True

        # ele tá em pending
        else:
            followup = FollowUp.objects.filter(submission=submission).order_by('-id')[0]

            if followup.current_status == pending:
                next_step = [followup.previous_status]
    
    output = {
        'is_pre_finish': is_pre_finish,
        'user_type': user_type,
        'submission': submission,
        'followups': followups,
        'next_step': next_step,
        'pending': pending,
        'is_finish': finish,
        'close': close,
        'followup_form': followup_form,
        'type_submission': type_submission,
    }

    return render_to_response('submission/show.html', output, context_instance=RequestContext(request))

@login_required
def change_status(request, id):

    submission = get_object_or_404(Submission, pk=id)

    if request.POST:
        next = request.POST['next']
        status = get_object_or_404(Step, pk=int(request.POST['action']))

        followup = FollowUp()
        followup.creator = request.user
        followup.submission = submission
        followup.previous_status = submission.current_status
        followup.current_status = status
    
        form = FollowUpForm(request.POST, request.FILES, instance=followup)

        if form.is_valid:
            form.save()
        else:
            pass

        submission.current_status = status
        submission.save()

    return redirect(next)

@login_required
def edit_type_submission(request, id):

    type_submission = get_object_or_404(TypeSubmission, pk=id)
    form = SubmissionIsoFinalForm(instance=type_submission)

    if request.POST:
        form = SubmissionIsoFinalForm(request.POST, instance=type_submission)
        if form.is_valid():
            form.save()
            return redirect(reverse('submission.views.show', args=[type_submission.submission.id]))

    output = {
        'form': form,
        'type_submission': type_submission,
    }

    return render_to_response('submission/edit-type-submission.html', output, context_instance=RequestContext(request))

@login_required
def list(request, type=0, filtr=0):
    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'
    if 'admins' in user_groups:
        user_type = 'admin'

    submissions = Submission.objects.all().order_by('updated')
    if not user_type == 'admin':
        submissions = submissions.filter(creator=request.user)

    filters = Step.objects.all()
    types = Type.objects.all()

    if int(type) > 0:
        type = get_object_or_404(Type, pk=type)
        submissions = submissions.filter(type=type)
        filters = filters.filter(type=type) 
        type = type.id
    
    if int(filtr) > 0:
        filtr = get_object_or_404(Step, pk=filtr)
        submissions = submissions.filter(current_status=filtr)
        filtr = filtr.id

    output = {
        'submissions': submissions,
        'filters': filters,
        'filtr': filtr,
        'types': types,
        'type': type,
    }

    return render_to_response('submission/list.html', output, context_instance=RequestContext(request))