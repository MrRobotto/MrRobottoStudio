import os
import settings
from utils import *

class FileSystemNavigator:
    def __init__(self, dir=None):
        if dir == None:
            self.current_dir = get_abs_path(settings.BASE_DIR)
        else:
            self.current_dir = get_abs_path(dir)
    def navigate_to(self, des):
        self.current_dir = get_abs_path(des)
    def get_directory_folders(self):
        return get_directory(self.current_dir)[1]
    def get_directory_files(self):
        return get_directory(self.current_dir)[2]
    def dir_contains_file(self, filename):
        return filename in self.get_directory_files()

class FileData:
    def __init__(self, dir=None, f=None):
        self.current_dir = None
        self.file = None
        self.file_path = None
        if dir is not None and f is not None:
            self.setFile(dir, f)
    def setFile(self, dif, f):
        self.current_dir = get_abs_path(dir)
        self.file = f
        self.file_path = get_abs_path(dir, f)
    def get_file_name(self):
        return self.file.split('.')[0]

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

class BlendFile:
    def __init__(self, dir=None, f=None):
        self.blend_file = FileData(dir, f)
        self.json_file = FileData(self.blend_file.get_file_name()+".json")