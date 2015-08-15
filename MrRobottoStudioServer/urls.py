from django.conf.urls import patterns, url, include
from django.conf.urls.static import static

from studio.views import ServicesView
#from studio import urls as studio_urls
from studioweb import urls as studio_urls
from studioservices import urls as services_urls
import MrRobottoStudioServer.settings as settings

urlpatterns = patterns('',
    url(r'^$', 'MrRobottoStudioServer.views.home', name='home'),
    #url(r'^studio/', include('studio.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^services/is-connected', ServicesView.as_view(), name='is-connected'),
    url(r'^services/textures', ServicesView.as_view(), name="textures"),
)

urlpatterns += studio_urls.urlpatterns
urlpatterns += services_urls.urlpatterns
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)