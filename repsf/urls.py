from django.conf.urls import patterns, include, url
from emailusernames.forms import EmailAuthenticationForm
from accounts import views
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
	
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'repsf.map.views.home', name='home'),
	url(r'^accounts/login/?$', 'django.contrib.auth.views.login', {'template_name':'login.html', 'authentication_form': EmailAuthenticationForm}, name='login'),
	url(r'^accounts/create/?$', 'repsf.accounts.views.create', name='register'),
	url(r'^accounts/profile/?$', 'repsf.accounts.views.read', name='show_user'),
	url(r'^accounts/logout/?$', 'repsf.accounts.views.end_session', name='logout'),
	url(r'^(?P<location>\w+)/?$', 'repsf.map.views.home', name='spec_loc'),
)

urlpatterns += patterns('',
	url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
