import io
import os

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.core.files.storage import default_storage
from django.http import FileResponse
from django.utils import timezone
from rest_framework import viewsets, mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, list_route, api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import qrcode.main
from rest_framework.reverse import reverse
from MrRobottoStudioServer import settings

from studioservices import utils
from studioservices.models import AndroidDevice, MrrFile
from studioservices.permissions import UserViewPermission, AuthTokenPermissions
from studioservices.serializers import UserSerializer, AuthTokenSerializer, RegisterSerializer, LoginSerializer, \
    AndroidDeviceSerializer, MrrFilesSerializer

User = get_user_model()


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
            #if 'attemp_id' not in request.data:
            #    return Response({'error': 'Not attemp_id field in url query'}, status=status.HTTP_400_BAD_REQUEST)
            id = request.data['android_id']
            name = request.data['name']
            #pk = request.data['attemp_id']
            #attempQuery = RegistrationAttemp.objects.filter(pk=pk, user=request.user, is_used=False)
            #if len(attempQuery) == 1:
            #    attemp = attempQuery.first()
            #else:
            #    return Response({'error': 'Expired registration code'}, status=status.HTTP_400_BAD_REQUEST)
            #attemp.is_used = True
            #attemp.save()
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

    def get_register_data(self, request):
        token, created = Token.objects.get_or_create(user=request.user)
        #attemp, created = RegistrationAttemp.objects.get_or_create(user=request.user, is_used=False)
        #url = utils.get_base_url() + reverse("api-devices-list") + "?attemp_id=" + str(attemp.pk)
        return {'base_url': utils.get_base_url(), 'token':token.key}

    @list_route(methods=['GET'])
    def qrcode(self, request, *args, **kwargs):
        img = qrcode.main.make(self.get_register_data(request))
        f = io.BytesIO()
        img.save(f, kind='PNG')
        f.seek(0)
        return FileResponse(f, content_type='image/png')

    @list_route(methods=['GET'])
    def manualregister(self, request, *args, **kwargs):
        d = {'base_url': utils.get_base_url()}
        return Response(d)

    @detail_route(methods=['GET'])
    def connect(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            device = self.get_queryset().get(pk=pk)
            device.is_connected = True
            device.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @detail_route(methods=['GET'])
    def disconnect(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        try:
            device = self.get_queryset().get(pk=pk)
            device.is_connected = False
            device.save()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)



class MrrFilesViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticated, )
    queryset = MrrFile.objects.all()
    serializer_class = MrrFilesSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return MrrFile.objects.all().order_by('-upload_date')
        else:
            return MrrFile.objects.filter(user=self.request.user).order_by('-upload_date')

    def save_blend(self, request):
        #Obtain the file
        f = request.FILES['blend']
        base_name = os.path.splitext(os.path.basename(f.name))[0]
        mrr = self.get_queryset().filter(user=self.request.user, base_name=base_name).first()
        created = not (mrr == None)
        if not created:
            try:
                os.remove(mrr.blend_file.path)
            except Exception as e:
                print(e)
                pass
            try:
                os.remove(mrr.mrr_file.path)
            except Exception as e:
                print(e)
                pass
        #Save the file
        username = request.user.username
        name_stored_file = default_storage.save(username + "/" + f.name, f)
        base_name2 = name_stored_file.split(".")[0]
        path = os.path.join(settings.MEDIA_ROOT, name_stored_file)
        #Export file
        if not utils.export_blend_to_mrr(path):
            os.remove(path)
            return Response({'error': 'Error exporting file'}, status=status.HTTP_400_BAD_REQUEST)
        mrr_path = os.path.join(os.path.dirname(path), base_name2+".mrr")
        #Save the model
        if created:
            mrr = MrrFile(user=self.request.user, base_name=base_name)
        mrr.upload_date = timezone.now()
        mrr.blend_file.name = path
        mrr.mrr_file.name = mrr_path
        mrr.save()
        self.select_file(mrr.pk)
        return mrr, created

    def save_textures(self, request):
        i = 0
        more_tex = True
        textures = []
        while more_tex:
            try:
                t = request.FILES['tex'+i]
                textures.append(t)
            except:
                more_tex = False
            i += 1
        return textures

    def create(self, request, *args, **kwargs):
        if 'blend' in request.FILES:
            self.save_textures(request)
            mrr, created = self.save_blend(request)
            return Response(MrrFilesSerializer().to_representation(mrr), status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
        else:
            return Response({'error': 'No file selected'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        pk = kwargs['pk']
        f = self.get_queryset().filter(pk=pk)[0]
        try:
            os.remove(f.mrr_file.path)
        except:
            pass
        try:
            os.remove(f.blend_file.path)
        except:
            pass
        return viewsets.ModelViewSet.destroy(self, request, args, kwargs)

    #TODO: Check existence
    @detail_route(methods=['GET'])
    def download(self, request, *args, **kwargs):
        pk = kwargs['pk']
        try:
            f = self.get_queryset().get(pk=pk)
            r = FileResponse(f.mrr_file, content_type="application/octet-stream")
            r['Content-Disposition'] = 'attachment; filename="' + f.base_name + '.mrr"'
            return r
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def select_file(self, pk):
        selecteds = self.get_queryset().filter(is_selected=True)
        for sel in selecteds:
            sel.is_selected = False
            sel.save()
        files = self.get_queryset().filter(pk=pk)
        f = files[0]
        f.is_selected = True
        f.save()
        return f

    #TODO: Check existence
    @detail_route(methods=['GET'])
    def select(self, request, *args, **kwargs):
        pk = kwargs['pk']
        f = self.select_file(pk)
        return Response(MrrFilesSerializer().to_representation(f) ,status=status.HTTP_200_OK)

    @list_route(methods=['GET'])
    def selected(self, request, *args, **kwargs):
        f = self.get_queryset().filter(is_selected=True)
        if len(f) > 0:
            f = f[0]
            return Response(MrrFilesSerializer().to_representation(f) ,status=status.HTTP_200_OK)
        return Response({} ,status=status.HTTP_200_OK)
