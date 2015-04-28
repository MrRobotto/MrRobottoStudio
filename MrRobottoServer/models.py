import os
import json
from django.http import HttpResponse
from MrRobottoServer import settings
from utils import get_abs_path, get_directory

SETTINGS_FILE = "settings.json"

def save_to_settings(obj):
    try:
        f = open(SETTINGS_FILE)
    except:
        f = open(SETTINGS_FILE, "w")
        f.close()
    f = open(SETTINGS_FILE)
    try:
        d = json.loads(f.read())
    except:
        d = dict()
    f.close()
    if isinstance(obj,BlenderExe):
        d["BlenderExe"] = obj.__dict__
    elif isinstance(obj,BlenderFile):
        d["BlenderFile"] = obj.__dict__
    f = open(SETTINGS_FILE,"w")
    f.write(json.dumps(d))
    f.close()

def load_from_settings(obj):
    f = open(SETTINGS_FILE)
    d = json.loads(f.read())
    f.close()
    if isinstance(obj,BlenderExe) and "BlenderExe" in d:
        obj.__dict__ = d["BlenderExe"]
    elif isinstance(obj,BlenderFile) and "BlenderFile" in d:
        obj.__dict__ = d["BlenderFile"]


class AndroidConnection:
    def __init__(self):
        self.response = HttpResponse(status=200)
        self.updated = False
        self.connected = False
        self.ua = None
    def connect(self, ua):
        self.ua = ua
        #self.response = HttpResponse(status=200)
        self.connected = True
        self.updated = False
    def update(self, data):
        self.response.content = data
        self.updated = True
    def disconnect(self):
        self.ua = None
        self.response = None
        self.updated = False
        self.connected = False

android_connection = AndroidConnection()

def get_android_connection():
    global android_connection
    return android_connection


class BlenderExe:
    def __init__(self):
        self.path, self.file = self.__get_blender()
        if self.path is not None and self.file is not None:
            self.abspath = get_abs_path(self.path, self.file)
            save_to_settings(self)
    def __find_blender_nt(self):
        dirs = ["C:\\Program Files", "C:\\Program Files (x86)"]
        for dir in dirs:
            gen = os.walk(dir)
            programs = gen.next()[1]
            for prog in programs:
                if 'blender' in prog.lower().split():
                    blender_dir =  get_abs_path(dir, prog)
                    walker = os.walk(blender_dir)
                    for w in walker:
                        for p in w[2]:
                            if p == 'blender.exe':
                                return (w[0],p)
                        #if 'blender.exe' in w[2]:
                        #    return
                            #return get_abs_path(w[0],'blender.exe')
    def __get_blender(self):
        load_from_settings(self)
        if self.abspath:
            return self.path, self.file
        if os.name == 'nt':
            blender = self.__find_blender_nt()
            if blender is not None:
                return blender
            else:
                None, None
        else:
            None, None

    def restore(self):
        self.path, self.file = self.__get_blender()
        self.abspath = get_abs_path(self.path, self.file)

    def navigate_to_path(self, path):
        self.file = None
        self.abspath = None
        self.path = get_abs_path(get_blender_search_dir(), path)

    def set_blender_path(self, path):
        self.file = None
        self.abspath = None
        self.path = path

    def set_blender_exe(self, exe):
        self.file = exe
        self.abspath = get_abs_path(self.path, self.file)
        save_to_settings(self)

    def get_abspath(self):
        return self.abspath

blender_exe = BlenderExe()

def get_blender_exe():
    global blender_exe
    return blender_exe





class BlenderFile:
    def __init__(self):
        self.path = settings.BASE_DIR
        self.file = None
        self.file_abspath = None
        self.exported = False
        self.json = None
        self.json_abspath = None
        load_from_settings(self)
    def __flush(self):
        self.file = None
        self.file_abspath = None
        self.exported = False
        self.json = None
        self.json_abspath = None
    def get_path(self):
        return self.path
    def navigate_to_path(self, path):
        self.__flush()
        self.path = get_abs_path(self.path, path)
    def set_blend_file(self, f):
        self.file = f
        self.file_abspath = get_abs_path(self.path, self.file)
        json = self.file.split('.')[0]+".json"
        if json in get_directory(self.path)[2]:
            self.export()
        save_to_settings(self)
    def get_abspath(self):
        return self.file_abspath
    def get_json_abspath(self):
        return self.json_abspath
    def export(self):
        self.exported = True
        self.json = self.file.split('.')[0] + ".json"
        self.json_abspath = get_abs_path(self.path, self.json)
        save_to_settings(self)


blender_file = BlenderFile()

def get_blender_file():
    global blender_file
    return blender_file






blender_search_dir = settings.BASE_DIR

def get_blender_search_dir():
    global blender_search_dir
    return blender_search_dir

def set_blender_search_dir(dir):
    global blender_search_dir
    blender_search_dir = get_abs_path(blender_search_dir, dir)



