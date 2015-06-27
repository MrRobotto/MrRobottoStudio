from tempfile import NamedTemporaryFile
from django.http import HttpResponse, FileResponse, JsonResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.generic import View

from MrRobottoStudioServer.utils import *

from studio.models import FileSystemNavigator, FileData, MrrFile, AndroidDevice


def home(request):
    if is_studio_app(request):
        return redirect('connect')
    else:
        return redirect('studio')

class Studio(View):

    @classmethod
    def get_blender_exe_explorer(cls):
        return FileSystemNavigator.objects.get_or_create_blenderexe_fsn()

    @classmethod
    def get_blender_file_explorer(cls):
        return FileSystemNavigator.objects.get_or_create_blendfile_fsn()

    @classmethod
    def get_blender_exe(cls):
        return FileData.objects.get_or_create_blenderexe()

    @classmethod
    def get_blender_file(cls):
        return FileData.objects.get_or_create_blendfile()

    @classmethod
    def get_mrr_file(cls):
        blender_file = Studio.get_blender_file()
        return None if blender_file == None else MrrFile(blender_file)

    def get_base_context(self):
        context = dict()
        context['connected'] = False
        device = AndroidDevice.objects.get_last_android()
        if device is not None:
            context['connected'] = device.is_connected
        context['ip'] = get_ip()
        blender_file = Studio.get_blender_file()
        blender_exe = Studio.get_blender_exe()
        if blender_file is not None:
            context['blendfile'] = blender_file.as_dict()
        if blender_exe is not None:
            context['blenderexe'] = blender_exe.as_dict()
        return context

    def export(self,needsExport=True):
        if needsExport:
            blender_exe = Studio.get_blender_exe()
            blender_file = Studio.get_blender_file()
            export_to_mrr(blender_exe.file_path, blender_file.file_path)
        device = AndroidDevice.objects.get_last_android()
        if device:
            device.update()
        #if AndroidView.connected:
        #    AndroidView.server_socket.send_update()

    def req_post_blender_config(self, request):
        if 'dirname' in request.POST:
            dirname = request.POST['dirname']
            Studio.get_blender_exe_explorer().navigate_to(dirname)
        elif 'exe' in request.POST:
            dir_path = Studio.get_blender_exe_explorer().dir_path
            FileData.objects.get_or_create_blenderexe(dir_path, request.POST['exe'])
        return redirect("blender-config")

    def req_post_blender_file(self, request):
        if 'dirname' in request.POST:
            dirname = request.POST['dirname']
            Studio.get_blender_file_explorer().navigate_to(dirname)
            return redirect("blender-file")
        elif 'blend' in request.POST:
            dir_path = Studio.get_blender_file_explorer().dir_path
            FileData.objects.get_or_create_blendfile(dir_path, request.POST['blend'])
            self.export()
            return redirect("json-tools")
        elif 'export' in request.POST:
            self.export()
            return redirect("json-tools")

    def req_post_json_tools(self, request):
        if 'export' in request.POST:
            self.export()
            return redirect("json-tools")
        elif 'upload' in request.POST:
            self.export(needsExport=False)
            return redirect("json-tools")
        elif 'save' in request.POST:
            Studio.get_mrr_file().update(request.POST['save'])
            self.export(needsExport=False)
            return redirect("json-tools")
        return HttpResponse(404)

    def post(self, request):
        path = request.path.replace('/','')
        if path == "studioblender-config":
            return self.req_post_blender_config(request)
        elif path == "studioblender-file":
            return self.req_post_blender_file(request)
        elif path == "studiojson-tools":
            return self.req_post_json_tools(request)
        else:
            return HttpResponse(404)

    def req_get_studio(self, request):
        context = self.get_base_context()
        return TemplateResponse(request, "index.html", context=context)

    def req_get_blender_config(self,request):
        context = self.get_base_context()
        context['blenderexe_explorer'] = Studio.get_blender_exe_explorer().as_dict()
        return TemplateResponse(request, "blender-config.html", context=context)

    def req_get_blender_file(self, request):
        context = self.get_base_context()
        context['blendfile_explorer'] = Studio.get_blender_file_explorer().as_dict()
        return TemplateResponse(request, "blender-file.html", context=context)

    def req_get_json_tools(self, request):
        context = self.get_base_context()
        mrr_file = Studio.get_mrr_file()
        if mrr_file is not None:
            context['mrr'] = mrr_file.as_dict()
        return TemplateResponse(request, "json-tools.html", context=context)

    def get(self, request):
        path = request.path.replace('/','').replace("studio","")
        if path == "":
            return self.req_get_studio(request)
        elif path == "blender-config":
            return self.req_get_blender_config(request)
        elif path == "blender-file":
            return self.req_get_blender_file(request)
        elif path == "json-tools":
            return self.req_get_json_tools(request)
        else:
            return HttpResponse(404)


