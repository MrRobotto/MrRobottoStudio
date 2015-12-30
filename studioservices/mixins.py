import os
from django.core.files.storage import default_storage
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from MrRobottoStudioServer import settings
from studioservices import utils
from studioservices.models import MrrFile
from studioservices.serializers import MrrFilesSerializer


class MrrFileExporter:

    def save_blend(self, request):
        #Obtain the file
        f = request.FILES['blend']
        base_name = os.path.splitext(os.path.basename(f.name))[0]
        mrr = MrrFile.objects.filter(user=request.user, base_name=base_name).first()
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
        user_path = os.path.join(settings.MEDIA_ROOT, username, f.name)
        name_stored_file = default_storage.save(user_path, f)
        base_name2 = name_stored_file.split(".")[0]
        path = os.path.join(settings.MEDIA_ROOT, name_stored_file)
        #Export file
        if not utils.export_blend_to_mrr(path):
            os.remove(path)
            return Response({'error': 'Error exporting file'}, status=status.HTTP_400_BAD_REQUEST)
        mrr_path = os.path.join(os.path.dirname(path), base_name2+".mrr")
        #Save the model
        if not created:
            mrr = MrrFile(user=request.user, base_name=base_name)
        mrr.upload_date = timezone.now()
        mrr.blend_file.name = path
        mrr.mrr_file.name = mrr_path
        mrr.save()
        #self.select_file(mrr.pk)
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