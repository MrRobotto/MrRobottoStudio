from commons import *

class Vertex:
    """Main vertex class"""
    def __init__(self, index, co, normal, mat=None, uv=None, w=None, bind=None):
        self.mainIndex = index
        self.index = index
        self.co = co
        self.normal = normal
        self.mat = mat
        self.uv = uv
        self.w = w
        self.bind = bind
    def __hash__(self):
        """It is hashed by its main index"""
        return self.mainIndex
    def __lt__(self,v):
        """And checked by index"""
        return self.index < v.index
    def __gt__(self,v):
        return self.index > v.index
    def __eq__(self,v):
        """But they are only equals if all they attributes are equals"""
        if self.mainIndex != v.mainIndex:
            return False
        elif not cmpVec(self.co,v.co):
            return False
        elif not cmpVec(self.normal,v.normal):
            return False
        elif self.mat != v.mat:
            return False
        elif not cmpVec(self.uv,v.uv):
            return False
        elif not cmpVec(self.w,v.w):
            return False
        elif not cmpVec(self.bind,v.bind):
            return False
        else:
            return True
    def __repr__(self):
        return "Vertex("+str(self.index)+")"
    def __iter__(self):
        """We represent a vector as a list, following the ORDER constant defined"""
        #TODO: set the order in function of bufferkeys
        l = list()
        l.extend(self.co)
        l.extend(self.normal)
        if self.mat != None:
            l.append(self.mat)
        if self.uv != None:
            l.extend(self.uv)
        if self.w != None:
            l.extend(self.w)
        if self.bind != None:
            l.extend(self.bind)
        l = [mround(e) for e in l]
        yield from l

class Face:
    """Contains the vertices of a fece, they must be three"""
    def __init__(self):
        self.verts = []
    def __repr__(self):
        return "Face("+str(tuple(self.verts))+")"
    def __getitem__(self,key):
        return self.verts[key]
    def __iter__(self):
        yield from self.verts
    @property
    def v1(self):
        return self.verts[0]
    @v1.setter
    def v1(self, value):
        self.verts[0] = value
    @property
    def v2(self):
        return self.verts[1]
    @v2.setter
    def v2(self, value):
        self.vers[1] = value
    @property
    def v3(self):
        return self.verts[2]
    @v3.setter
    def v3(self, value):
        self.verts[2] = value
    def addVert(self,v):
        if len(self.verts) >= 3:
            raise Exception("Face must have 3 vertices")
        self.verts.append(v)


class GeometryList:
    def __init__(self):
        self.vertices = set()
        self.baseMap = dict()
        self.indices = set()
        self.tail = list()
        self.base = set()
        self.faces = []
        self.count = 0
    def addFace(self,v1,v2,v3):
        u1 = self.addVert(v1)
        u2 = self.addVert(v2)
        u3 = self.addVert(v3)
        self.faces.extend([u1,u2,u3])
    def getNumFaces(self):
        return len(self.faces)
    def getNumVertices(self):
        return len(self.vertices)
    def addVert(self, v):
        if not v.mainIndex in self.indices or not v in self.vertices:
            if not v.mainIndex in self.indices:
                self.indices.add(v.mainIndex)
                self.count = max(self.count,v.mainIndex)
                self.base.add(v)
                self.baseMap[v.index] = v
            else:
                self.tail.append(v)
            for i in range(len(self.tail)):
                self.tail[i].index = self.count + i
            self.vertices.add(v)
            return v
        else:
            if v in self.base:
                return self.baseMap[v.index]
            for u in self.tail:
                if u == v:
                    return u
            #for u in self.vertices:
            #    if u == v:
            #        return u
    def checkGeometry(self):
        if len(self.base) != self.count:
            self.count = len(self.base)
            verts = list(self.base)
            verts.sort()
            for i in range(len(verts)):
                verts[i].index = i
            for i in range(len(self.tail)):
                self.tail[i].index = self.count + i
    def getFaceIndices(self):
        self.checkGeometry()
        return [v.index for v in self.faces]
    def getVertices(self):
        self.checkGeometry()
        verts = list(self.vertices)
        verts.sort()
        return [e for v in verts for e in list(v)]



#TODO: Remove Name and Index
class AttributeKey:
    """AttributeKey class for saving OGL attributes in an standard format"""
    def __init__(self, AttributeName, DataSize, DataType):
        self.Attribute = AttributeName
        self.Size = DataSize
        self.DataType = DataType
        self.Pointer = 0
        self.Stride = 0
    def __hash__(self):
        return hash(self.Attribute)
    def __eq__(self,k):
        return k.Attribute == self.Attribute
    def __lt__(self,k):
        return ORDER[self.Attribute] < ORDER[k.Attribute]
    def __gt__(self,k):
        return ORDER[self.Attribute] > ORDER[k.Attribute]
    def __iter__(self):
        yield from self.__dict__.items()
    def getDataSize(self):
        return getDataSize(self.DataType)

