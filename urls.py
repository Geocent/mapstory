from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from staticfiles.urls import staticfiles_urlpatterns
from geonode.sitemap import LayerSitemap, MapSitemap
from geonode.proxy.urls import urlpatterns as proxy_urlpatterns
from mapstory.models import *
from mapstory.forms import ProfileForm
from hitcount.views import update_hit_count_ajax

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

js_info_dict = {
    'domain': 'djangojs',
    'packages': ('geonode',)
}

sitemaps = {
    "layer": LayerSitemap,
    "map": MapSitemap
}
    

urlpatterns = patterns('',
    # inject our form into these views
    ('^profiles/edit', 'profiles.views.edit_profile', {'form_class': ProfileForm,}),
    ('^profiles/create', 'profiles.views.create_profile', {'form_class': ProfileForm,}),
)

urlpatterns += patterns('mapstory.views',
    (r'^(?:index/?)?$', 'index'),

    (r'', include('geonode.simplesearch.urls')), # put this first to ensure search urls priority
    (r'', include('geonode.urls')),
    (r'^data/create_annotations_layer/(?P<mapid>\d+)$','create_annotations_layer'),
    url(r'^mapstory/donate$',direct_to_template, {"template":"mapstory/donate.html"},name='donate'),
    url(r'^mapstory/thanks$',direct_to_template, {"template":"mapstory/thanks.html"}),
    url(r'^mapstory/alerts$','alerts',name='alerts'),
    url(r'^mapstory/tile/(?P<mapid>\d+)$','map_tile',name='map_tile'),
    url(r'^mapstory/tiles$','map_tiles',name='map_tiles'),
    url(r'^mapstory/storyteller/(?P<username>\S+)$','about_storyteller',name='about_storyteller'),
    url(r'^mapstory/section/(?P<section>[-\w]+)$','section_detail',name='section_detail'),
    url(r'^mapstory/resource/(?P<resource>[-\w]+)$','resource_detail',name='mapstory_resource'),
    url(r'^mapstory/how-to$','how_to',name='how_to'),
    
    # semi-temp urls
    url(r'^mapstory/topics/(?P<layer_or_map>\w+)/(?P<layer_or_map_id>\d+)$','topics_api',name='topics_api'),
    url(r'^mapstory/comment/(?P<layer_or_map_id>\d+)/(?P<comment_id>\d+)$','delete_story_comment',name='delete_story_comment'),
    url(r'^favorite/map/(?P<id>\d+)$','favorite',{'layer_or_map':'map'}, name='add_favorite_map'),
    url(r'^favorite/layer/(?P<id>\d+)$','favorite',{'layer_or_map':'layer'}, name='add_favorite_layer'),
    url(r'^favorite/(?P<id>\d+)/delete$','delete_favorite',name='delete_favorite'),
    url(r'^mapstory/publish/(?P<layer_or_map>\w+)/(?P<layer_or_map_id>\d+)$','publish_status',name='publish_status'),
    url(r'^mapstory/add-to-map/(?P<id>\d+)/(?P<typename>[:\w]+)','add_to_map',name='add_to_map'),
    url(r'^search/favoriteslinks$','favoriteslinks',name='favoriteslinks'),
    url(r'^search/favoriteslist$','favoriteslist',name='favoriteslist'),

    url(r'^ajax/hitcount/$', update_hit_count_ajax, name='hitcount_update_ajax'),

    # for now, direct-to-template but should be in database
    url(r"^mapstory/thoughts/jonathan-marino", direct_to_template, {"template": "mapstory/thoughts.html",
        "extra_context" : {'html':'mapstory/thoughts/jm.html'}}, name="thoughts-jm"),
    url(r"^mapstory/thoughts/parag-khanna", direct_to_template, {"template": "mapstory/thoughts.html",
        "extra_context" : {'html':'mapstory/thoughts/pk.html'}}, name="thoughts-pk"),
    url(r"^mapstory/thoughts/roberta-balstad", direct_to_template, {"template": "mapstory/thoughts.html",
        "extra_context" : {'html':'mapstory/thoughts/rb.html'}}, name="thoughts-rb"),
    url(r"^mapstory/thoughts/r-siva-kumar", direct_to_template, {"template": "mapstory/thoughts.html",
        "extra_context" : {'html':'mapstory/thoughts/sk.html'}}, name="thoughts-sk"),

    # ugh, overrides
    url(r'^(?P<layername>[^/]*)/metadata$', 'layer_metadata', name="layer_metadata"),
)

urlpatterns += proxy_urlpatterns

# Extra static file endpoint for development use
if settings.SERVE_MEDIA:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^thumbs/(?P<path>.*)$','django.views.static.serve',{
            'document_root' : settings.THUMBNAIL_STORAGE,
        })
    )
    urlpatterns += staticfiles_urlpatterns()
    
