import os
import time
import re
import subprocess
import struct

from MrRobottoStudioServer import settings


def is_studio_app(request):
    ua = get_user_agent(request)
    ua = ua.lower()
    return "mrrobotto" in ua

def get_user_agent(request):
    return request.META['HTTP_USER_AGENT']

def file_filter(files, ext):
    return [f for f in files if re.match(r".*."+ext+'$',f)]

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
    elif dir is not None:
        return os.path.abspath(dir)
    return None

def export_to_mrr(blender, file):
    script = os.path.join(settings.BASE_DIR,'scripts','JSONExporter.py')
    subprocess.call([blender, file, '--background','--python',script])

def save_json(filepath, json):
    f = file(filepath, 'w')
    f.write(json)
    f.close()

def get_modification_time(f):
    return time.ctime(os.path.getmtime(f))

def decode_mrr(filename):
    f = open(filename, "rb")
    magic = f.readline().strip()
    if not magic == 'MRROBOTTOFILE':
        return None, None
    command = f.read(4)
    json = None
    images = dict()
    while not command == "FNSH":
        if command == "JSON":
            l = f.read(4)
            l = struct.unpack('>I', l)[0]
            f.read(1)
            json = f.read(l)
            f.read(1)
        if command == "TEXT":
            ntex = f.read(4)
            ntex = struct.unpack('>I', ntex)[0]
            f.read(1)
            for texi in range(ntex):
                nameTag = f.read(4)
                nameLen = f.read(4)
                nameLen = struct.unpack('>I', nameLen)[0]
                texName = f.read(nameLen)
                texLen = f.read(4)
                texLen = struct.unpack('>I', texLen)[0]
                f.read(1)
                image = f.read(texLen)
                f.read(1)
                images[texName] = image
        command = f.read(4)
    return json, images