#TODO: Change lists for hash
class AttributeKeyList:
    def __init__(self):
        self.keys = dict()
        self.attributes = set()
        self.stride = 0
    def asList(self):
        keylist = list(self.keys.values())
        keylist.sort()
        return keylist
    def __iter__(self):
        yield from self.asList()
    def hasAttribute(self, attr):
        return attr in self.keys.keys()
    def getKey(self, attrName):
        if attrName in self.keys:
            return self.keys[attrName]
        return None
    def addKey(self,key):
        #When we add a key we need to change the stride of all keys in that list
        #because if we have something like [V1,V2,V2,UV1,UV2] (stride = 3+2=5)
        #and we add normals we will have [V1,V2,V3,N1,N2,N3,UV1,UV2] (stride = 3+3+2=8)
        #if self.hasAttribute(key):
        self.keys[key.Attribute] = key
        keylist = self.asList()
        stride = sum([k.Size for k in keylist])
        aux = 0
        for k in keylist:
            k.Pointer = aux
            k.Stride = stride
            aux += k.Size
    def removeKey(self, keyName):
        self.keys.pop(keyName)
        keylist = self.asList()
        stride = sum([k.Size for k in keylist])
        aux = 0
        for k in keylist:
            k.Pointer = aux
            k.Stride = stride
            aux += k.Size

class Mesh:
    def __init__(self, drawType=DRAWTYPE_TRIANGLES):
        self.DrawType = drawType
        self.AttributeKeys = AttributeKeyList()
        self.IndexData = list()
        self.VertexData = list()
        self.Count = 0
        self.Name = None
        #This is declarated just for not repeat an expensive operation over and over
        self._materialIndices = None
        self._boneIndices = None
    def __iter__(self):
        #And it must be removed from mesh
        d = self.__dict__.copy()
        d.pop('_materialIndices')
        d.pop('_boneIndices')
        yield from d.items()
    def addKey(self,key):
        self.AttributeKeys.addKey(key)
    def hasKey(self,attrName):
        return self.AttributeKeys.hasAttribute(attrName)
    def getBoneIndices(self):
        return self._boneIndices
    def getMaterialIndices(self):
        return self._materialIndices



class Uniform:
    def __init__(self, Uniform, Name, Count, DataType):
        self.Name = Name
        self.Uniform = Uniform
        self.DataType = DataType
        self.Count = Count
    def __iter__(self):
        yield from self.__dict__.items()
    def __repr__(self):
        if self.DataType == DATATYPE_SAMPLER2D and self.Count > 1:
            for i in range(self.Count):
                s = "uniform "+self.DataType+ " " + self.Name + "_" + str(i) + ";"
                return s
        else:
            s = "uniform "+self.DataType + " " + self.Name
            if self.Count > 1:
                s += "["+str(self.Count)+"]"
            s += ";"
            return s

class UniformKey:
    def __init__(self, Generator, Uniform, level, Count = 1, Index = 0):
        self.Generator = Generator
        self.Uniform = Uniform
        self.Level = level
        self.Count = Count
        self.Index = Index
        if self.Index > 0:
            self.Uniform += "_"+str(self.Index)
        self.uniformName = None
        self.uniformDataType = None
    def getCount(self):
        return self.Count
    def getUniform(self):
        if self.Index > 0:
            self.uniformName += str(self.Index)
        return Uniform(self.Uniform, self.uniformName, self.Count, self.uniformDataType)
    def __iter__(self):
        d = self.__dict__.copy()
        d.pop('uniformName')
        d.pop('uniformDataType')
        yield from d.items()

class UniformKeyList:
    def __init__(self):
        self.uniforms = list()
        self.byGenType = dict()
    def addUniformKey(self, uniformKey):
        self.uniforms.append(uniformKey)
        if not uniformKey.Generator in self.byGenType:
            self.byGenType[uniformKey.Generator] = [uniformKey]
        else:
            self.byGenType[uniformKey.Generator].append(uniformKey)
    def getByGenerator(self, generator):
        return self.byGenType[generator]
    def __iter__(self):
        yield from self.uniforms

class Attribute:
    def __init__(self, AttributeName, Name, Index, DataType):
        self.Attribute = AttributeName
        self.Name = Name
        self.Index = Index
        self.DataType = DataType
    def __hash__(self):
        return hash(self.Attribute)
    def __eq__(self,k):
        return k.Attribute == self.Attribute
    def __lt__(self,k):
        return ORDER[self.Attribute] < ORDER[k.Attribute]
    def __gt__(self,k):
        return ORDER[self.Attribute] > ORDER[k.Attribute]
    def __iter__(self):
        yield from self.__dict__.items()
    def __repr__(self):
        s = "attribute "+self.DataType + " " + self.Name +";"
        return s

