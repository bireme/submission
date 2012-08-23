#! coding: utf-8
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import Group
from django.http import Http404
from models import *
from forms import *

@login_required
def index(request):
    
    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'
    filtr = False

    output = {}
    submissions = Submission.objects.all().order_by('updated').exclude(current_status__finish=True)
    filters = Step.objects.all().exclude(finish=True)

    if 'admins' in user_groups:
        user_type = 'admin'
        
    if user_type == 'user':
        submissions = submissions.filter(creator=request.user)

    if 'opened_filter' in request.GET:
        try:
            filtr = Step.objects.get(pk=request.GET['opened_filter'])
            submissions = submissions.filter(current_status=filtr)
        except:
            pass
            
    output['submissions'] = submissions
    output['filters'] = filters
    output['filtr'] = filtr

    return render_to_response('submission/index.html', output, context_instance=RequestContext(request))
        

@login_required
def create(request):
    types = Type.objects.all()
    form = SubmissionForm()
    success = False

    if request.POST:        

        status = Step.objects.filter(type=request.POST['type']).filter(parent=None)[0]
        submission = Submission(current_status=status)
        submission.creator = request.user
        submission.updater = request.user

        form = SubmissionForm(request.POST, request.FILES, instance=submission)
        if form.is_valid():
            form.save()  
            success = True      
        else:
            print form.errors
        
    
    output = {
        'types': types,
        'form': form,
        'success': success,
    }
    return render_to_response('submission/create.html', output, context_instance=RequestContext(request))

@login_required
def exclude(request, id):
    return

@login_required
def edit(request, id):
    
    submission = Submission.objects.get(id=id)
    form = SubmissionForm(instance=submission)

    if request.POST:
        
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():            
            form.save()

    output = {
        'form': form,
        'edited': True,
        'id': id,
    }

    return render_to_response('submission/create.html', output, context_instance=RequestContext(request))

@login_required
def approve(request, id):

    next = reverse("submission.views.index")
    if 'next' in request.GET:
        next = request.GET['next']

    if request.POST:

        submission = get_object_or_404(Submission, pk=id)

        message = SubmissionHistory(submission=submission)
        message.obs = request.POST['obs']
        message.status = request.POST['status']
        message.creator = request.user
        message.save()

        submission.status = request.POST['status']
        submission.updater = request.user
        submission.save()

    return redirect(next)

@login_required
def show(request, id):

    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'
    finish = False
    if 'admins' in user_groups:
        user_type = 'admin'

    submission = get_object_or_404(Submission, pk=id)

    if user_type != 'admin' and submission.creator != request.user:
        return Http404

    followups = FollowUp.objects.filter(submission=id)
    steps = Step.objects.filter(type=submission.type)
    pending = steps.filter(pending=True)[0]
    next_step = steps.filter(parent=submission.current_status)
    
    if not next_step:
        if submission.current_status.finish:
            finish = True
        # ele tá em pending
        else:
            followup = FollowUp.objects.filter(submission=submission).order_by('-created')[0]
            next_step = [followup.current_status]
    
    output = {
        'user_type': user_type,
        'submission': submission,
        'followups': followups,
        'next_step': next_step,
        'pending': pending,
        'is_finish': finish,
    }

    return render_to_response('submission/show.html', output, context_instance=RequestContext(request))

@login_required
def change_status(request, id):

    submission = get_object_or_404(Submission, pk=id)

    if request.POST:
        next = request.POST['next']
        status = get_object_or_404(Step, pk=int(request.POST['action']))
        obs = request.POST['obs']

        followup = FollowUp()
        followup.submission = submission
        followup.previous_status = submission.current_status
        followup.current_status = status
        followup.message = obs
        followup.save()

        submission.current_status = status
        submission.save()

    return redirect(next)

@login_required
def list(request, type=0, filtr=0):
    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'
    if 'admins' in user_groups:
        user_type = 'admin'

    submissions = Submission.objects.all().order_by('updated')
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