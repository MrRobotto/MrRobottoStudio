from tempfile import TemporaryFile, NamedTemporaryFile
import django
from django.http import HttpResponse, FileResponse, JsonResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.generic import View

from MrRobottoStudioServer.AppController import *
from MrRobottoStudioServer.ServerSocket import *

#from AppController import *
#from ServerSocket import AndroidTCPServer
from MrRobottoStudioServer import settings
from MrRobottoStudioServer.AppController import BlenderExe, BlendFile, MRRFile, FileSystemNavigator
import MrRobottoStudioServer.utils
from MrRobottoStudioServer.utils import *


def prueba(request):
    AndroidView.server_socket.send_update()
    return HttpResponse()

def home(request):
    if is_studio_app(request):
        return redirect('connect')
    else:
        return redirect('studio')

class Studio(View):
    blender_exe = BlenderExe()
    blender_file = BlendFile()
    mrr_file = MRRFile()
    blender_exe_explorer = FileSystemNavigator()
    blender_file_explorer = FileSystemNavigator()

    def get_base_context(self):
        context = dict()
        context['connected'] = AndroidView.server_socket.android is not None
        context['ip'] = get_ip()
        return context

    def export(self,needsExport=True):
        if needsExport:
            utils.export_to_mrr(Studio.blender_exe.file_path, Studio.blender_file.file_path)
            Studio.mrr_file.setFile(Studio.blender_file.dir_path, Studio.blender_file.get_file_base_name()+".mrr")
            Studio.mrr_file.export()
        if AndroidView.server_socket.is_connected():
            AndroidView.server_socket.send_update()
        #con = get_android_connection()
        #con.update_mrr(load_mrr(get_blender_file().get_mrr_abspath()))

    def post_blender_config(self, request):
        if 'dirname' in request.POST:
            dirname = request.POST['dirname']
            Studio.blender_exe_explorer.navigate_to(dirname)
        elif 'exe' in request.POST:
            dir_path = Studio.blender_exe_explorer.dir_path
            Studio.blender_exe.setFile(dir_path, request.POST['exe'])
        return redirect("blender-config")

    def post_blender_file(self, request):
        if 'dirname' in request.POST:
            dirname = request.POST['dirname']
            Studio.blender_file_explorer.navigate_to(dirname)
            return redirect("blender-file")
        elif 'blend' in request.POST:
            dir_path = Studio.blender_file_explorer.dir_path
            Studio.blender_file.setFile(dir_path, request.POST['blend'])
            self.export()
            return redirect("json-tools")
        elif 'export' in request.POST:
            self.export()
            return redirect("json-tools")

    def post_json_tools(self, request):
        if 'export' in request.POST:
            self.export()
            return redirect("json-tools")
        elif 'upload' in request.POST:
            self.export(needsExport=False)
            return redirect("json-tools")
        elif 'save' in request.POST:
            #save_json(get_blender_file().get_json_abspath(), request.POST['json'])
            return redirect("json-tools")

    def post(self, request):
        path = request.path.replace('/','')
        if path == "studioblender-config":
            return self.post_blender_config(request)
        elif path == "studioblender-file":
            return self.post_blender_file(request)
        elif path == "studiojson-tools":
            return self.post_json_tools(request)
        else:
            return HttpResponse(404)

    def get_studio(self, request):
        context = self.get_base_context()
        context['blender'] = Studio.blender_exe.file_path
        context['blender_file'] = Studio.blender_file.file_path
        return TemplateResponse(request, "index.html", context=context)

    def get_blender_config(self,request):
        context = self.get_base_context()
        dir_path = Studio.blender_exe_explorer.dir_path
        context['current'] = Studio.blender_exe.file_path
        list_dir = get_directory(dir_path)
        context['dirname'] = list_dir[0]
        context['folders'] = list_dir[1]
        context['files'] = file_filter(list_dir[2],".exe")
        return TemplateResponse(request, "blender-config.html", context=context)

    def get_blender_file(self, request):
        context = self.get_base_context()
        dir_path = Studio.blender_file_explorer.dir_path
        context['current'] = Studio.blender_file.file_path
        print(dir_path)
        list_dir = get_directory(dir_path)
        context['dirname'] = list_dir[0]
        context['folders'] = list_dir[1]
        context['files'] = file_filter(list_dir[2],".blend")
        return TemplateResponse(request, "blender-file.html", context=context)

    def get_json_tools(self, request):
        context = self.get_base_context()
        context['current_blend'] = Studio.blender_file.file_path
        if Studio.mrr_file.exported:
            context['current_mrr'] = Studio.mrr_file
            context['json'] = Studio.mrr_file.get_json()
            context['texture_names'] = Studio.mrr_file.get_textures().keys()
        return TemplateResponse(request, "json-tools.html", context=context)

    def get(self, request):
        context = dict()
        context['connected'] = AndroidView.server_socket.android is not None
        context['ip'] = get_ip()
        path = request.path.replace('/','')
        if path == "studio":
            return self.get_studio(request)
        elif path == "studioblender-config":
            return self.get_blender_config(request)
        elif path == "studioblender-file":
            return self.get_blender_file(request)
        elif path == "studiojson-tools":
            return self.get_json_tools(request)
        else:
            return HttpResponse(404)





class AndroidView(View):
    server_socket = AndroidTCPServer()
    connected = False

    def get_connect(self, request):
        response = HttpResponse(status=200)
        response['server_socket_port'] = settings.SERVER_SOCKET_PORT
        AndroidView.connected = True
        return response

    def get_disconnect(self, request):
        AndroidView.connected = False
        return HttpResponse(status=200)

    def get_update(self, request):
        return FileResponse(open(Studio.mrr_file.file_path,'rb'))

    def get(self, request):
        #if not utils.is_studio_app(request):
        #    return HttpResponse(status=403)
        path = request.path.replace('/','')
        if path == "androidconnect":
            return self.get_connect(request)
        elif path == "androiddisconnect":
            return self.get_disconnect(request)
        elif path == "androidupdate":
            return self.get_update(request)
        else:
            return HttpResponse(404)


class ServicesView(View):
    last_android = None

    '''def get_is_connected(self, request):
        AndroidView.server_socket.lock.acquire()
        current = AndroidView.server_socket.is_connected()
        AndroidView.server_socket.lock.release()
        #while current == ServicesView.last_android:
        #    current = AndroidView.server_socket.is_connected()
        #ServicesView.last_android = current
        #while not AndroidView.server_socket.has_changed(): None
        #print "salgo y envio", AndroidView.server_socket.is_connected()
        return JsonResponse({'value':current})'''

    def get_is_connected(self, request):
        current = AndroidView.connected
        while current == ServicesView.last_android:
            current = AndroidView.connected
        ServicesView.last_android = current
        return JsonResponse({'value':current})

    def get_get_texture(self, request):
        texname = request.path.split('/')[-1]
        suffix = texname.split('.')[-1]
        f = NamedTemporaryFile(suffix='.'+suffix)
        f.write(Studio.mrr_file.get_textures()[texname])
        f.seek(0)
        return FileResponse(f)

    def get(self, request):
        path = request.path.replace('/','')
        if path == "servicesis-connected":
            return self.get_is_connected(request)
        if "textures" in path:
            return self.get_get_texture(request)