from django.conf.urls import patterns, url, include
from django.conf.urls.static import static

from studio.views import ServicesView
from studio import urls as studio_urls
import MrRobottoStudioServer.settings as settings

urlpatterns = patterns('',
    url(r'^$', 'studio.views.home', name='home'),
    #url(r'^studio/', include('studio.urls')),
    url(r'^services/is-connected', ServicesView.as_view(), name='is-connected'),
    url(r'^services/textures', ServicesView.as_view(), name="textures"),
)

urlpatterns += studio_urls.urlpatterns
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)