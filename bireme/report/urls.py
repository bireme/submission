from django.conf.urls.defaults import patterns

urlpatterns = patterns('',
    
    (r'^$', 'report.views.search'),
    (r'^index-all/?$', 'report.views.index_all'),
)

