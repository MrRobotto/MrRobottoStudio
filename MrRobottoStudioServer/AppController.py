import os
import json
import MrRobottoStudioServer.settings as settings
import MrRobottoStudioServer.utils as utils


SETTINGS_FILE = "settings.json"

def save_to_settings(obj, dictionary=None):
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
    if dictionary is not None:
        d[obj.__class__.__name__] = dictionary
    else:
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
            self.dir_path = utils.get_abs_path(dir)
        else:
            if not load_from_settings(self):
                self.dir_path = utils.get_abs_path(settings.BASE_DIR)
                save_to_settings(self)
    def navigate_to(self, des):
        self.dir_path = utils.get_abs_path(os.path.join(self.dir_path,des))
        save_to_settings(self)
    def get_directory_folders(self):
        return utils.get_directory(self.dir_path)[1]
    def get_directory_files(self):
        return utils.get_directory(self.dir_path)[2]
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
        self.dir_path = utils.get_abs_path(dir)
        self.file = f
        self.file_path = utils.get_abs_path(dir, f)
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
            programs = next(gen)[1]
            for prog in programs:
                if 'blender' in prog.lower().split():
                    blender_dir = utils.get_abs_path(dir, prog)
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
            self.last_modification = None
        self.jsonStr = None
        self.textures = None
        self.d = None
        self.objects = None
        self.objects_json = None
    def __create_json_objects(self):
        self.objects = []
        for obj in self.d['SceneObjects']:
            d = obj.copy()
            if "Mesh" in d:
                d.pop("Mesh")
            self.objects.append(d)
        self.objects_json = {e['Name']: {'json': json.dumps(e), 'obj': e} for e in self.objects}
    def __save_to_settings(self):
        d = self.__dict__.copy()
        d.pop('jsonStr')
        d.pop('textures')
        d.pop('d')
        d.pop('objects')
        d.pop('objects_json')
        save_to_settings(self, d)
    def __save_to_mrr(self):
        utils.write_mrr(self.file_path, self.jsonStr, self.textures)
    def export(self):
        self.exported = True
        self.jsonStr, self.textures = utils.decode_mrr(self.file_path)
        self.last_modification = utils.get_modification_time(self.file_path)
        self.d = json.loads(self.jsonStr)
        self.__create_json_objects()
        self.__save_to_settings()
    def update(self, objectsJson):
        objs = json.loads(objectsJson)
        d = {e['Name']: e for e in self.d['SceneObjects']}
        for name, obj in objs.items():
            d[name].update(obj)
        self.jsonStr = json.dumps(self.d, indent = None, separators = (',',':'), sort_keys = True)
        self.__create_json_objects()
        self.__save_to_mrr()
        self.__save_to_settings()
    def get_json(self):
        if not self.last_modification == utils.get_modification_time(self.file_path) or self.jsonStr is None:
            self.export()
        return self.jsonStr
    def get_textures(self):
        if not self.last_modification == utils.get_modification_time(self.file_path) or self.textures is None:
            self.export()
        return self.textures


class SceneObjectsList:
    def __init__(self, mrrFile=None):
        if mrrFile is not None:
            self.set_mrrfile(mrrFile)
        if not load_from_settings(self):
            self.d = None
            self.objects = None
            self.objects_json = None
    def __createJsonObjects(self):
        self.objects = self.d['SceneObjects'].copy()
        for obj in self.objects:
            if "Mesh" in obj:
                obj.pop("Mesh")
        self.objects_json = {e['Name']: {'json': json.dumps(e), 'obj': e} for e in self.objects}
    def set_mrrfile(self, mrrFile):
        self.d = json.loads(mrrFile.get_json())
        self.__createJsonObjects()
        save_to_settings(self)
    def update(self, objectsJson):
        objs = json.loads(objectsJson)
        d = {e['Name']: e for e in self.d['SceneObjects']}
        for name, obj in objs.items():
            d[name].update(obj)
        self.__createJsonObjects()

        save_to_settings(self)
    def get_objects_names(self):
        return self.objects.keys()
    def get_shader_program(self, name):
        return self.objects[name]