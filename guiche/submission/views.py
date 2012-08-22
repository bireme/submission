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

    output = {}
    submissions = Submission.objects.all().order_by('updated')
    filters = Step.objects.all()

    if 'admins' in user_groups:
        user_type = 'admin'
        
    if user_type == 'user':
        submissions = submissions.filter(creator=request.user)

    if 'opened_filter' in request.GET:
        filtr = Step.objects.get(pk=request.GET['opened_filter'])
        try:
            submissions = submissions.filter(current_status=filtr)
        except:
            pass
            
    output['submissions'] = submissions
    output['filters'] = filters

    if user_type == 'admin':
        return render_to_response('submission/index-admin.html', output, context_instance=RequestContext(request))

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
def show_submission(request, id):

    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'
    if 'admins' in user_groups:
        user_type = 'admin'

    submission = get_object_or_404(Submission, pk=id)

    if user_type != 'admin' and submission.creator != request.user:
        return Http404

    followups = FollowUp.objects.filter(submission=id)
    next_step = Step.objects.filter(parent=submission.current_status)

    output = {
        'user_type': user_type,
        'submission': submission,
        'followups': followups,
        'next_step': next_step,
    }

    return render_to_response('submission/show.html', output, context_instance=RequestContext(request))