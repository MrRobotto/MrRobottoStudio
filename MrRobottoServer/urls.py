from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import Studio, AndroidView
import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'MrRobottoServer.views.home', name='home'),

    url(r'^studio/', Studio.as_view(), name='studio'),
    url(r'^blender-config', Studio.as_view(), name='blender-config'),
    url(r'^blender-file', Studio.as_view(), name='blender-file'),
    url(r'^json-tools', Studio.as_view(), name='json-tools'),
    url(r'^flush-devices/', 'MrRobottoServer.views.flush_devices', name='flush'),

    url(r'^connect/', AndroidView.as_view(), name='connect'),
    url(r'^disconnect/', AndroidView.as_view(), name='disconnect'),
    url(r'^android-update/', AndroidView.as_view(), name='update'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
