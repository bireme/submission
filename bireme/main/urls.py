from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
	(r'^search/?$', 'main.views.search'),
    (r'^$', 'submission.views.index'),
)

