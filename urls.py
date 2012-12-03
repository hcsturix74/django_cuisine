from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()
from django.views.generic import *

urlpatterns = patterns('',
    # Examples:
    url(r'^$', TemplateView.as_view(
        template_name='cookbook/homepage.html'),
        name='homepage'
    ),
    url(r'^login/$', TemplateView.as_view(
        template_name='cookbook/login.html'),
        name='login'
    ),
    #url(r'^django_cuisine/', include('django_cuisine.urls')),
    url('^', include('cookbook.urls', namespace='cookbook_list')),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        #    url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views.serve'),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT } ),
    )
    urlpatterns += staticfiles_urlpatterns()
#STATIC MEDIA SERVER
urlpatterns += patterns('',
    #    url(r'^static/(?P<path>.*)$', 'django.contrib.staticfiles.views.serve'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
        })
)

if 'social_auth' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        url(r'', include('social_auth.urls')),
    )
