from datetime import datetime

from django.template.context import RequestContext
from django.views.generic import list_detail
from django.shortcuts import render

from journal.models import Entry, Section


def index(request):
    entries = Entry.objects.get_published()[:5]
    try:
        from photologue.models import Gallery
        galleries = Gallery.objects.all()[:3]
    except:
        pass
    return render(request, 'journal/index.html', locals(),
                  context_instance=RequestContext(request))


def view_section(request, slug, page=1):
    section = Section.objects.get(slug__exact=slug)
    entries = section.entries.filter(publish=True, pub_date__lte=datetime.now())
    try:
        from photologue.models import Gallery
        galleries = Gallery.objects.all()[:3]
    except:
        galleries = None
    return list_detail.object_list(request,
                                   queryset=entries,
                                   paginate_by=5,
                                   page=page,
                                   allow_empty=True,
                                   template_name='journal/view_section.html',
                                   extra_context={'section': section,
                                                  'galleries': Gallery.objects.all()[:3]})
