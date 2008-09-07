from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from datetime import datetime

JOURNAL_DIR='journal'

# Create your models here.
class Image(models.Model):
    "A scanned image or photograph"
    image = models.ImageField(upload_to=JOURNAL_DIR+"/images/%Y/%m/%d")
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(max_length=80)
    slug=models.SlugField(unique_for_date='pub_date', help_text='A "Slug" is a unique URL-friendly title for an object.')
    caption = models.TextField(blank=True, null=True)
    artist = models.CharField(max_length=100, blank=True)
    journal_entry = models.ForeignKey('Entry')
    
    def __unicode__(self):
        return self.title


class Author(models.Model):
    salutation = models.CharField(max_length=10, null=True, blank=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=40)
    email = models.EmailField(null=True)
    bio = models.TextField(null=True)
    headshot = models.ImageField(upload_to=JOURNAL_DIR+"/authors",null=True,blank=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)


class EntryManager(models.Manager):
    def get_published(self):
        return self.filter(publish=True, pub_date__lte=datetime.now)
    def get_drafts(self):
        return self.filter(publish=False)

class Entry(models.Model):
    """ A journal entry """
    title = models.CharField(max_length = 100)
    slug = models.SlugField(unique_for_date='pub_date', 
                            help_text='A "Slug" is a unique URL-friendly title for an object.')
    summary = models.TextField(help_text="A single paragraph summary or preview of the article.")
    body = models.TextField("Body text")
    author = models.ForeignKey(Author)
    publish = models.BooleanField(default=False)
    pub_date = models.DateTimeField(default=datetime.now)
    sections = models.ManyToManyField('Section', related_name='entries')


    # custom entry manager
    objects = EntryManager()
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return "/journal/entry/%s/%s/" % (self.pub_date.strftime("%Y/%b/%d").lower(), self.slug)

    def get_image_set(self):
        try:
            image_set = Image.objects.filter(journal_entry=self.id)
        except:
            pass
        return image_set

    def get_document_set(self):
        try:
            document_set = Document.objects.filter(journal_entry=self.id)
        except:
            pass
        return document_set


    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'
        verbose_name_plural="Entries"

        
class Document(models.Model):
    file = models.FileField("Document", upload_to=JOURNAL_DIR+"/documents/%Y/%b/%d")
    pub_date = models.DateTimeField("Date published", default=datetime.now)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique_for_date='pub_date')
    summary = models.TextField()
    journal_entry = models.ForeignKey('Entry')

    class Meta:
        ordering = ['-pub_date']
        get_latest_by = 'pub_date'

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        args = self.pub_date.strftime("%Y/%b/%d").lower().split("/") + [self.slug]
        return reverse('pr-document-detail', args=args)

    def doc_dir(self):
        return os.path.dirname(self.get_file_filename())

    def remove_dirs(self):
        if os.path.isdir(self.doc_dir()):
            if os.listdir(self.doc_dir()) == []:
                os.removedirs(self.doc_dir())

    def delete(self):
        super(Document, self).delete()
        self.remove_dirs()
       

class Section(models.Model):
    title = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['title']

    class Admin:
        list_display = ('title',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pr-section', args=[self.slug])
        
