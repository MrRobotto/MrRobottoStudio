from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import Studio, AndroidView, AndroidView2
import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'MrRobottoStudioServer.views.home', name='home'),

    url(r'^studio', Studio.as_view(), name='studio'),
    url(r'^blender-config', Studio.as_view(), name='blender-config'),
    url(r'^blender-file', Studio.as_view(), name='blender-file'),
    url(r'^json-tools', Studio.as_view(), name='json-tools'),

    url(r'^connect', AndroidView2.as_view(), name='connect'),
    url(r'^disconnect', AndroidView.as_view(), name='disconnect'),
    url(r'^android-update', AndroidView2.as_view(), name='update'),
    url(r'^fast-update', AndroidView.as_view(), name='fast-update'),

    url(r'^caca/', 'MrRobottoStudioServer.views.caca', name='caca')
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
