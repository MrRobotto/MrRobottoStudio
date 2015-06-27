import os
import json
from django.db import models
from django.utils import timezone
from MrRobottoStudioServer import settings
import MrRobottoStudioServer.utils as utils

class FileSystemNavigatorManager(models.Manager):
    def get_or_create_fsn_of(self, dir_path=settings.BASE_DIR, explorer="", filters=""):
        res = self.filter(explorer=explorer)
        if res:
            return res.first()
        else:
            p = utils.get_abs_path(dir_path)
            fsn = self.create(dir_path=p, explorer=explorer, filters=filters)
            return fsn
    def get_or_create_blenderexe_fsn(self):
        return self.get_or_create_fsn_of(explorer="blender", filters=".exe")
    def get_or_create_blendfile_fsn(self):
        return self.get_or_create_fsn_of(explorer="blendfile", filters=".blend")


class FileSystemNavigator(models.Model):
    dir_path = models.FilePathField()
    explorer = models.CharField(primary_key=True, max_length=50, default="")
    filters = models.CharField(max_length=50, default="")
    objects = FileSystemNavigatorManager()
    def navigate_to(self, dest):
        self.dir_path = utils.get_abs_path(os.path.join(self.dir_path, dest))
        self.save()
    def get_folders_and_files(self):
        resFiles = list()
        dirname, folders, files = utils.get_directory(self.dir_path)
        filters = str(self.filters).split(" ")
        for filter in filters:
            resFiles.extend(utils.file_filter(files, filter))
        resFiles.sort()
        return folders, resFiles
    def contains_file(self, filename):
        return filename in self.get_files()
    def as_dict(self):
        d = dict()
        d['dir_path'] = self.dir_path
        d['folders'], d['files'] = self.get_folders_and_files()
        d['explorer'] = self.explorer
        return d


class FileDataManager(models.Manager):
    def get_or_create_filedata(self, file_type="", dir_path=None, file=None):
        if dir_path == None or file == None:
            return None
        p = utils.get_abs_path(dir_path)
        if  p == None:
            return None
        file_path = utils.get_abs_path(p, file)
        if file_path == None:
            return None
        res = self.filter(file_type=file_type, file_path=file_path).first()
        if res:
            res.access_time = timezone.now()
            res.save()
            return res
        else:
            fd = self.create(file_type=file_type, dir_path=p, file=file, file_path=file_path)
            return fd
    def get_or_create_blenderexe(self, dir_path=None, file=None):
        if dir_path is not None and file is not None:
            return self.get_or_create_filedata(file_type="blender",dir_path=dir_path, file=file)
        res = self.filter(file_type="blender").order_by("-access_time").first()
        if res is not None:
            res.access_time = timezone.now()
            res.save()
            return res
        p, f = self.__find_blender()
        return self.get_or_create_filedata(file_type="blender",dir_path=p, file=f)
    def get_or_create_blendfile(self, dir_path=None, file=None):
        if dir_path == None and file == None:
            res = self.filter(file_type="blendfile").order_by("-access_time").first()
            if res is not None:
                res.access_time = timezone.now()
                res.save()
                return res
        return self.get_or_create_filedata(file_type="blendfile",dir_path=dir_path, file=file)
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

class FileData(models.Model):
    file_type = models.CharField(max_length=30, default="")
    dir_path = models.FilePathField()
    file_path = models.FilePathField()
    file = models.CharField(max_length=50, default="")
    access_time = models.DateTimeField(default=timezone.now)
    objects = FileDataManager()
    def get_file_base_name(self):
        return self.file.split('.')[0]
    def __repr__(self):
        return self.file
    def as_dict(self):
        d = dict()
        d['dir_path'] = self.dir_path
        d['file_path'] = self.file_path
        d['file'] = self.file
        d['file_base_name'] = self.get_file_base_name()
        d['access_time'] = self.access_time
        d['file_type'] = self.file_type
        return d

class MrrFile:
    def __init__(self, blend_file):
        f = blend_file.get_file_base_name()+".mrr"
        file_path = utils.get_abs_path(blend_file.dir_path, f)
        self.file_path = file_path
        self.last_modification = utils.get_modification_time(file_path)
        self.textures = dict()
        self.mainDict = dict()
        self.reduced = list()
        self.load_file()
    def load_file(self):
        jsonStr, self.textures = utils.decode_mrr(self.file_path)
        self.mainDict = json.loads(jsonStr)
        self.create_reduced()
        self.last_modification = utils.get_modification_time(self.file_path)
    def create_reduced(self):
        self.reduced = list()
        for obj in self.mainDict['SceneObjects']:
            d = obj.copy()
            if "Mesh" in d:
                d.pop("Mesh")
            self.reduced.append(d)
    def update(self, objectsJson):
        objs = json.loads(objectsJson)
        d = {e['Name']: e for e in self.mainDict['SceneObjects']}
        for name, obj in objs.items():
            d[name].update(obj)
        jsonStr = self.__create_json_from_dict(self.mainDict)
        self.create_reduced()
        utils.write_mrr(self.file_path, jsonStr, self.textures)
        self.last_modification = utils.get_modification_time(self.file_path)
    def __create_json_from_dict(self, d):
        return json.dumps(d, indent = None, separators = (',',':'), sort_keys = True)
    def get_json(self):
        if not self.last_modification == utils.get_modification_time(self.file_path) or self.mainDict is None:
            self.load_file()
        d = {e['Name']: {'json': json.dumps(e, indent = None, separators = (',',':'), sort_keys = True), 'obj': e} for e in self.reduced}
        return d
    def get_textures(self):
        if not self.last_modification == utils.get_modification_time(self.file_path) or self.textures is None:
            self.load_file()
        return self.textures
    def as_dict(self):
        d = dict()
        d['file_path'] = self.file_path
        d['objects_dict'] = self.get_json()
        d['reduced'] = self.reduced
        return d

class AndroidDeviceManager(models.Manager):
    def get_or_create_device(self, model_name):
        res = self.filter(model_name=model_name)
        if res:
            res = res.first()
            res.connect()
            return res
        return self.create(model_name=model_name)
    def get_last_android(self):
        devices = self.order_by("-last_connection")
        if devices:
            return devices.first()
        else:
            return None

class AndroidDevice(models.Model):
    model_name = models.TextField(primary_key=True)
    is_connected = models.BooleanField(default=True)
    need_update = models.BooleanField(default=False)
    last_connection = models.DateTimeField(auto_now=True)
    objects = AndroidDeviceManager()
    def connect(self):
        self.is_connected = True
        self.last_connection = timezone.now()
        self.need_update = True
        self.save()
    def disconnect(self):
        self.is_connected = False
        self.need_update = True
        self.save()
    def update(self):
        self.need_update = True
        self.save()
    def updated(self):
        self.need_update = False
        self.save()