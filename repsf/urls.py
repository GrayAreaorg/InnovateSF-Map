from django.conf.urls import patterns, include, url
from emailusernames.forms import EmailAuthenticationForm
from repsf.accounts.forms import ISFAuthForm
from accounts import views
import settings
from moderation.helpers import auto_discover

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
auto_discover()

urlpatterns = patterns('',
    # Examples:
	
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'repsf.map.views.home', name='home'),
	url(r'^accounts/login/?$', 'django.contrib.auth.views.login', {'template_name':'login.html', 'authentication_form': ISFAuthForm}, name='login'),
	url(r'^accounts/create/?$', 'repsf.accounts.views.create', name='register'),
	url(r'^accounts/profile/?$', 'repsf.accounts.views.read', name='show_user'),
	url(r'^accounts/logout/?$', 'repsf.accounts.views.end_session', name='logout'),
	url(r'^locations/edit/(?P<id>\d+)/?$', 'repsf.map.views.update', name='update_location'),
	url(r'^locations/create/?$', 'repsf.map.views.create', name='create_location'),
	url(r'^embed/?$', 'repsf.map.views.home', {'embed': True}, name='embed'),
	url(r'^get_user/?$', 'repsf.accounts.views.is_logged_in', name='get_user'),
	url(r'^(?P<location>[a-zA-Z0-9 ._]+)/?$', 'repsf.map.views.home', name='spec_loc'),
)

urlpatterns += patterns('',
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
