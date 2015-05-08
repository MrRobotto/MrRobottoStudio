import os
import settings
import utils
from utils import *
import json

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
    d[obj.__class__.__name__] = obj.__dict__
    f = open(SETTINGS_FILE,"w")
    f.write(json.dumps(d))
    f.close()

def load_from_settings(obj):
    try:
        f = open(SETTINGS_FILE)
    except:
        return False
    d = json.loads(f.read())
    f.close()
    if obj.__class__.__name__ in d:
        obj.__dict__ = d[obj.__class__.__name__]
        return True
    return False


class FileSystemNavigator:
    def __init__(self, dir=None):
        if dir is not None:
            self.dir_path = get_abs_path(dir)
        else:
            if not load_from_settings(self):
                self.dir_path = get_abs_path(settings.BASE_DIR)
                save_to_settings(self)
    def navigate_to(self, des):
        self.dir_path = get_abs_path(os.path.join(self.dir_path,des))
        save_to_settings(self)
    def get_directory_folders(self):
        return get_directory(self.dir_path)[1]
    def get_directory_files(self):
        return get_directory(self.dir_path)[2]
    def dir_contains_file(self, filename):
        return filename in self.get_directory_files()

class FileData:
    def __init__(self, dir=None, f=None):
        self.dir_path = None
        self.file = None
        self.file_path = None
        if dir is not None and f is not None:
            self.setFile(dir, f)
        elif dir is not None and f is None:
            self.dir_path = dir
        elif dir is None and f is None:
            if not load_from_settings(self):
                self.dir_path = settings.BASE_DIR
                save_to_settings(self)
    def setFile(self, dir, f):
        self.dir_path = get_abs_path(dir)
        self.file = f
        self.file_path = get_abs_path(dir, f)
        save_to_settings(self)
    def get_file_base_name(self):
        return self.file.split('.')[0]
    def __repr__(self):
        return self.file

class BlenderExe(FileData):
    def __init__(self, dir=None, f=None):
        if dir == None and f == None:
            dir, f = self.__find_blender()
        FileData.__init__(self,dir,f)
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
    def __find_blender(self):
        if os.name == 'nt':
            blender = self.__find_blender_nt()
            if blender is not None:
                return blender
            else:
                None, None
        else:
            None, None

class BlendFile(FileData):
    def __init__(self, dir=None, f=None):
        FileData.__init__(self, dir, f)

class MRRFile(FileData):
    def __init__(self, dir=None, f=None):
        FileData.__init__(self, dir, f)
        if not 'exported' in self.__dict__:
            self.exported = False
    def export(self):
        self.exported = True
        save_to_settings(self)
    def decode(self):
        return utils.decode_mrr(self.file_path)