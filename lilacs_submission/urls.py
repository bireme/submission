from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lilacs_submission.views.home', name='home'),
    # url(r'^lilacs_submission/', include('lilacs_submission.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/?$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/?$', 'django.contrib.auth.views.logout'),
    
    (r'^/?$', 'submission.views.index'),
    # (r'^submission/edit/(?P<id>\d+)/?$', 'submission.views.edit'),
    # (r'^submission/exclude/(?P<id>\d+)/?$', 'submission.views.exclude'),
    # (r'^submission/approve/(?P<id>\d+)/?$', 'submission.views.approve'),
    (r'^submission/new/?$', 'submission.views.create'),
    (r'^submission/new/(?P<type>\d+)/?$', 'submission.views.create'),
    (r'^submission/show/(?P<id>\d+)/?$', 'submission.views.show'),
    (r'^submission/edit-type/(?P<id>\d+)/?$', 'submission.views.edit_type_submission'),
    (r'^submission/change_status/(?P<id>\d+)/?$', 'submission.views.change_status'),
    (r'^submission/list/?$', 'submission.views.list'),
    (r'^submission/list/(?P<type>\d+)/?$', 'submission.views.list'),
    (r'^submission/list/(?P<type>\d+)/(?P<filtr>\d+)/?$', 'submission.views.list'),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
