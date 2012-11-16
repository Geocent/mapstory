from mapstory.models import *
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

class ResourceForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Resource
        
class ResourceAdmin(admin.ModelAdmin):
    list_display = 'id','name','order'
    list_display_links = 'id',
    list_editable = 'name','order'
    form = ResourceForm
    ordering = ['order',]

class SectionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Section

class SectionAdmin(admin.ModelAdmin):
    list_display = 'id','name','order'
    list_display_links = 'id',
    list_editable = 'name','order'
    form = SectionForm
    ordering = ['order',]
    
class VideoLinkForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = VideoLink

class VideoLinkAdmin(admin.ModelAdmin):
    list_display = 'id','name','title','href','publish','location'
    list_display_links = 'id',
    list_editable = 'name','title','publish','href','location'
    form = VideoLinkForm
    
class ContactDetailAdmin(admin.ModelAdmin):
    pass

class OrgAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            self.fields = ('organization',)
        else:
            self.fields = None
        return super(OrgAdmin, self).get_form(request, obj, **kwargs)

class OrgContentAdmin(admin.ModelAdmin):
    pass

admin.site.register(VideoLink, VideoLinkAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(ContactDetail, ContactDetailAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Org, OrgAdmin)
admin.site.register(OrgContent, OrgContentAdmin)
admin.site.register(Topic)