class UniformList:
    def __init__(self):
        self.uniforms = {}
    def addUniform(self, uniform):
        self.uniforms[uniform.Name] = uniform
    def __iter__(self):
        yield from self.uniforms.values()

class AttributeList:
    def __init__(self):
        self.attributes = {}
    def addAttribute(self, attr):
        self.attributes[attr.Attribute] = attr
    def __iter__(self):
        yield from self.attributes.values()

class ShaderProgram:
    def __init__(self, Name, configurer, vssource, fssource):
        self.Name = Name
        self.configurer = configurer
        attributes = configurer.attributes.values()
        uniforms = configurer.getUniforms()
        self.VertexShaderSource = vssource
        self.FragmentShaderSource = fssource
        self.Attributes = AttributeList()
        self.Uniforms = UniformList()
        for attr in attributes:
            self.addAttribute(attr)
        for unif in uniforms:
            self.addUniform(unif)
    def addUniform(self, uniform):
        self.Uniforms.addUniform(uniform)
    def addAttribute(self, attr):
        self.Attributes.addAttribute(attr)
    def __iter__(self):
        d = self.__dict__.copy()
        d.pop("configurer")
        yield from d.items()





class Transform:
    def __init__(self):
        self.Location = Vector((0,0,0))
        self.Rotation = Quaternion((1,0,0,0))
        self.Scale = Vector((1,1,1))
    def __iter__(self):
        yield from self.__dict__.items()


class MaterialLight:
    def __init__(self, intensity, color):
        self.Intensity = intensity
        self.Color = color
    def __iter__(self):
        yield from self.__dict__.items()

class Material:
    def __init__(self, name, diffuse, specular, ambient, texture = None):
        self.Name = name
        self.Diffuse = diffuse
        self.Specular = specular
        self.Ambient = ambient
        self.Texture = texture
    def hasTexture(self):
        return self.Texture is not None
    def __iter__(self):
        yield from self.__dict__.items()

class MaterialList:
    def __init__(self):
        self.Materials = list()
    def addMaterial(self, material):
        self.Materials.append(material)
    def __len__(self):
        return len(self.Materials)
    def __iter__(self):
        yield from self.Materials

class Texture:
    def __init__(self, name, minFilter=TEXMINFILTER_LINEAR, magFilter=TEXMAGFILTER_LINEAR, index=DEFAULT_TEXTURE_INDEX, path=None):
        self.Name = name
        self.MinFilter = minFilter
        self.MagFilter = magFilter
        self.Index = index
        #Remove from export
        self.path = path
    def __iter__(self):
        d = self.__dict__.copy()
        d.pop('path')
        yield from d.items()



class SceneObj:
    def __init__(self, name, sceneType):
        self.Type = sceneType
        self.Name = name
        self.Transform = Transform()
        self.UniformKeys = UniformKeyList()
        self.ShaderProgram = None
    def setName(self, name):
        self.Name = cleanName(name)
    def __iter__(self):
        yield from self.__dict__.items()




class Scene(SceneObj):
    def __init__(self, clearColor = SCENE_CLEARCOLOR):
        SceneObj.__init__(self, DEFAULT_NAME_SCENE, SCENEOBJTYPE_SCENE)
        self.ClearColor = clearColor
        self.AmbientLightColor = None




class Model(SceneObj):
    def __init__(self):
        SceneObj.__init__(self, DEFAULT_NAME_MODEL, SCENEOBJTYPE_MODEL)
        self.Mesh = Mesh()
        self.Materials = MaterialList()
        self.Skeleton = None



class Lens:
    def __init__(self, Type):
        self.Type = Type
    def __iter__(self):
        yield from self.__dict__.items()

class PerspectiveLens(Lens):
    def __init__(self):
        Lens.__init__(self, LENS_PERSPECTIVE)
        self.FOV = 0
        self.AspectRatio = 0
        self.ClipStart = 0
        self.ClipEnd = 0

class OrthographicLens(Lens):
    def __init__(self):
        Lens.__init__(self, LENS_ORTHOGRAPHIC)
        self.OrthographicScale = 0

class Camera(SceneObj):
    def __init__(self):
        SceneObj.__init__(self, DEFAULT_NAME_CAMERA, SCENEOBJTYPE_CAMERA)
        self.Lens = None



class PoseBone:
    def __init__(self, name, scale, rotation, location):
        self.Name = name
        self.Rotation = rotation
        self.Location = location
        self.Scale = scale
    def __iter__(self):
        yield from self.__dict__.items()

