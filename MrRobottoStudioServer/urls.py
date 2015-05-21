from django.conf.urls import patterns, url
from django.conf.urls.static import static

from MrRobottoStudioServer.views import Studio, AndroidView, ServicesView
import MrRobottoStudioServer.settings as settings


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'MrRobottoStudioServer.views.home', name='home'),

    url(r'^studio', Studio.as_view(), name='studio'),
    url(r'^studio/blender-config', Studio.as_view(), name='blender-config'),
    url(r'^studio/blender-file', Studio.as_view(), name='blender-file'),
    url(r'^studio/json-tools', Studio.as_view(), name='json-tools'),

    url(r'^android/connect', AndroidView.as_view(), name='connect'),
    url(r'^android/disconnect', AndroidView.as_view(), name='disconnect'),
    url(r'^android/update', AndroidView.as_view(), name='update'),

    url(r'^services/is-connected', ServicesView.as_view(), name='is-connected'),
    url(r'^services/textures', ServicesView.as_view(), name="textures"),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
