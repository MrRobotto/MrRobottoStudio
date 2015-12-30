from django.conf.urls import patterns, url, include
from studioweb import views

studiourls = [
    url(r'^$', views.studio_home, name='studio'),
    url(r'^login-page/$', views.studio_login_page, name='login-page'),
    url(r'^logout-user/$', views.studio_logout_user, name='logout-user'),
    url(r'^devices/$', views.studio_devices, name='devices'),
    url(r'^blender-files/?$', views.studio_blender_files, name='blender-files')
    ]

urlpatterns = [
    url(r'^$', views.root),
    url(r'^studio/', include(studiourls)),
    ]

