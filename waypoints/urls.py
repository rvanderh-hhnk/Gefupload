from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.static import static

from waypoints import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='waypoints-index'),
    url(r'^contact$', views.contact, name='waypoints-contact'),
    url(r'^levering$', views.levering, name='waypoints-levering'),
    url(r'^sheet002.htm$', views.levering, name='waypoints-levering'),
    url(r'^tabstrip.htm$', views.levering, name='waypoints-levering'),
    url(r'^geoportaal$', views.geoportaal, name='waypoints-geoportaal'),
    url(r'^upload$', views.upload, name='waypoints-upload'),
    url(r'^delete$', views.delete, name='waypoints-delete'),
    url(r'^del_project$', views.del_project, name='waypoints-del_project'),
    url(r'^truncate$', views.truncate, name='waypoints-truncate'),
    url(r'^opleveren$', views.opleveren, name='waypoints-opleveren'),
	url(r'^accounts/', include('registration.backends.default.urls')),
)

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)