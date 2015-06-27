from django.conf.urls import patterns, url, include

from studio.views import Studio, AndroidView, ServicesView

androidurls = patterns('',
    url(r'^', AndroidView.as_view(), name='android'),
    url(r'^connect', AndroidView.as_view(), name='connect'),
    url(r'^disconnect', AndroidView.as_view(), name='disconnect'),
    url(r'^update', AndroidView.as_view(), name='update'),
    )

studiourls = patterns('',
    url(r'^', Studio.as_view(), name='studio'),
    url(r'^blender-config', Studio.as_view(), name='blender-config'),
    url(r'^blender-file', Studio.as_view(), name='blender-file'),
    url(r'^json-tools', Studio.as_view(), name='json-tools'),
    )

urlpatterns = patterns('',
    url(r'^studio/', include(studiourls)),
    url(r'^android/', include(androidurls))
    )

