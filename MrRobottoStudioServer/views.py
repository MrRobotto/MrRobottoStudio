import mimetypes
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.generic import View

from models import get_android_connection, get_blender_search_dir, set_blender_search_dir
from models import get_blender_exe, get_blender_file
from utils import *
import utils
from AppController import *

from ServerSocket import runServerSocket, getSocketServer
runServerSocket()

def caca(request):
    getSocketServer().android.sendall("caca")

def home(request):
    if is_android(request):
        return redirect('connect')
    else:
        return redirect('studio')

def export(needsExport=True):
    if needsExport:
        export_to_json(get_blender_exe().get_abspath(), get_blender_file().get_abspath())
        get_blender_file().export()
    con = get_android_connection()
    con.update(load_json(get_blender_file().get_json_abspath()))

def export_mrr(needsExport=True):
    if needsExport:
        export_to_mrr(get_blender_exe().get_abspath() , get_blender_file().get_abspath())
        get_blender_file().export_mrr()
    con = get_android_connection()
    con.update_mrr(load_mrr(get_blender_file().get_mrr_abspath()))



class Studio(View):
    blender_exe = BlenderExe()
    blender_file = BlendFile()
    mrr_file = MRRFile()
    blender_exe_explorer = FileSystemNavigator()
    blender_file_explorer = FileSystemNavigator()

    def get_base_context(self):
        context = dict()
        context['connected'] = getSocketServer().android is not None
        context['ip'] = get_ip()
        return context

    def export(self,needsExport=True):
        if needsExport:
            utils.export_to_mrr(Studio.blender_exe.file_path, Studio.blender_file.file_path)
            Studio.mrr_file.setFile(Studio.blender_file.dir_path, Studio.blender_file.get_file_base_name()+".mrr")
            Studio.mrr_file.export()
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
        elif 'blend' in request.POST:
            dir_path = Studio.blender_file_explorer.dir_path
            Studio.blender_file.setFile(dir_path, request.POST['blend'])
            self.export()
            return redirect("json-tools")
        elif 'export' in request.POST:
            self.export()
            return redirect("json-tools")
        return redirect("blender-file")

    def post_json_tools(self, request):
        if 'export' in request.POST:
            self.export()
            return redirect("json-tools")
        elif 'upload' in request.POST:
            return redirect("json-tools")
        elif 'save' in request.POST:
            #save_json(get_blender_file().get_json_abspath(), request.POST['json'])
            return redirect("json-tools")

    def post(self, request):
        path = request.path.replace('/','')
        if path == "blender-config":
            return self.post_blender_config(request)
        elif path == "blender-file":
            return self.post_blender_file(request)
        elif path == "json-tools":
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
        dir = Studio.blender_exe_explorer.dir_path
        context['current'] = Studio.blender_exe.file_path
        try:
            dir = get_directory(dir)
            context['dirname'] = dir[0]
            context['folders'] = dir[1]
            context['files'] = file_filter(dir[2],".exe")
        except:
            context['dirname'] = get_blender_search_dir()
            context['folders'] = []
            context['files'] = []
        return TemplateResponse(request, "blender-config.html", context=context)

    def get_blender_file(self, request):
        context = self.get_base_context()
        dir_path = Studio.blender_file_explorer.dir_path
        context['current'] = Studio.blender_file.file_path
        try:
            dir = get_directory(dir_path)
            context['dirname'] = dir[0]
            context['folders'] = dir[1]
            context['files'] = file_filter(dir[2],".blend")
        except:
            context['dirname'] = dir_path
            context['folders'] = []
            context['files'] = []
        return TemplateResponse(request, "blender-file.html", context=context)

    def get_json_tools(self, request):
        context = self.get_base_context()
        context['current_blend'] = Studio.blender_file.file_path
        if Studio.mrr_file.exported:
            context['current_mrr'] = Studio.mrr_file
            context['json'] = Studio.mrr_file.decode()[0]
        return TemplateResponse(request, "json-tools.html", context=context)

    def get(self, request):
        con = get_android_connection()
        context = dict()
        context['connected'] = getSocketServer().android is not None
        context['ip'] = get_ip()
        path = request.path.replace('/','')
        if path == "studio":
            return self.get_studio(request)
        elif path == "blender-config":
            return self.get_blender_config(request)
        elif path == "blender-file":
            return self.get_blender_file(request)
        elif path == "json-tools":
            return self.get_json_tools(request)
        else:
            return HttpResponse(404)





class AndroidView2(View):

    def connect(self, request):
        return HttpResponse(status=201)

    def android_update(self, request):
        file_full_path = Studio.mrr_file.file_path
        with open(file_full_path,'rb') as f:
            data = f.read()
        print Studio.mrr_file.file_path
        response = HttpResponse(data, status=201, content_type=mimetypes.guess_type(file_full_path)[0])
        response['Content-Disposition'] = "attachment; filename={0}".format(Studio.mrr_file.file)
        response['Content-Length'] = os.path.getsize(file_full_path)
        return response

    def get(self, request):
        #if not utils.is_android(request):
        #    return HttpResponse(403)
        path = request.path.replace('/','')
        if path == "connect":
            return self.connect(request)
        elif path == "android-update":
            return self.android_update(request)
        else:
            return HttpResponse(404)




class AndroidView(View):

    def connect(self, request):
        if not is_android(request):
            return HttpResponse(403)
        con = get_android_connection()
        con.connect(get_user_agent(request))
        return HttpResponse(status=201)

    def disconnect(self, request):
        if not is_android(request):
            return HttpResponse(403)
        con = get_android_connection()
        con.disconnect()
        return HttpResponse(status=201)

    def wait_update(self, request):
        if not is_android(request):
            return HttpResponse(403)
        con = get_android_connection()
        con.connect(get_user_agent(request))
        while not con.updated: None
        #con.disconnect()
        con.updated = False
        return con.response

    def export(self, needsExport=True):
        if needsExport:
            export_to_json(get_blender_exe().get_abspath(), get_blender_file().get_abspath())
            get_blender_file().export()
        con = get_android_connection()
        con.update(load_json(get_blender_file().get_json_abspath()))

    def fast_update2(self, request):
        if not is_android(request):
            return HttpResponse(403)
        con = get_android_connection()
        con.connect(get_user_agent(request))
        export(needsExport=False)
        #con.disconnect()
        con.updated = False
        return con.response

    def fast_update(self, request):
        con = get_android_connection()
        con.connect(get_user_agent(request))
        export_mrr(needsExport=False)
        con.updated = False
        return con.response



    def get(self, request):
        if request.path == "/connect/":
            return self.connect(request)
        elif request.path == "/disconnect/":
            return self.disconnect(request)
        elif request.path == "/android-update/":
            return self.wait_update(request)
        elif request.path == "/fast-update/":
            return self.fast_update(request)