class AndroidView(View):

    def req_post_connect(self, request):
        print("POST")
        print(request.POST)
        print("Body")
        print(request.body)
        print("Meta")
        print(request.META)
        android_id = "android"
        if "HTTP_ANDROID_ID" in request.META:
            android_id = request.META["HTTP_ANDROID_ID"]
        device = AndroidDevice.objects.get_or_create_device(android_id)
        if device is not None:
            device.connect()
        return HttpResponse(status=200)

    def req_post_disconnect(self, request):
        device = AndroidDevice.objects.get_last_android()
        if device is not None:
            device.disconnect()
        return HttpResponse(status=200)

    def post(self, request):
        path = request.path.replace('/','').replace("android","")
        if path == "connect":
            return self.req_post_connect(request)
        elif path == "disconnect":
            return self.req_post_disconnect(request)
        else:
            return HttpResponse(404)

    def req_get_connect(self, request):
        print("GET")
        print(request.GET)
        print("Body")
        print(request.body)
        android_id = "android"
        if "android_id" in request.GET:
            android_id = request.GET["android_id"]
        device = AndroidDevice.objects.get_or_create_device(android_id)
        if device is not None:
            device.connect()
        return HttpResponse(status=200)

    def req_get_disconnect(self, request):
        device = AndroidDevice.objects.get_last_android()
        if device is not None:
            device.disconnect()
        return HttpResponse(status=200)

    def req_get_need_update(self, request):
        #while current == ServicesView.last_android:
        #    current = AndroidView.connected
        #ServicesView.last_android = current
        d = dict()
        device = AndroidDevice.objects.get_last_android()
        if device is None:
            d["need_update"] = False
            return JsonResponse(d)
        current = device.need_update
        #while current == AndroidView.last_update:
        #    current = device.need_update
        #AndroidView.last_update = current
        d["need_update"] = current
        return JsonResponse(d)

    def req_get_update(self, request):
        device = AndroidDevice.objects.get_last_android()
        if device is not None:
            device.updated()
        return FileResponse(open(Studio.get_mrr_file().file_path,'rb'))

    def get(self, request):
        #if not utils.is_studio_app(request):
        #    return HttpResponse(status=403)
        path = request.path.replace('/','').replace("android","")
        if path == "connect":
            return self.req_get_connect(request)
        elif path == "disconnect":
            return self.req_get_disconnect(request)
        elif path == "update":
            return self.req_get_update(request)
        elif path == "need-update":
            return self.req_get_need_update(request)
        else:
            return HttpResponse(404)


class ServicesView(View):

    def get_is_connected(self, request):
        #current = AndroidView.android_device.is_connected
        device = AndroidDevice.objects.get_last_android()
        if device is not None:
            current = device.is_connected
        else:
            current = False
        #while current == ServicesView.last_android:
        #    current = AndroidView.connected
        #ServicesView.last_android = current
        return JsonResponse({'value':current})

    def get_get_texture(self, request):
        texname = request.path.split('/')[-1]
        suffix = texname.split('.')[-1]
        f = NamedTemporaryFile(suffix='.'+suffix)
        f.write(Studio.get_mrr_file().get_textures()[texname])
        f.seek(0)
        return FileResponse(f)

    def get(self, request):
        path = request.path.replace('/','')
        if path == "servicesis-connected":
            return self.get_is_connected(request)
        if "textures" in path:
            return self.get_get_texture(request)