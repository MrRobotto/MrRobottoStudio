from django.contrib.auth import get_user_model, authenticate, login, logout
from django.http import FileResponse
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, list_route
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.response import Response
from rest_framework.reverse import reverse
from MrRobottoStudioServer import utils
from studioservices.models import AndroidDevice, RegistrationAttemp, BlendFile
from studioservices.serializers import UserSerializer, AuthTokenSerializer, RegisterSerializer, LoginSerializer, \
    AndroidDeviceSerializer, BlendFileSerializer

import qrcode.main
import io

User = get_user_model()

class UserViewPermission(BasePermission):

    def has_permission(self, request, view):
        if IsAdminUser().has_permission(request, view):
            return True
        if view.action in ['create']:
            return not IsAuthenticated().has_permission(request, view)
        if view.action in ['delete']:
            return IsAdminUser().has_permission(request, view)
        if view.action in ['list','retrieve','update','partial_update','qrcode']:
            return IsAuthenticated().has_permission(request, view)
        return False

    def has_object_permission(self, request, view, obj):
        if IsAdminUser().has_permission(request, view):
            return True
        if view.action in ['create']:
            return False
        if view.action in ['delete']:
            return IsAdminUser().has_permission(request, view)
        if view.action in ['list','retrieve','update','partial_update']:
            return IsAuthenticated().has_permission(request, view) and request.user == obj
        return False


class RegisterViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [UserViewPermission]

    def create(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        if s.is_valid(raise_exception=True):
            user = User.objects.create_user(username=s.data['username'],
                                            password=s.data['password'])
            token, created = Token.objects.get_or_create(user=user)
            user = authenticate(username=s.data['username'], password=s.data['password'])
            login(request, user)
            return Response({'username': user.username, 'token': token.key}, status=status.HTTP_201_CREATED)


class LoginViewSet(viewsets.GenericViewSet,
                   mixins.CreateModelMixin):

    queryset = User.objects.all()
    serializer_class = LoginSerializer
    permission_classes = [UserViewPermission]

    def create(self, request, *args, **kwargs):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            login(request, user)
            return Response({'user':user.username, 'token':token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'bad credentials'}, status=status.HTTP_400_BAD_REQUEST)


class LogoutViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin):

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        logout(request)
        #TODO: Remove token
        return Response()


class UserViewSet(viewsets.GenericViewSet,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin):
    """
    A view for editing user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserViewPermission]
    lookup_field = ('username')

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        else:
            return User.objects.filter(pk=self.request.user.pk)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        d = serializer.data
        devices = AndroidDevice.objects.filter(user=instance)
        s = AndroidDeviceSerializer()
        list_devices = [{'android_id':device.android_id} for device in devices]
        d['devices'] = list_devices
        return Response(d)


class AuthTokenPermissions(BasePermission):

    def has_permission(self, request, view):
        if IsAdminUser().has_permission(request, view):
            return True
        if view.action in ['list']:
            return IsAuthenticated().has_permission(request, view)
        if view.action in ['create']:
            return True
        if view.action in ['retrieve']:
            return IsAuthenticated().has_permission(request, view)
        if view.action in ['destroy']:
            return IsAuthenticated().has_permission(request, view)


class AuthTokenViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin):
    """A view for managing auth token"""
    queryset = Token.objects.all()
    serializer_class = AuthTokenSerializer
    permission_classes = [AuthTokenPermissions]
    lookup_field = ('user__username')

    def get_queryset(self):
        if self.request.user.is_staff:
            return Token.objects.all()
        else:
            return Token.objects.filter(user=self.request.user)


class AndroidDeviceViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = AndroidDevice.objects.all()
    serializer_class = AndroidDeviceSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return AndroidDevice.objects.all().order_by('-last_connection')
        else:
            return AndroidDevice.objects.filter(user=self.request.user).order_by('-last_connection')

    def create(self, request, *args, **kwargs):
        try:
            if 'android_id' not in request.data:
                return Response({'error': 'Not android_id field in request data'}, status=status.HTTP_400_BAD_REQUEST)
            if 'name' not in request.data:
                return Response({'error': 'Not name field in request data'}, status=status.HTTP_400_BAD_REQUEST)
            if 'attemp_id' not in request.data:
                return Response({'error': 'Not attemp_id field in url query'}, status=status.HTTP_400_BAD_REQUEST)
            id = request.data['android_id']
            name = request.data['name']
            pk = request.GET['attemp_id']
            attempQuery = RegistrationAttemp.objects.filter(pk=pk, user=request.user, is_used=False)
            if len(attempQuery) == 1:
                attemp = attempQuery.first()
            else:
                return Response({'error': 'Expired registration code'}, status=status.HTTP_400_BAD_REQUEST)
            attemp.is_used = True
            attemp.save()
            device, created1 = AndroidDevice.objects.get_or_create(android_id=id, user=request.user)
            if name == "":
                name = id
            if created1:
                device.name = name
                device.save()
            token, created2 = Token.objects.get_or_create(user=request.user)
            d = AndroidDeviceSerializer().to_representation(device)
            d.update({'token': token.key})
            return Response(d, status=status.HTTP_201_CREATED if created1 else status.HTTP_200_OK)
        except:
            return Response({'error': 'bad request data'}, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['GET'])
    def qrcode(self, request, *args, **kwargs):
        token, created = Token.objects.get_or_create(user=request.user)
        attemp, created = RegistrationAttemp.objects.get_or_create(user=request.user, is_used=False)
        url = utils.get_baser_url() + reverse("api-devices-list") + "?pk=" + str(attemp.pk)
        img = qrcode.main.make({'url': url, 'token':token.key})
        f = io.BytesIO()
        img.save(f, kind='PNG')
        f.seek(0)
        return FileResponse(f, content_type='image/png')


class BlendFilesViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = BlendFile.objects.all()
    serializer_class = BlendFileSerializer


    def get_queryset(self):
        if self.request.user.is_staff:
            return BlendFile.objects.all().order_by('-upload_date')
        else:
            return BlendFile.objects.filter(user=self.request.user).order_by('-upload_date')

    def create(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            f = request.FILES['file']
            blend, created = BlendFile.objects.get_or_create(user=self.request.user, filename=f.name)
            blend.file = f
            blend.upload_date = timezone.now()
            blend.save()
            return Response(BlendFileSerializer().to_representation(blend), status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        else:
            return Response({'error': 'No file selected'}, status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['GET'])
    def download(self, request, *args, **kwargs):
        pk = kwargs['pk']
        files = self.get_queryset().filter(pk=pk)
        blend = files[0]
        r = FileResponse(blend.file, content_type="application/octet-stream")
        r['Content-Disposition'] = 'attachment; filename="' + blend.filename + '"'
        return r