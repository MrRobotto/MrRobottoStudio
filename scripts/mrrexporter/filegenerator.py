from commons import *
from models import *
from exporters import *
            
def prettyPrintJSON(scene):
    """Pretty printing long lists"""
    #All lists with a key inside "keys" will be printed in one row
    keys=["VertexData","IndexData","Location","Rotation","Scale","Local2World","Up","Forward","Right","ClearColor","Color","BoneOrder"]
    st = json.dumps(scene, indent = 4, separators = (',',':'), sort_keys = True, cls = SceneJSONEncoder)
    spl = st.splitlines()
    r = ""
    i = 0
    keyFound = False
    jsonKeys = ["\""+k+"\"" for k in keys]
    while i < len(spl):
        for k in jsonKeys:
            if spl[i].find(k) >= 0:
                keyFound = True
                break
        if spl[i].find("[]") >= 0 and keyFound:
            r = r+spl[i]+"\n"
            i = i+1
            keyFound = False
        elif spl[i].find("[") >= 0 and keyFound:
            r = r + spl[i]
            i = i+1
            while spl[i].find("]") < 0:
                r = r + spl[i].split()[0]
                i = i+1
            r = r+spl[i].split()[0]+"\n"
            i = i+1
            keyFound = False
        else:
            r = r+spl[i]+"\n"
            i = i+1
    return r

def writeToFile(filename, content):
    file = open(filename,"w")
    file.write(content)
    file.close()

def writeToFile2(filename, json, textures):
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
            f = open(item[1],'rb')
            image = f.read()
            file.write(bytearray('NAME',encoding='ascii'))
            file.write(struct.pack('>I',len(item[0])))
            file.write(bytearray(item[0],encoding='ascii'))
            file.write(struct.pack('>I',len(image)))
            file.write(bytearray('\n',encoding='ascii'))
            file.write(image)
            file.write(bytearray('\n',encoding='ascii'))
            f.close()
    file.write(bytearray('FNSH',encoding='ascii'))
    file.close()

class SceneJSONEncoder(json.JSONEncoder):
    def default(self,obj):
        #All elements in listTypes will be serialized as lists
        listTypes = (Vertex,AttributeKeyList,Vector,Quaternion,Matrix,AttributeList,UniformList, MaterialList, UniformKeyList,Color)
        #All elements in dictTypes will be serialized as dicts
        dictTypes = [AttributeKey, Mesh, Model, Transform, Scene, Camera, Lens, ShaderProgram, Attribute, UniformKey]
        dictTypes += [Uniform, SceneObjectsList, Hierarchy, HierarchyObject, Material, MaterialLight,Texture, Action, Skeleton]
        dictTypes += [Frame, PoseBone, Bone, BoneIndex, Light]
        dictTypes = tuple(dictTypes)
        if isinstance(obj,dictTypes):
            return dict(obj)
        if isinstance(obj,listTypes):
            return list(obj)
        json.JSONEncoder.default(self, obj)


class Exporter:
    sceneObjectsList = SceneObjectsList()

    def __init__(self):
        #self.filepath = bpy.path.abspath(D.filepath).replace(bpy.path.basename(D.filepath),"")
        self.filename = os.path.splitext(D.filepath)[0]

    def export(self):
        SceneObjectsListExporter(D.objects,Exporter.sceneObjectsList).export()
        sceneJson = json.dumps(Exporter.sceneObjectsList, indent = None, separators = (',',':'), sort_keys = True, cls = SceneJSONEncoder)
        #writeToFile(self.filename + EXT, prettyPrintJSON(sceneObjectsList))
        #writeToFile(self.filename + EXT, json.dumps(Exporter.sceneObjectsList, indent = None, separators = (',',':'), sort_keys = True, cls = SceneJSONEncoder))
        #writeToFile(self.filename + EXT, sceneJson)
        #writeToFile(self.filename + EXT, prettyPrintJSON(Exporter.sceneObjectsList))
        writeToFile2(self.filename + '.mrr', sceneJson, Exporter.sceneObjectsList.textures)
        
class Exporter2:
    def __init__(self, objName):
        #self.filepath = bpy.path.abspath(D.filepath).replace(bpy.path.basename(D.filepath),"")
        #self.filename = os.path.splitext(D.filepath)[0]
        self.filename = os.path.splitext(D.filepath)[0] + "_" + objName
        self.objName = objName
        
    def getTexture(self, obj):
        textures = dict()
        if obj.Type == SCENEOBJTYPE_MODEL:
            for mat in obj.Materials:
                if mat.hasTexture():
                    textures[mat.Texture.Name] = mat.Texture.path
        return textures
            
    def export(self):
        #SceneObjectsListExporter(D.objects,Exporter.sceneObjectsList).export()
        #sceneJson = json.dumps(Exporter.sceneObjectsList, indent = None, separators = (',',':'), sort_keys = True, cls = SceneJSONEncoder)
        obj = SceneObjectExporter2(self.objName, D.objects).export()
        if obj is not None:
            objJson = json.dumps(obj, indent = None, separators = (',',':'), sort_keys = True, cls = SceneJSONEncoder)
            writeToFile2(self.filename + '.mrr', objJson, self.getTexture(obj))
        
class Executor:
    def __init__(self):
        self.queue = list()
        self.numProcess = 0
        self.maxProcess = multiprocessing.cpu_count() + 1
        self.process = list()
    def addCmd(self, cmd):
        self.queue.append(cmd)
    def nextCmd(self):
        if len(self.queue) > 0:
            return self.queue.pop(0)
        return None
    def waitExecOne(self):
        while self.numProcess >= self.maxProcess:
            for p in self.process:
                p.poll()
            self.process = [p for p in self.process if p.returncode == None]
            self.numProcess = len(self.process)
    def waitExecAll(self):
        while self.numProcess > 0:
            for p in self.process:
                p.wait()
            self.process = [p for p in self.process if p.returncode == None]
            self.numProcess = len(self.process)
    def executeAll(self):
        while len(self.queue) > 0:
            cmd = self.nextCmd()
            self.waitExecOne()
            if cmd == None:
                self.waitExecAll()
                return
            else:
                p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL)
                self.process.append(p)
                self.numProcess = len(self.process)


