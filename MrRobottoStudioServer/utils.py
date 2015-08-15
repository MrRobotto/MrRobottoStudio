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
    if settings.STUDIO_IP is None:
        import socket
        return socket.gethostbyname(socket.gethostname())
    else:
        return settings.STUDIO_IP

def get_port():
    return settings.STUDIO_PORT

def get_baser_url():
    return "http://" + get_ip() + ":" + str(get_port())

def get_directory(dir):
    g = os.walk(dir)
    return next(g)

def get_abs_path(dir, file=None):
    if file is not None:
        return os.path.abspath(os.path.join(dir,file))
    elif dir is not None:
        return os.path.abspath(dir)
    return None

def export_to_mrr(blender, file):
    script = os.path.join(settings.BASE_DIR,'scripts/mrrexporter','mrrexporter.py')
    subprocess.call([blender, file, '--background','--python',script])

def get_modification_time(f):
    return time.ctime(os.path.getmtime(f))

def decode_mrr(filename):
    f = open(filename, "rb")
    magic = f.readline().strip()
    if not magic == b"MRROBOTTOFILE":
        return None, None
    command = f.read(4)
    json = None
    images = dict()
    while not command == b"FNSH":
        if command == b"JSON":
            l = f.read(4)
            l = struct.unpack('>I', l)[0]
            f.read(1)
            json = f.read(l)
            json = json.decode("ascii")
            f.read(1)
        if command == b"TEXT":
            ntex = f.read(4)
            ntex = struct.unpack('>I', ntex)[0]
            f.read(1)
            for texi in range(ntex):
                nameTag = f.read(4)
                nameLen = f.read(4)
                nameLen = struct.unpack('>I', nameLen)[0]
                texName = f.read(nameLen)
                texName = texName.decode("ascii")
                texLen = f.read(4)
                texLen = struct.unpack('>I', texLen)[0]
                f.read(1)
                image = f.read(texLen)
                f.read(1)
                images[texName] = image
        command = f.read(4)
    return json, images

def write_mrr(filename, json, textures):
    file = open(filename, "wb")
    file.write(bytearray('MRROBOTTOFILE\n', encoding='ascii'))
    file.write(bytearray('JSON',encoding='ascii'))
    file.write(struct.pack('>I',len(json)))
    file.write(bytearray('\n',encoding='ascii'))
    file.write(bytearray(json, encoding='ascii'))
    file.write(bytearray('\n',encoding='ascii'))
    if len(textures) > 0:
        file.write(bytearray('TEXT',encoding='ascii'))
        file.write(struct.pack('>I',len(textures)))
        file.write(bytearray('\n',encoding='ascii'))
        for item in textures.items():
            #f = open(item[1],'rb')
            #image = f.read()
            image = item[1]
            file.write(bytearray('NAME',encoding='ascii'))
            file.write(struct.pack('>I',len(item[0])))
            file.write(bytearray(item[0],encoding='ascii'))
            file.write(struct.pack('>I',len(image)))
            file.write(bytearray('\n',encoding='ascii'))
            file.write(image)
            file.write(bytearray('\n',encoding='ascii'))
            #f.close()
    file.write(bytearray('FNSH',encoding='ascii'))
    file.close()