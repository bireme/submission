from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    (r'^accounts/login/?$', 'django.contrib.auth.views.login'),
    (r'^accounts/logout/?$', 'django.contrib.auth.views.logout'),

    # internationalization
    url(r'^i18n/', include('django.conf.urls.i18n')),

    (r'^/?$', 'submission.views.index'),
    (r'^submission/new/?$', 'submission.views.create'),
    (r'^submission/new/(?P<type>\d+)/?$', 'submission.views.create'),
    (r'^submission/show/(?P<id>\d+)/?$', 'submission.views.show'),
    (r'^submission/edit-type/(?P<id>\d+)/?$', 'submission.views.edit_type_submission'),
    (r'^submission/change_status/(?P<id>\d+)/?$', 'submission.views.change_status'),
    (r'^submission/list/?$', 'submission.views.list'),
    (r'^submission/list/(?P<type>\d+)/?$', 'submission.views.list'),
    (r'^submission/list/(?P<type>\d+)/(?P<filtr>\d+)/?$', 'submission.views.list'),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'^rosetta/', include('rosetta.urls')),
    )

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
