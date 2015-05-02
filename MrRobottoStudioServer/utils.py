import os
import subprocess
from MrRobottoStudioServer import settings


def is_android(request):
    ua = get_user_agent(request)
    ua = ua.lower()
    return "android" in ua

def get_user_agent(request):
    return request.META['HTTP_USER_AGENT']

def file_filter(files, ext):
    return [f for f in files if ext in f]

def get_ip():
    import socket
    #return socket.gethostname()
    return socket.gethostbyname(socket.gethostname())

def get_directory(dir):
    g = os.walk(dir)
    return g.next()

def get_abs_path(dir, file=None):
    if file is not None:
        return os.path.abspath(os.path.join(dir,file))
    else:
        return os.path.abspath(dir)

def export_to_json(blender, file):
    script = os.path.join(settings.BASE_DIR,'scripts','JSONExporter3')
    subprocess.call([blender, file, '--background','--python',script])

def save_json(filepath, json):
    f = file(filepath, 'w')
    f.write(json)
    f.close()

def load_json(filename):
    if filename:
        f = open(filename)
        o = f.read()
        return o.replace('"','\"')
