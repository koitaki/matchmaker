from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.urls')),
	url(r'^$', 'profiles.views.all', name='all'),
    url(r'^members/(?P<username>\w+)/$', 'profiles.views.single_user', name='single_user'),
	url(r'^edit/$', 'profiles.views.edit_profile', name='edit_profile'),
	url(r'^edit/jobs$', 'profiles.views.edit_jobs'),
	url(r'^edit/locations$', 'profiles.views.edit_locations'),
	url(r'^questions/$', 'questions.views.all_questions', name='questions'),
)
