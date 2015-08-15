from django.conf.urls import url, include
from rest_framework import routers
import studioservices
from studioservices.views import *

router = routers.SimpleRouter()
router.register(r'register', RegisterViewSet, base_name='api-register')
router.register(r'login', LoginViewSet, base_name='api-login')
router.register(r'users', UserViewSet, base_name='api-users')
router.register(r'tokens', AuthTokenViewSet, base_name='api-tokens')
router.register(r'devices', AndroidDeviceViewSet, base_name='api-devices')
router.register(r'blendfiles', BlendFilesViewSet, base_name='api-blendfiles')

apipatterns = [
    url(r'^', include(router.urls)),
]

urlpatterns = [
    url(r'^api/v1/', include(apipatterns))
]