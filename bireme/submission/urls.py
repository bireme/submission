from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
	(r'^new/?$', 'submission.views.create'),
    (r'^new/(?P<type>\d+)/?$', 'submission.views.create'),
    (r'^show/(?P<id>\d+)/?$', 'submission.views.show'),
    (r'^edit-type/(?P<id>\d+)/?$', 'submission.views.edit_type_submission'),
    (r'^edit-followup/(?P<id>\d+)/?$', 'submission.views.edit_followup'),
    (r'^change_status/(?P<id>\d+)/?$', 'submission.views.change_status'),
    (r'^list/?$', 'submission.views.list'),
    (r'^bulk/?$', 'submission.views.bulk'),    
)

