from django.contrib import admin
from simplejournal.models import Image, Author, Entry, Document, Section

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'pub_date', 'image')
    prepopulated_fields = {"slug": ("title",)}

class AuthorAdmin(admin.ModelAdmin):
    pass

class EntryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'pub_date',)
    search_fields = ('title', 'body',)
    date_hierarchy = 'pub_date'
    prepopulated_fields = {"slug": ("title",)}

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date')
    list_filter = ['pub_date']
    prepopulated_fields = {"slug": ("title",)}

class SectionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Image, ImageAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Section, SectionAdmin)
