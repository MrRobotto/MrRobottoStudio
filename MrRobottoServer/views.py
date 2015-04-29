from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.views.generic import View

from models import get_android_connection, get_blender_search_dir, set_blender_search_dir
from models import get_blender_exe, get_blender_file
from utils import *


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

class Studio(View):

    def studio_get(self, request, context):
        context['blender'] = get_blender_exe().get_abspath()
        context['blender_file'] = get_blender_file().get_abspath()
        return TemplateResponse(request, "index.html",context=context)

    def blender_config_get(self,request,context):
        dir = get_blender_search_dir()
        context['current'] = get_blender_exe().get_abspath()
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

    def blender_config_post(self, request):
        if 'dirname' in request.POST:
            dirname = request.POST['dirname']
            set_blender_search_dir(dirname)
        elif 'exe' in request.POST:
            get_blender_exe().set_blender_path(get_blender_search_dir())
            get_blender_exe().set_blender_exe(request.POST['exe'])
        return redirect("/blender-config")

    def blender_file_get(self, request, context):
        path = get_blender_file().get_path()
        context['current'] = get_blender_file().get_abspath()
        try:
            dir = get_directory(path)
            context['dirname'] = dir[0]
            context['folders'] = dir[1]
            context['files'] = file_filter(dir[2],".blend")
        except:
            context['dirname'] = path
            context['folders'] = []
            context['files'] = []
        return TemplateResponse(request, "blender-file.html", context=context)

    def blender_file_post(self, request):
        if 'dirname' in request.POST:
            dirname = request.POST['dirname']
            get_blender_file().navigate_to_path(dirname)
        elif 'blend' in request.POST:
            get_blender_file().set_blend_file(request.POST['blend'])
            return redirect("/json-tools")
        elif 'export' in request.POST:
            export()
            return redirect("/json-tools")
        return redirect("/blender-file")


    def json_tools_get(self, request, context):
        context['current_blend'] = get_blender_file().get_abspath()
        context['current_json'] = get_blender_file().get_json_abspath()
        context['json'] = load_json(get_blender_file().get_json_abspath())
        return TemplateResponse(request, "json-tools.html", context=context)

    def json_tools_post(self, request):
        if 'export' in request.POST:
            export(False)
            return redirect("/json-tools")


    def post(self, request):
        if request.path == "/blender-config":
            return self.blender_config_post(request)
        elif request.path == "/blender-file":
            return self.blender_file_post(request)
        elif request.path == "/json-tools":
            return self.json_tools_post(request)

    def get(self, request):
        con = get_android_connection()
        context = dict()
        context['con'] = con
        context['ip'] = get_ip()
        if request.path == "/studio/":
            return self.studio_get(request, context)
        elif request.path == "/blender-config":
            return self.blender_config_get(request, context)
        elif request.path == "/blender-file":
            return self.blender_file_get(request, context)
        elif request.path == "/json-tools":
            return self.json_tools_get(request, context)



def flush_devices(request):
    con = get_android_connection()
    con.disconnect()
    return redirect('studio')




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

    def fast_update(self, request):
        if not is_android(request):
            return HttpResponse(403)
        con = get_android_connection()
        con.connect(get_user_agent(request))
        export(needsExport=False)
        #con.disconnect()
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

