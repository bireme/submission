from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
from registration.forms import *
from django.http import Http404



@login_required
def register(request, success_url=None,
             form_class=RegistrationForm, profile_callback=None,
             template_name='registration/registration_form.html',
             extra_context=None):
    
    if not (request.user.get_profile().is_admin or request.user.get_profile().is_admin):
        raise Http404

    if request.method == 'POST':
        form = form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_user = form.save(profile_callback=profile_callback)
            
            return HttpResponseRedirect(reverse('registration.views.list'))
    else:
        form = form_class()
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)

@login_required
def list(request):
    output = {}
    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'

    if not user.get_profile().is_admin:
        raise Http404

    users = User.objects.filter(userprofile__center=request.user.get_profile().center).filter(is_active=True)
    users = users.exclude(id=request.user.id)

    output['users'] = users

    return render_to_response('registration/list.html', output, context_instance=RequestContext(request))

@login_required
def remove(request, id):

    output = {}
    user = request.user
    user_groups = [group.name for group in user.groups.all()]
    user_type = 'user'

    if not user.get_profile().is_admin:
        raise Http404

    user = User.objects.get(pk=id)
    user.is_active = False
    user.save()

    return HttpResponseRedirect(reverse('registration.views.list'))

@login_required
def edit(request):
    output = {}
    user = request.user

    form = EditUserForm(instance=user)
    if request.POST:
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            print form.save()

    output['form'] = form
    
    return render_to_response('registration/edit.html', output, context_instance=RequestContext(request))