class Bone:
    def __init__(self, name):
        self.Name = name
        self.Children = []
    def addChildBone(self, bone):
        self.Children.append(bone)
    def __iter__(self):
        yield from self.__dict__.items()

class Frame:
    def __init__(self, number):
        self.Number = number
        self.Bones = []
    def addBone(self, bone):
        self.Bones.append(bone)
    def __iter__(self):
        yield from self.__dict__.items()

class Action:
    def __init__(self, name, acType):
        self.Type = acType
        self.Name = name
        self.FPS = None
        self.KeyFrames = []
    def addKeyFrame(self, frame):
        self.KeyFrames.append(frame)
    def __iter__(self):
        yield from self.__dict__.items()

class Skeleton:
    def __init__(self):
        self.Root = None
        self.Actions = []
        self.Pose = None
        self.BoneOrder = []
    def setRootBone(self, bone):
        self.Root = bone
    def __iter__(self):
        yield from self.__dict__.items()

class BoneIndex:
    def __init__(self, name, index):
        self.Name = name
        self.Index = index
    def __iter__(self):
        yield from self.__dict__.items()
    def __lt__(self, other):
        return self.Index < other.Index
    def __eq__(self, other):
        return self.Index == other.Index


class BoneIndicesAligner:
    def __init__(self, skeletonOb):
        self.map = dict()
        count = 0
        for pbone in skeletonOb.pose.bones:
            self.map[pbone.name] = count
            count += 1
    def getIndexOf(self, boneName):
        return self.map[boneName]



class HierarchyObject:
    def __init__(self, name):
        self.Name = name
        self.Children = []
    def addChild(self, obj):
        if isinstance(obj, HierarchyObject):
            self.Children.append(obj)
        else:
            raise Exception("This is not an hierarchy object")
    def __iter__(self):
        yield from self.__dict__.items()

class Hierarchy:
    def __init__(self):
        self.elements = dict()
        self.root = None
    def addChildTo(self, childName, parentName=None):
        #TODO: Check this exception, a child can only have one parent
        if childName in self.elements:
            raise Exception("Key already present in hierarchy")
        if self.root != None and parentName == None:
            raise Exception("The root has been already set")
        elif self.root == None and parentName == None:
            self.root = HierarchyObject(childName)
            self.elements[childName] = self.root
            return
        if not parentName in self.elements:
            raise Exception("The parent "+parentName+" is not present")
        else:
            parent = self.elements[parentName]
            child = HierarchyObject(childName)
            parent.addChild(child)
            self.elements[childName] = child
    def __iter__(self):
        yield from self.root.__dict__.items()



class SceneObjectsList:
    def __init__(self):
        self.SceneObjects = []
        self.Hierarchy = Hierarchy()
        #Remove from exporting
        self.byType = dict()
        self.textures = dict()
    def getByType(self, typ):
        if typ in self.byType:
            return self.byType[typ]
        return []
    def getLights(self):
        if SCENEOBJTYPE_LIGHT in self.byType:
            return self.byType[SCENEOBJTYPE_LIGHT]
        return []
    def getModels(self):
        if SCENEOBJTYPE_MODEL in self.byType:
            return self.byType[SCENEOBJTYPE_MODEL]
        return []
    def addTexture(self, texture):
        self.textures[texture.Name] = texture
    def getTextures(self):
        return self.textures
    def __addChildTo(self, child, parent=None):
        if parent != None:
            self.Hierarchy.addChildTo(child.Name, parent.Name)
        else:
            self.Hierarchy.addChildTo(child.Name)
    def addSceneObj(self, obj, parent=None):
        self.__addChildTo(obj,parent)
        self.SceneObjects.append(obj)
        if obj.Type in self.byType:
            self.byType[obj.Type].append(obj)
        else:
            self.byType[obj.Type] = list()
            self.byType[obj.Type].append(obj)
        if obj.Type == SCENEOBJTYPE_MODEL:
            for mat in obj.Materials:
                if mat.hasTexture():
                    self.textures[mat.Texture.Name] = mat.Texture.path
    def __iter__(self):
        d = self.__dict__.copy()
        d.pop('byType')
        d.pop('textures')
        yield from d.items()

class Light(SceneObj):
    def __init__(self):
        SceneObj.__init__(self, DEFAULT_NAME_LIGHT, SCENEOBJTYPE_LIGHT)
        self.LightType = None
        self.Color = None

class PointLight(Light):
    def __init__(self):
        Light.__init__(self)
        self.LinearAttenuation = None
        self.QuadraticAttenuation = None

class SpotLight(Light):
    def __init__(self):
        Light.__init__(self)
        self.LinearAttenuation = None
        self.QuadraticAttenuation = None
        self.SpotSize = None