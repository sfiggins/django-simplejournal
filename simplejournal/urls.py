from django.conf.urls.defaults import *
from simplejournal.models import Entry

urlpatterns = patterns('journal.views',
    url(r'^$', 'index', name="journal-index"),
    url(r'^section/(?P<slug>[\-\d\w]+)/$', 'view_section', name="journal-section"),
    url(r'^section/(?P<slug>[\-\d\w]+)/page/(?P<page>[0-9]+)/$', 'view_section', name="journal-section-page")
)

# journal entries
entry_args = {'date_field': 'pub_date', 'allow_empty': True, 'queryset': Entry.objects.get_published()}
urlpatterns 
urlpatterns += patterns('django.views.generic.date_based',
    url(r'^entry/(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[\-\d\w]+)/$',
        'object_detail', {'date_field': 'pub_date', 'slug_field': 'slug', 
        'queryset': Entry.objects.all()}, name='journal-article-detail'),
)
