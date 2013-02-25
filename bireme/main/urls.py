from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    (r'^search/?$', 'main.views.search'),
	(r'^cookie-lang/?$', 'main.views.cookie_lang'),
    (r'^$', 'submission.views.index'),
)

