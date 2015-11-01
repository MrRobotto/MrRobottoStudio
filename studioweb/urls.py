from django.conf.urls import patterns, url, include

studiourls = patterns('',
    url(r'^$', 'studioweb.views.studio_home', name='studio'),
    url(r'^login-page/$', 'studioweb.views.studio_login_page', name='login-page'),
    url(r'^logout-user/$', 'studioweb.views.studio_logout_user', name='logout-user'),
    url(r'^devices/$', 'studioweb.views.studio_devices', name='devices'),
    url(r'^blender-files/$', 'studioweb.views.studio_blender_files', name='blender-files')
    )

urlpatterns = patterns('',
    url(r'^$', 'studioweb.views.root'),
    url(r'^studio/', include(studiourls)),
    )

