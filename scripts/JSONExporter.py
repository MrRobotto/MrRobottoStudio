import os
import json
import threading
import struct
from math import pi

import bpy
import bpy.path
import bmesh
from mathutils import *
import bpy.types

D = bpy.data
C = bpy.context

EXT = ".json"
MAX_DIGITS = 6
PRECISSION = 0.0000001

NUM_BONES_PERVERTEX = 4

DATATYPE_FLOAT = "float"
DATATYPE_INT = "int"
DATATYPE_SHORT = "short"
DATATYPE_VEC2 = "vec2"
DATATYPE_VEC3 = "vec3"
DATATYPE_VEC4 = "vec4"
DATATYPE_MAT3 = "mat3"
DATATYPE_MAT4 = "mat4"
DATATYPE_SAMPLER2D = "sampler2D"

ATTRNAME_VERTEX = "Vertices"
ATTRNAME_NORMAL = "Normals"
ATTRNAME_MATERIAL = "MaterialIndex"
ATTRNAME_TEXTURE = "Texture"
ATTRNAME_WEIGHT = "Weight"
ATTRNAME_BIND = "BoneIndices"

NAME_VERTEX = "vertex"
NAME_NORMAL = "normal"
NAME_MATERIAL = "matIndex"
NAME_TEXTURECO = "texCo"
NAME_WEIGHT = "weights"
NAME_BIND = "bIndices"

INDEX_VERTEX = 0
INDEX_NORMAL = 1
INDEX_MATERIAL = 2
INDEX_TEXTURE = 3
INDEX_WEIGHT = 4
INDEX_BIND = 5

DATATYPEATTR_VERTEX = DATATYPE_VEC3
DATATYPEATTR_NORMAL = DATATYPE_VEC3
DATATYPEATTR_MATERIAL = DATATYPE_FLOAT
DATATYPEATTR_TEXTURE = DATATYPE_VEC2
DATATYPEATTR_WEIGHT = DATATYPE_VEC4
DATATYPEATTR_BIND = DATATYPE_VEC4

DATATYPEKEY_VERTEX = DATATYPE_FLOAT
DATATYPEKEY_NORMAL = DATATYPE_FLOAT
DATATYPEKEY_MATERIAL = DATATYPE_FLOAT
DATATYPEKEY_TEXTURE = DATATYPE_FLOAT
DATATYPEKEY_WEIGHT = DATATYPE_FLOAT
DATATYPEKEY_BIND = DATATYPE_FLOAT

SIZEKEY_VERTEX = 3
SIZEKEY_NORMAL = 3
SIZEKEY_MATERIAL = 1
SIZEKEY_TEXTURE = 2
SIZEKEY_WEIGHT = NUM_BONES_PERVERTEX
SIZEKEY_BIND = NUM_BONES_PERVERTEX

UNIFORMGENERATOR_MVP = "Generator_Matrix_Model_View_Projection"
UNIFORMGENERATOR_MODEL = "Generator_Matrix_Model"
UNIFORMGENERATOR_VIEW = "Generator_Matrix_View"
UNIFORMGENERATOR_PROJECTION = "Generator_Matrix_Projection"
UNIFORMGENERATOR_TMV = "Generator_Matrix_Transp_Model_View"
UNIFORMGENERATOR_ITMV = "Generator_Matrix_Inverse_Transp_Model_View"
UNIFORMGENERATOR_MATERIAL_AMBIENT_COLOR = "Generator_Ambient_Color"
UNIFORMGENERATOR_MATERIAL_AMBIENT_INTENSITY = "Generator_Ambient_Intensity"
UNIFORMGENERATOR_MATERIAL_DIFFUSE_COLOR = "Generator_Diffuse_Color"
UNIFORMGENERATOR_MATERIAL_DIFFUSE_INTENSITY = "Generator_Diffuse_Intensity"
UNIFORMGENERATOR_MATERIAL_SPECULAR_COLOR = "Generator_Specular_Color"
UNIFORMGENERATOR_MATERIAL_SPECULAR_INTENSITY = "Generator_Specular_Intensity"
UNIFORMGENERATOR_BONE_MATRIX = "Generator_Bone_Matrix"
UNIFORMGENERATOR_TEXTURED_MATERIAL = "Generator_Textured_Material"
UNIFORMGENERATOR_TEXTURE = "Generator_Texture_Sampler"
UNIFORMGENERATOR_LIGHT_POSITION = "Generator_Light_Position"
UNIFORMGENERATOR_LIGHT_COLOR = "Generator_Light_Color"
UNIFORMGENERATOR_LIGHT_POSITION_ARRAY = "Generator_Light_Position_Array"
UNIFORMGENERATOR_LIGHT_COLOR_ARRAY = "Generator_Light_Color_Array"

UNIFORM_MVP = "Matrix_Model_View_Projection"
UNIFORM_MODEL = "Matrix_Model"
UNIFORM_VIEW = "Matrix_View"
UNIFORM_PROJECTION = "Matrix_Projection"
UNIFORM_TMV = "Matrix_Transp_Model_View"
UNIFORM_ITMV = "Matrix_Inverse_Transp_Model_View"
UNIFORM_MATERIAL_AMBIENT_COLOR = "Ambient_Color"
UNIFORM_MATERIAL_AMBIENT_INTENSITY = "Ambient_Intensity"
UNIFORM_MATERIAL_DIFFUSE_COLOR = "Diffuse_Color"
UNIFORM_MATERIAL_DIFFUSE_INTENSITY = "Diffuse_Intensity"
UNIFORM_MATERIAL_SPECULAR_COLOR = "Specular_Color"
UNIFORM_MATERIAL_SPECULAR_INTENSITY = "Specular_Intensity"
UNIFORM_BONE_MATRIX = "Bone_Matrix"
UNIFORM_TEXTURED_MATERIAL = "Textured_Material"
UNIFORM_TEXTURE = "Texture_Sampler"
UNIFORM_LIGHT_POSITION = "Light_Position"
UNIFORM_LIGHT_COLOR = "Light_Color"
UNIFORM_LIGHT_POSITION_ARRAY = "Light_Position_Array"
UNIFORM_LIGHT_COLOR_ARRAY = "Light_Color_Array"

NAME_MVP = "mvpMatrix"
NAME_MODEL = "modelMatrix"
NAME_VIEW = "viewMatrix"
NAME_PROJECTION = "projMatrix"
NAME_MATERIAL_AMBIENT_COLOR = "ambientClr"
NAME_MATERIAL_AMBIENT_INTENSITY = "ambientInt"
NAME_MATERIAL_DIFFUSE_COLOR = "diffuse_color"
NAME_MATERIAL_DIFFUSE_INTENSITY = "diffuseInt"
NAME_MATERIAL_SPECULAR_COLOR = "specular_color"
NAME_MATERIAL_SPECULAR_INTENSITY = "specularInt"
NAME_BONE_MATRIX = "bones"
NAME_TEXTURE_SAMPLER = "mrtexture"
NAME_TEXTURED_MATERIAL = "mrtexturedMaterials"
NAME_LIGHT_POSITION = "mrLightPosition"
NAME_LIGHT_COLOR = "mrLightColor"
NAME_LIGHT_POSITION_ARRAY = "mrLightsPosition"
NAME_LIGHT_COLOR_ARRAY = "mrLightsColor"


MESHDICT_FACENAME = "Faces"
MESHDICT_EDGESNAME = "Edges"

DRAWTYPE_LINES = "Lines"
DRAWTYPE_TRIANGLES = "Triangles"

SCENEOBJTYPE_SCENE = "Scene"
SCENEOBJTYPE_MODEL  = "Model"
SCENEOBJTYPE_CAMERA = "Camera"
SCENEOBJTYPE_LIGHT = "Light"

LENS_PERSPECTIVE = "Perspective"
LENS_ORTHOGRAPHIC = "Orthographic"

DEFAULT_NAME_SCENE = "Scene"
DEFAULT_NAME_MODEL = "Model"
DEFAULT_NAME_CAMERA = "Camera"
DEFAULT_NAME_LIGHT = "Light"

RENDERING_LEVEL_OBJECT = 0
RENDERING_LEVEL_SCENE = 1
RENDERING_LEVEL_TOP_SCENE_LEVEL = 2
RENDERING_LEVEL_USER_LEVEL = 3

ACTIONTYPE_SKELETAL = "Skeletal"

TEXMAGFILTER_NEAREST = "Nearest"
TEXMAGFILTER_LINEAR = "Linear"
TEXMINFILTER_NEAREST = "Nearest"
TEXMINFILTER_LINEAR = "Linear"
TEXMINFILTER_NEAREST_NEAREST = "Nearest_Nearest"
TEXMINFILTER_NEAREST_LINEAR = "Nearest_Linear"
TEXMINFILTER_LINEAR_LINEAR = "Linear_Linear"
TEXMINFILTER_LINEAR_NEAREST = "Linear_Nearest"

LIGHTTYPE_SPOT = "Spot"
LIGHTTYPE_POINT = "Point"

DEFAULT_TEXTURE_INDEX = 1

ACTION_FPS = 24

SCENE_CLEARCOLOR = [0.5,0.5,0.5,1.0]

ORDER = {ATTRNAME_VERTEX: 0, ATTRNAME_NORMAL: 1, ATTRNAME_MATERIAL:2, ATTRNAME_TEXTURE: 3, ATTRNAME_WEIGHT: 4, ATTRNAME_BIND: 5}
DATATYPE_SIZES = {DATATYPE_FLOAT: 1, DATATYPE_INT: 1, DATATYPE_VEC2: 2, DATATYPE_VEC3: 3, DATATYPE_VEC4: 4, DATATYPE_MAT3: 9, DATATYPE_MAT4: 16}


def getDataSize(dataType):
    return DATATYPE_SIZES[dataType]

def cmpVec(v1,v2):
    """Compare if two vectors are equals"""
    if v1 == v2:
        return True
    return (v1-v2).length < PRECISSION

def mround(f):
    if hasattr(f, '__iter__') or hasattr(f, '__getitem__'):
        return [round(e, MAX_DIGITS) for e in f]
    else:
        return round(f, MAX_DIGITS)


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
    def __init__(self, AttributeName, Name, Index, DataSize, DataType):
        self.Attribute = AttributeName
        self.Name = Name
        self.Index = Index
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
        self.uniforms = []
    def addUniformKey(self, uniformKey):
        self.uniforms.append(uniformKey)
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
    def __init__(self,Name,attributes,uniforms,vssource,fssource):
        self.Name = Name
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
        yield from self.__dict__.items()





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
        self.Name = name
    def __iter__(self):
        yield from self.__dict__.items()




class Scene(SceneObj):
    def __init__(self, clearColor = SCENE_CLEARCOLOR):
        SceneObj.__init__(self, DEFAULT_NAME_SCENE, SCENEOBJTYPE_SCENE)
        self.ClearColor = clearColor




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


class VertexAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_VERTEX, NAME_VERTEX, INDEX_VERTEX, DATATYPEATTR_VERTEX)

class NormalAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_NORMAL, NAME_NORMAL, INDEX_NORMAL, DATATYPEATTR_NORMAL)

class MaterialAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_MATERIAL, NAME_MATERIAL, INDEX_MATERIAL, DATATYPEATTR_MATERIAL)

class TextureAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_TEXTURE, NAME_TEXTURECO, INDEX_TEXTURE, DATATYPEATTR_TEXTURE)

class WeightAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_WEIGHT, NAME_WEIGHT, INDEX_WEIGHT, DATATYPEATTR_WEIGHT)

class BIndAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_BIND, NAME_BIND, INDEX_BIND, DATATYPEATTR_BIND)



class VertexKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_VERTEX, NAME_VERTEX, INDEX_VERTEX, SIZEKEY_VERTEX, DATATYPEKEY_VERTEX)

class NormalKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_NORMAL, NAME_NORMAL, INDEX_NORMAL, SIZEKEY_NORMAL ,DATATYPEKEY_NORMAL)

class MaterialKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_MATERIAL, NAME_MATERIAL, INDEX_MATERIAL, SIZEKEY_MATERIAL, DATATYPEKEY_MATERIAL)

class TextureKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_TEXTURE, NAME_TEXTURECO, INDEX_TEXTURE, SIZEKEY_TEXTURE, DATATYPEKEY_TEXTURE)

class WeightKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_WEIGHT, NAME_WEIGHT, INDEX_WEIGHT, SIZEKEY_WEIGHT, DATATYPEKEY_WEIGHT)

class BIndKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_BIND, NAME_BIND, INDEX_BIND, SIZEKEY_BIND, DATATYPEKEY_BIND)



class MVPUniform(Uniform):
    def __init__(self):
        Uniform.__init__(self, UNIFORM_MVP, NAME_MVP, 1, DATATYPE_MAT4)

class ModelMatrixUniform(Uniform):
    def __init__(self):
        Uniform.__init__(self, UNIFORM_MODEL, NAME_MODEL, 1, DATATYPE_MAT4)

class ViewMatrixUniform(Uniform):
    def __init__(self):
        Uniform.__init__(self, UNIFORM_VIEW, NAME_VIEW, 1, DATATYPE_MAT4)

class ProjectionMatrixUniform(Uniform):
    def __init__(self):
        Uniform.__init__(self, UNIFORM_PROJECTION, NAME_PROJECTION, 1, DATATYPE_MAT4)

class MaterialAmbientColor(Uniform):
    def __init__(self, count):
        Uniform.__init__(self, UNIFORM_MATERIAL_AMBIENT_COLOR, NAME_MATERIAL_AMBIENT_COLOR, count, DATATYPE_VEC4)

class MaterialAmbientIntensity(Uniform):
    def __init__(self, count):
        Uniform.__init__(self, UNIFORM_MATERIAL_AMBIENT_INTENSITY, NAME_MATERIAL_AMBIENT_INTENSITY, count, DATATYPE_FLOAT)

class MaterialDiffuseColor(Uniform):
    def __init__(self, count):
        Uniform.__init__(self, UNIFORM_MATERIAL_DIFFUSE_COLOR, NAME_MATERIAL_DIFFUSE_COLOR, count, DATATYPE_VEC4)

class MaterialDiffuseIntensity(Uniform):
    def __init__(self, count):
        Uniform.__init__(self, UNIFORM_MATERIAL_DIFFUSE_INTENSITY, NAME_MATERIAL_DIFFUSE_INTENSITY, count, DATATYPE_FLOAT)

class MaterialSpecularColor(Uniform):
    def __init__(self, count):
        Uniform.__init__(self, UNIFORM_MATERIAL_SPECULAR_COLOR, NAME_MATERIAL_SPECULAR_COLOR, count, DATATYPE_VEC4)

class MaterialSpecularIntensity(Uniform):
    def __init__(self, count):
        Uniform.__init__(self, UNIFORM_MATERIAL_SPECULAR_INTENSITY, NAME_MATERIAL_SPECULAR_INTENSITY, count, DATATYPE_FLOAT)

class BoneMatrix(Uniform):
    def __init__(self, count):
        Uniform.__init__(self, UNIFORM_BONE_MATRIX, NAME_BONE_MATRIX, count, DATATYPE_MAT4)

class TexturedMaterial(Uniform):
    def __init__(self, count=1):
        Uniform.__init__(self, UNIFORM_TEXTURED_MATERIAL, NAME_TEXTURED_MATERIAL, count, DATATYPE_FLOAT)

class TextureSampler(Uniform):
    def __init__(self,count=1):
        Uniform.__init__(self, UNIFORM_TEXTURE, NAME_TEXTURE_SAMPLER, count, DATATYPE_SAMPLER2D)

class LightPosition(Uniform):
    def __init__(self):
        Uniform.__init__(self, UNIFORM_LIGHT_POSITION, NAME_LIGHT_POSITION, 1, DATATYPE_VEC4)

class LightColor(Uniform):
    def __init__(self):
        Uniform.__init__(self, UNIFORM_LIGHT_COLOR, NAME_LIGHT_COLOR, 1, DATATYPE_VEC4)

class LightsPositionArray(Uniform):
    def __init__(self,count=1):
        Uniform.__init__(self, UNIFORM_LIGHT_POSITION_ARRAY, NAME_LIGHT_POSITION_ARRAY, count, DATATYPE_VEC4)

class LightsColorArray(Uniform):
    def __init__(self,count=1):
        Uniform.__init__(self, UNIFORM_LIGHT_COLOR_ARRAY, NAME_LIGHT_COLOR_ARRAY, count, DATATYPE_VEC4)



class MVPUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_MVP,  UNIFORM_MVP, RENDERING_LEVEL_SCENE, 1)
        self.uniformName = NAME_MVP
        self.uniformDataType = DATATYPE_MAT4

class ModelMatrixUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_MODEL, UNIFORM_MODEL, RENDERING_LEVEL_OBJECT, 1)
        self.uniformName = NAME_MODEL
        self.uniformDataType = DATATYPE_MAT4

class ViewMatrixUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_VIEW, UNIFORM_VIEW, RENDERING_LEVEL_OBJECT, 1)
        self.uniformName = NAME_VIEW
        self.uniformDataType = DATATYPE_MAT4

class ProjectionMatrixUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_PROJECTION , UNIFORM_PROJECTION, RENDERING_LEVEL_OBJECT, 1)
        self.uniformName = NAME_PROJECTION
        self.uniformDataType = DATATYPE_MAT4

class MaterialAmbientColorKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_AMBIENT_COLOR, UNIFORM_MATERIAL_AMBIENT_COLOR, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_MATERIAL_AMBIENT_COLOR
        self.uniformDataType = DATATYPE_VEC4

class MaterialAmbientIntensityKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_AMBIENT_INTENSITY, UNIFORM_MATERIAL_AMBIENT_INTENSITY, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_MATERIAL_AMBIENT_INTENSITY
        self.uniformDataType = DATATYPE_FLOAT

class MaterialDiffuseColorKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_DIFFUSE_COLOR, UNIFORM_MATERIAL_DIFFUSE_COLOR, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_MATERIAL_DIFFUSE_COLOR
        self.uniformDataType = DATATYPE_VEC4

class MaterialDiffuseIntensityKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_DIFFUSE_INTENSITY, UNIFORM_MATERIAL_DIFFUSE_INTENSITY, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_MATERIAL_DIFFUSE_INTENSITY
        self.uniformDataType = DATATYPE_FLOAT

class MaterialSpecularColorKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_SPECULAR_COLOR, UNIFORM_MATERIAL_SPECULAR_COLOR, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_MATERIAL_SPECULAR_COLOR
        self.uniformDataType = DATATYPE_VEC4

class MaterialSpecularIntensityKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_SPECULAR_INTENSITY ,UNIFORM_MATERIAL_SPECULAR_INTENSITY, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_MATERIAL_SPECULAR_INTENSITY
        self.uniformDataType = DATATYPE_FLOAT

class BoneMatrixKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_BONE_MATRIX, UNIFORM_BONE_MATRIX, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_BONE_MATRIX
        self.uniformDataType = DATATYPE_MAT4

class TexturedMaterialKey(UniformKey):
    def __init__(self, count=1):
        UniformKey.__init__(self, UNIFORMGENERATOR_TEXTURED_MATERIAL, UNIFORM_TEXTURED_MATERIAL, count)
        self.uniformName = NAME_TEXTURED_MATERIAL
        self.uniformDataType = DATATYPE_FLOAT

class TextureSamplerKey(UniformKey):
    def __init__(self, count=1, index=0):
        UniformKey.__init__(self, UNIFORMGENERATOR_TEXTURE, UNIFORM_TEXTURE, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_TEXTURE_SAMPLER
        self.uniformDataType = DATATYPE_SAMPLER2D

class LightPositionKey(UniformKey):
    def __init__(self,count=1):
        UniformKey.__init__(self, UNIFORMGENERATOR_LIGHT_POSITION, UNIFORM_LIGHT_POSITION, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_LIGHT_POSITION
        self.uniformDataType = DATATYPE_VEC4

class LightColorKey(UniformKey):
    def __init__(self,count=1):
        UniformKey.__init__(self, UNIFORMGENERATOR_LIGHT_COLOR, UNIFORM_LIGHT_COLOR, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = NAME_LIGHT_COLOR
        self.uniformDataType = DATATYPE_VEC4

class LightsPositionArrayKey(UniformKey):
    def __init__(self,count=1):
        UniformKey.__init__(self, UNIFORMGENERATOR_LIGHT_POSITION_ARRAY, UNIFORM_LIGHT_POSITION_ARRAY, RENDERING_LEVEL_SCENE, count)
        self.uniformName = NAME_LIGHT_POSITION_ARRAY
        self.uniformDataType = DATATYPE_VEC4

class LightsColorArrayKey(UniformKey):
    def __init__(self,count=1):
        UniformKey.__init__(self, UNIFORMGENERATOR_LIGHT_COLOR_ARRAY, UNIFORM_LIGHT_COLOR_ARRAY, RENDERING_LEVEL_SCENE, count)
        self.uniformName = NAME_LIGHT_COLOR_ARRAY
        self.uniformDataType = DATATYPE_VEC4


def getAttributeFromAttributeKey(attrib):
    if isinstance(attrib, VertexKey):
        return VertexAttribute()
    elif isinstance(attrib, NormalKey):
        return NormalAttribute()
    elif isinstance(attrib, MaterialKey):
        return MaterialAttribute()
    elif isinstance(attrib, TextureKey):
        return TextureAttribute()
    elif isinstance(attrib, WeightKey):
        return WeightAttribute()
    elif isinstance(attrib, BIndKey):
        return BIndAttribute()

def getUniformFromUniformKey(uniformKey):
     '''if isinstance(uniform,MVPUniformKey):
        return MVPUniform()
     if isinstance(uniform,ModelMatrixUniformKey):
        return ModelMatrixUniform()
     if isinstance(uniform,ViewMatrixUniformKey):
        return ViewMatrixUniform()
     if isinstance(uniform,ProjectionMatrixUniformKey):
        return ProjectionMatrixUniform()
     if isinstance(uniform,MaterialAmbientColorKey):
        return MaterialAmbientColor(uniform.Count)
     if isinstance(uniform,MaterialAmbientIntensityKey):
        return MaterialAmbientIntensity(uniform.Count)
     if isinstance(uniform,MaterialDiffuseColorKey):
        return MaterialDiffuseColor(uniform.Count)
     if isinstance(uniform,MaterialDiffuseIntensityKey):
        return MaterialDiffuseIntensity(uniform.Count)
     if isinstance(uniform,MaterialSpecularColorKey):
        return MaterialSpecularColor(uniform.Count)
     if isinstance(uniform,MaterialSpecularIntensityKey):
        return MaterialSpecularIntensity(uniform.Count)
     if isinstance(uniform,BoneMatrixKey):
        return BoneMatrix(uniform.Count)
     if isinstance(uniform,TextureSamplerKey):
         return TextureSampler(uniform.Count)
     if isinstance(uniform,TexturedMaterialKey):
         return TexturedMaterial(uniform.Count)
     if isinstance(uniform,LightColorKey):
         return LightColor()
     if isinstance(uniform,LightPositionKey):
         return LightPosition()
     if isinstance(uniform,LightsPositionArrayKey):
         return LightsPositionArray(uniform.Count)
     if isinstance(uniform,LightsColorArrayKey):
         return LightsColorArray(uniform.Count)'''
     return uniformKey.getUniform()



VoidShader = ShaderProgram("VoidShader", [],[],"","")

class ShaderSourceGeneratorBase:
    def __init__(self, configurer, uniforms):
        self.configurer = configurer
        self.src = ""
        self.uniforms = uniforms
    def genHeaders(self, un=True, at=True, va=True):
        s = ""
        if un:
            for unif in self.uniforms.values():
                s += str(unif) + "\n"
            s += "\n"
        if at:
            for atr in self.configurer.attributes.values():
                s += str(atr) + "\n"
            s += "\n"
        if va:
            for var in self.configurer.varyings:
                s += var + "\n"
            s += "\n"
        self.src += s
    def genMainOpen(self):
        self.src += "void main() {\n"
    def genMainClose(self):
        self.src += "}\n"


class FragmentShaderSourceGenerator(ShaderSourceGeneratorBase):
    def __init__(self, configurer):
        ShaderSourceGeneratorBase.__init__(self, configurer, configurer.fsuniforms)
    def genColorFromMaterial(self):
        self.src += "\tgl_FragColor = vcolor;\n"
    def genColorFromTexture(self):
        self.src += "\tvec4 color = texture2D(" + NAME_TEXTURE_SAMPLER + ", " + "vtexco" +");\n"
        self.src += "\tgl_FragColor = color;\n"
    def genSource(self):
        self.genHeaders(at=False)
        self.genMainOpen()
        if self.configurer.hasTextures():
            self.genColorFromTexture()
        elif self.configurer.hasMaterials():
            self.genColorFromMaterial()
        self.genMainClose()
        return self.src



class VertexShaderSourceGenerator(ShaderSourceGeneratorBase):
    def __init__(self, configurer):
        ShaderSourceGeneratorBase.__init__(self, configurer, configurer.vsuniforms)
    #TODO: Los outs deben ir a otra parte
    def genMaterialColorOut(self):
        n = self.configurer.getMaterialsCount()
        if n > 1:
            self.src += "\tint matIndexInt = int(" + NAME_MATERIAL + ");\n"
            self.src += "\tvcolor = " + NAME_MATERIAL_DIFFUSE_COLOR +"[matIndexInt];\n"
        else:
            self.src += "\tvcolor = " + NAME_MATERIAL_DIFFUSE_COLOR + ";\n"
    def genTextureOut(self):
        self.src += "\tvtexco = " + NAME_TEXTURECO + ";\n"
    def genApplyBonesFunction(self):
        s = ""
        s += "vec3 applyBones() {\n"
        s += "\tvec4 indices = " + NAME_BIND + ";\n"
        s += "\tvec4 w = " + NAME_WEIGHT + ";\n"
        s += "\t if (int(indices.x) < 0) {\n"
        s += "\t\treturn " + NAME_VERTEX + ";\n"
        s += "\t}\n"
        if self.configurer.getBonesCount() == 1:
            s += "\tmat4 mat = " + NAME_BONE_MATRIX + " * w.x;\n"
            s += "\tvec4 v = mat * vec4(" + NAME_VERTEX + ",1);\n"
            s += "\treturn vec3(v.x/v.w, v.y/v.w, v.z/v.w);\n"
            s += "}\n"
            s += "\n"
            self.src += s
            return
        s = ""
        s += "vec3 applyBones() {\n"
        s += "\tvec4 indices = " + NAME_BIND + ";\n"
        s += "\tvec4 w = " + NAME_WEIGHT + ";\n"
        s += "\t if (int(indices.x) < 0) {\n"
        s += "\t\treturn " + NAME_VERTEX + ";\n"
        s += "\t}\n"
        s += "\tmat4 mat = " + NAME_BONE_MATRIX + "[int(indices.x)] * w.x;\n"
        s += "\tfor (int i = 1; i < 4; i++) {\n"
        s += "\t\tindices = indices.yzwx;\n"
        s += "\t\tw = w.yzwx;\n"
        s += "\t\tif (int(indices.x) > 0 && w.x > 0.0) {\n"
        s += "\t\t\tmat = mat + " + NAME_BONE_MATRIX + "[int(indices.x)] * w.x;\n"
        s += "\t\t}\n"
        s += "\t}\n"
        s += "\tvec4 v = mat * vec4(" + NAME_VERTEX + ",1);\n"
        s += "\treturn vec3(v.x/v.w, v.y/v.w, v.z/v.w);\n"
        s += "}\n"
        s += "\n"
        self.src += s
    def genMVPVertex(self):
        self.src += "\tgl_Position = " + NAME_MVP + " * " + "vec4(" + NAME_VERTEX +",1);\n"
    def genBoneApplyMVPVertex(self):
        self.src += "\tvec3 pos = applyBones();\n"
        self.src += "\tgl_Position = " + NAME_MVP + " * "+ "vec4(pos, 1);\n"

    def genSource(self):
        self.genHeaders()
        if self.configurer.hasBones():
            self.genApplyBonesFunction()
        self.genMainOpen()
        if self.configurer.hasTextures():
            self.genTextureOut()
        elif self.configurer.hasMaterials():
            self.genMaterialColorOut()
        if self.configurer.hasBones():
            self.genBoneApplyMVPVertex()
        else:
            self.genMVPVertex()
        self.genMainClose()
        return self.src


class ShaderGenerator:
    counter = 0
    baseName = "ShaderProgram_"
    def __init__(self, obj):
        self.obj = obj
        self.configurer = ShaderConfigurer(self.obj)
        self.name = self.__genName()
    def __genName(self):
        name = ShaderGenerator.baseName + str(ShaderGenerator.counter)
        ShaderGenerator.counter += 1
        return name
    def genSource(self):
        vs, fs = None, None
        if isinstance(self.obj, Model):
            vs = VertexShaderSourceGenerator(self.configurer).genSource()
            fs = FragmentShaderSourceGenerator(self.configurer).genSource()
        print("VertexShader")
        print(vs)
        print("FragmentShader")
        print(fs)
        return vs, fs
    def genShaderProgram(self):
        vs, fs = self.genSource()
        return ShaderProgram(self.name, self.configurer.attributes.values(), self.configurer.uniforms.values(), vs, fs)

class ShaderConfigurer:
    def __init__(self, obj, objectList=None):
        self.obj = obj
        self.objectList = objectList
        self.attributes = dict()
        self.uniforms = dict()
        self.vsuniforms = dict()
        self.fsuniforms = dict()
        self.varyings = list()
        self.__getAttributesOfObject()
        self.__getUniformsOfObject()
        self.__getVaryingsOfObject()
    def getUniforms(self):
        return self.uniforms
    def getVsUniforms(self):
        return self.vsuniforms
    def getFsUniforms(self):
        return self.fsuniforms
    def getAttributes(self):
        return self.attributes
    def getVaryings(self):
        return self.varyings
    def getMaterialsCount(self):
        if UNIFORM_MATERIAL_DIFFUSE_COLOR not in self.uniforms:
            return 0
        return self.uniforms[UNIFORM_MATERIAL_DIFFUSE_COLOR].Count
    def getBonesCount(self):
        if UNIFORM_BONE_MATRIX not in self.uniforms:
            return 0
        return self.uniforms[UNIFORM_BONE_MATRIX].Count
    def hasMaterials(self):
        return UNIFORM_MATERIAL_DIFFUSE_COLOR in self.uniforms
    def hasMultipleMaterialsAndTextures(self):
        return UNIFORM_TEXTURE in self.uniforms and self.uniforms[UNIFORM_MATERIAL_DIFFUSE_COLOR].Count > 1
    def hasTextures(self):
        return UNIFORM_TEXTURE in self.uniforms
    def hasBones(self):
        return UNIFORM_BONE_MATRIX in self.uniforms
    def __getVaryingsOfObject(self):
        if isinstance(self.obj, Model):
            #if self.hasMultipleMaterialsAndTextures():
            #    self.varyings.append("varying vec2 vtexco;")
            #    self.varyings.append("varying vec4 vcolor;")
            #    return
            if self.hasTextures():
                self.varyings.append("varying vec2 vtexco;")
                return
            if self.hasMaterials():
                self.varyings.append("varying vec4 vcolor;")
    def __getAttributesOfObject(self):
        if isinstance(self.obj, Model):
            for key in self.obj.Mesh.AttributeKeys:
                atr = getAttributeFromAttributeKey(key)
                self.attributes[atr.Attribute] = atr
    def __getUniformsOfObject(self):
        for key in self.obj.UniformKeys:
            unif = getUniformFromUniformKey(key)
            self.uniforms[unif.Uniform] = unif
        if isinstance(self.obj, Model):
            self.__getModelUniforms()
    def __getModelUniforms(self):
        d = self.uniforms.copy()
        d.pop(UNIFORM_MODEL, None)
        self.vsuniforms[UNIFORM_MVP] = MVPUniform()
        for unif in d:
            if unif == UNIFORM_TEXTURE:
                self.fsuniforms[UNIFORM_TEXTURE] = d[unif]
            else:
                self.vsuniforms[unif] = d[unif]
        self.uniforms = self.vsuniforms.copy()
        self.uniforms.update(self.fsuniforms)




#TODO: All exporters should have a method export with an out object?

class MeshExporter:
    def __init__(self, meshOb, outMesh, boneAligner=None):
        self.outMesh = outMesh
        self.meshOb = meshOb
        self.mesh = self.meshOb.data
        self.boneAligner = boneAligner
    def createBMesh(self):
        """Creation of a bmesh from meshOb and mesh"""
        self.bm = bmesh.new()
        self.bm.from_mesh(self.mesh)
        bmesh.ops.triangulate(self.bm, faces=self.bm.faces)
    def setKeys(self):
        """Adding of all available keys"""
        self.addVertexKey()
        self.addNormalKey()
        self.addMaterialKey()
        self.addUVKey()
        self.addArmatureKey()
    def setName(self):
        self.outMesh.Name = self.mesh.name
    def addVertexKey(self):
        """Add vertex coordinates key, it always exists"""
        self.outMesh.addKey(VertexKey())
    def addNormalKey(self):
        """Add vertex normal coordinates, it always exists"""
        self.outMesh.addKey(NormalKey())
    def addMaterialKey(self):
        """Add material key if we have materials"""
        if (len(self.meshOb.material_slots) > 0):
            self.outMesh.addKey(MaterialKey())
    def addUVKey(self):
        """Add UV coordinates if we have textures"""
        self.texLayer = self.bm.loops.layers.uv.active
        if self.texLayer != None:
            self.outMesh.addKey(TextureKey())
    def addArmatureKey(self):
        """Add weight and bone index keys if we have armature"""
        self.armOb = None
        self.arm = None
        self.armVGroups = None
        self.deformLayer = None
        for mod in self.meshOb.modifiers:
            if mod.type == 'ARMATURE':
                #We save the armature object and armature
                self.armOb = mod.object
                if self.armOb == None:
                    return
                self.arm = self.armOb.data
                #Also we save all bones vertex groups and the deformation layer
                self.armVGroups = [self.meshOb.vertex_groups[pbone.bone.name] for pbone in self.armOb.pose.bones if pbone.bone.name in self.meshOb.vertex_groups]
                self.deformLayer = self.bm.verts.layers.deform.active
                self.outMesh.addKey(WeightKey())
                self.outMesh.addKey(BIndKey())
                #TODO: Multiples armatures?
                return
    def getWeightAndIndex(self, loop, layer, groups):
        #if layer == None:
        #    return None, None
        if not self.outMesh.hasKey(ATTRNAME_BIND) or not self.outMesh.hasKey(ATTRNAME_WEIGHT):
            return None, None
        dvert = loop.vert[layer]
        count = 0
        #Default [0,0,0,0], no weight
        w = Vector([0]*NUM_BONES_PERVERTEX)
        #Default [-1,-1,-1,-1] no valid index
        i = Vector([-1]*NUM_BONES_PERVERTEX)
        for group in groups:
            if group.index in dvert:
                weight = dvert[group.index]
                if (abs(weight) > PRECISSION and count < NUM_BONES_PERVERTEX):
                    w[count] = weight
                    #i[count] = group.index
                    i[count] = self.boneAligner.getIndexOf(group.name)
                    count += 1
        w = w.normalized()
        return w,i
    def getUV(self, loop, layer):
        if self.outMesh.hasKey(ATTRNAME_TEXTURE):
            if layer == None:
                return None
            uv = loop[layer].uv
            c = Vector([uv[0],1-uv[1]])
            return c
    #TODO: Change all methods to this format
    def getMaterialIndex(self, face):
        if self.outMesh.hasKey(ATTRNAME_MATERIAL):
            return face.material_index
        else:
            return None
    def fixMaterialIndexAttribute(self):
        indices = self.outMesh.getMaterialIndices()
        if len(indices) == 1:
            key = self.outMesh.AttributeKeys.getKey(ATTRNAME_MATERIAL)
            pointer = key.Pointer
            stride = key.Stride
            v = self.outMesh.VertexData
            self.outMesh.VertexData = [v[i] for i in range(len(v)) if (i-pointer)%stride!=0]
            self.outMesh.AttributeKeys.removeKey(ATTRNAME_MATERIAL)
        elif len(indices) > 1:
            match = True
            remap = dict()
            for i in range(len(indices)):
                if not i == indices[i]:
                    match = False
                    remap[indices[i]] = i
                else:
                    remap[i] = i
            #Padding of materials, this means, there are materials not in use
            if not match:
                key = self.outMesh.AttributeKeys.getKey(ATTRNAME_MATERIAL)
                pointer = key.Pointer
                stride = key.Stride
                size = key.Size
                v = self.outMesh.VertexData
                for i in range(pointer,len(v), stride):
                    for j in range(size):
                        v[i+j] = remap[v[i+j]]
    def fixBoneIndicesAttributes(self):
        boneIndices = self.outMesh.getBoneIndices()
        match = True
        remap = dict()
        for i in range(len(boneIndices)):
            bi = int(boneIndices[i])
            if not i == bi:
                match = False
                remap[bi] = i
            else:
                remap[i] = i
        if not match:
            key = self.outMesh.AttributeKeys.getKey(ATTRNAME_BIND)
            pointer = key.Pointer
            stride = key.Stride
            size = key.Size
            v = self.outMesh.VertexData
            for i in range(pointer, len(v), stride):
                for j in range(size):
                    if v[i+j]>=0:
                        v[i+j] = remap[int(v[i+j])]
    def fixFaceIndices(self, geom):
        if not len(self.bm.verts) > len(geom.indices):
            return
        vertices = geom.vertices
        l = list(vertices)
        l.sort()
        for i in range(len(vertices)):
            if i != l[i].index:
                l[i].index = i
    def export(self):
        self.createBMesh()
        self.setName()
        self.setKeys()
        geom = GeometryList()
        materialSet = set()
        boneIndices = set()
        for face in self.bm.faces:
            f = Face()
            for loop in face.loops:
                index = loop.vert.index
                co = loop.vert.co
                normal = loop.vert.normal
                matIndex = self.getMaterialIndex(face)
                uv = self.getUV(loop, self.texLayer)
                w,bind = self.getWeightAndIndex(loop, self.deformLayer, self.armVGroups)
                v = Vertex(index,co,normal,matIndex, uv,w,bind)
                f.addVert(v)
                if bind is not None:
                    for ind in bind: boneIndices.add(int(ind))
                if matIndex is not None:
                    materialSet.add(matIndex)
            geom.addFace(f.v1,f.v2,f.v3)
        self.fixFaceIndices(geom)
        self.outMesh.IndexData = geom.getFaceIndices()
        self.outMesh.VertexData = geom.getVertices()
        self.outMesh.Count = geom.getNumFaces()
        self.bm.free()
        l = list(materialSet)
        l.sort()
        self.outMesh._materialIndices = l
        if -1 in boneIndices:
            boneIndices.remove(-1)
        l = list(boneIndices)
        l.sort()
        self.outMesh._boneIndices = l
        self.fixMaterialIndexAttribute()
        self.fixBoneIndicesAttributes()


class TransformExporter:
    def __init__(self, ob, outTrans):
        self.outTrans = outTrans
        self.ob = ob
    def getRotation(self):
        #The camera has Y as up axis in blender
        curMode = self.ob.rotation_mode
        if self.ob.type == 'CAMERA':
            self.ob.rotation_mode = 'QUATERNION'
            quat = self.ob.rotation_quaternion.copy()
            basisChange = Matrix([[1,0,0,0],[0,0,-1,0],[0,1,0,0],[0,0,0,1]])
            m = quat.to_matrix().to_4x4() * basisChange.inverted()
            quat = m.to_euler().to_quaternion()
        else:
            #We need the rotation in Quaternion mode, so we force it
            if self.ob.rotation_mode == 'QUATERNION':
                quat = self.ob.rotation_quaternion.copy()
            elif self.ob.rotation_mode != 'AXIS_ANGLES':
                quat = self.ob.rotation_euler.to_quaternion()
            else:
                self.ob.rotation_mode = 'QUATERNION'
                quat = self.ob.rotation_quaternion.copy()
        self.ob.rotation_mode = curMode
        return quat
    def export(self):
        t = self.outTrans
        t.Location = [mround(e) for e in self.ob.location]
        t.Rotation = [mround(e) for e in self.getRotation()]
        t.Scale =    [mround(e) for e in self.ob.scale]

class MaterialsExporter:
    def __init__(self, ob, model, outMaterials):
        self.ob = ob
        self.model = model
        self.outMaterials = outMaterials
        self.textureIndex = DEFAULT_TEXTURE_INDEX
    def getDiffuse(self, mat):
        color = mat.diffuse_color
        alpha = 1.0
        intensity = mround(mat.diffuse_intensity)
        color4 = [mround(e) for e in color] + [mround(alpha)]
        return MaterialLight(intensity, color4)
    def getSpecular(self, mat):
        color = mat.specular_color
        alpha = mat.specular_alpha
        intensity = mround(mat.specular_intensity)
        color4 = [mround(e) for e in color] + [mround(alpha)]
        return MaterialLight(intensity, color4)
    def getAmbient(self, mat):
        color = D.worlds[0].ambient_color
        alpha = 1.0
        intensity = mround(mat.ambient)
        color4 = [mround(e) for e in color] + [mround(alpha)]
        return MaterialLight(intensity, color4)
    def getTexture(self, mat):
        images = bpy.data.images
        try:
            activeTextureName = mat.active_texture.image.name
            for image in images:
                if image.name == activeTextureName:
                    path = image.filepath_from_user()
                    if os.path.exists(path):
                        t=Texture(activeTextureName,index=self.textureIndex,path=path)
                        self.textureIndex+=1
                        return t
        except:
            return None
    def export(self):
        #exportar nombre, diffuse, specular, emmisive?, ambient (tb ambient en la scene)
        #si tiene una textura o no asociada
        indices = self.model.Mesh.getMaterialIndices()
        for index in indices:
            material_slot = self.ob.material_slots[index]
            mat = material_slot.material
            name = mat.name
            diffuse = self.getDiffuse(mat)
            specular = self.getSpecular(mat)
            ambient = self.getAmbient(mat)
            texture = self.getTexture(mat)
            material = Material(name, diffuse, specular, ambient, texture)
            self.outMaterials.addMaterial(material)

class ModelExporter:
    def __init__(self, meshOb, outModel):
        self.meshOb = meshOb
        self.outModel = outModel
        self.boneAligner = None
    def setName(self):
        self.outModel.setName(self.meshOb.name)
    def setShader(self):
        #self.outModel.ShaderProgram = BasicShader
        self.outModel.ShaderProgram = ShaderGenerator(self.outModel).genShaderProgram()
    def getSkeleton(self):
        for mod in self.meshOb.modifiers:
            if mod.type == 'ARMATURE':
                return mod.object
    def getMaterials(self):
        if (len(self.meshOb.material_slots) > 0):
            return self.meshOb.material_slots
        else:
            return None
    def setUniformKeys(self):
        keys = self.outModel.UniformKeys
        keys.addUniformKey(ModelMatrixUniformKey())
        mesh = self.outModel.Mesh
        #TODO: Obtener los materiales del meshob y listos
        materials = self.outModel.Materials
        if materials is not None:
            numMat = len(materials)
            keys.addUniformKey(MaterialAmbientColorKey(numMat))
            keys.addUniformKey(MaterialAmbientIntensityKey(numMat))
            keys.addUniformKey(MaterialDiffuseColorKey(numMat))
            keys.addUniformKey(MaterialDiffuseIntensityKey(numMat))
            keys.addUniformKey(MaterialSpecularColorKey(numMat))
            keys.addUniformKey(MaterialSpecularIntensityKey(numMat))
            numTextures = 0
            for mat in materials:
                if mat.hasTexture():
                    numTextures += 1
            if numTextures > 0:
                keys.addUniformKey(TextureSamplerKey(numTextures))
                #keys.addUniformKey(TexturedMaterialKey(numMat))
        skeleton = self.getSkeleton()
        if skeleton is not None:
            bones = mesh.getBoneIndices()
            keys.addUniformKey(BoneMatrixKey(len(bones)))
    def export(self):
        global meshOb
        meshOb = self.meshOb
        self.setName()
        skeletonOb = self.getSkeleton()
        if skeletonOb is not None:
            self.outModel.Skeleton = Skeleton()
            self.boneAligner = BoneIndicesAligner(skeletonOb)
            MeshExporter(self.meshOb, self.outModel.Mesh,self.boneAligner).export()
            poseBones = [skeletonOb.pose.bones[i] for i in self.outModel.Mesh.getBoneIndices()]
            SkeletonExporter(skeletonOb, self.meshOb, self.outModel.Skeleton, poseBones, self.boneAligner).export()
        else:
            MeshExporter(self.meshOb, self.outModel.Mesh).export()
        TransformExporter(self.meshOb, self.outModel.Transform).export()
        MaterialsExporter(self.meshOb, self.outModel, self.outModel.Materials).export()
        self.setUniformKeys()
        self.setShader()

class CameraExporter:
    def __init__(self, cameraOb, outCamera):
        self.cameraOb = cameraOb
        self.camera = cameraOb.data
        self.outCamera = outCamera
    def setName(self):
        self.outCamera.setName(self.cameraOb.name)
    def setLens(self):
        if self.camera.type == "PERSP":
            self.outCamera.Lens = PerspectiveLens()
            self.exportPerspectiveLens(self.camera, self.outCamera.Lens)
        elif self.camera.type == "ORTHO":
            self.outCamera.Lens = OrthographicLens()
            self.exportOrthographicLens(self.camera, self.outCamera.Lens)
    def exportPerspectiveLens(self,camera,lens):
        #TODO: Delete, this won't be used anymore
        lens.AspectRatio = mround(camera.angle_x)
        lens.ClipStart = mround(camera.clip_start)
        lens.ClipEnd = mround(camera.clip_end)
        curUnits, camera.lens_unit = camera.lens_unit, "FOV"
        lens.FOV = mround(camera.lens)
        camera.lens_unit = curUnits
    def exportOrthographicLens(self,camera,lens):
        lens.OrthographicScale = camera.ortho_scale
    def setUniformKeys(self):
        keys = self.outCamera.UniformKeys
        keys.addUniformKey(ViewMatrixUniformKey())
        keys.addUniformKey(ProjectionMatrixUniformKey())
    def export(self):
        self.setName()
        self.setLens()
        TransformExporter(self.cameraOb, self.outCamera.Transform).export()
        self.setUniformKeys()




class SkeletonPoseExporter:
    def __init__(self, skeletonOb, meshOb, poseBones, outSkeleton):
        self.skeletonOb = skeletonOb
        self.meshOb = meshOb
        self.poseBones = poseBones
        self.outSkeleton = outSkeleton
    def export(self):
        wm2 = self.skeletonOb.matrix_world
        wm = self.meshOb.matrix_world
        for pbone in self.poseBones:
            b = None
            #m = pbone.matrix_channel
            #m = wm.inverted() * wm2* pbone.matrix*pbone.bone.matrix_local.inverted()* wm2.inverted() * wm
            m = wm.inverted() * wm2* pbone.matrix*pbone.bone.matrix_local.inverted()* wm2.inverted() * wm
            q = m.to_quaternion()
            q.normalize()
            s = mround(m.to_scale())
            l = mround(m.to_translation())
            q = mround(q)

            b = PoseBone(pbone.name,s, q, l)
            self.outSkeleton.append(b)

class SingleSkeletalActionExporter:
    def __init__(self, actionOb, skeletonOb, meshOb, poseBones, outAction):
        self.actionOb = actionOb
        self.outAction = outAction
        self.skeletonOb = skeletonOb
        self.meshOb = meshOb
        self.poseBones = poseBones
        self.originalKeyFrame = bpy.context.scene.frame_current
        self.originalAction = self.skeletonOb.animation_data.action
    def setAction(self):
        '''binds the action to be exported'''
        self.skeletonOb.animation_data.action = self.actionOb
    def restoreOriginalAction(self):
        '''Restores the action in use defined by the user'''
        self.skeletonOb.animation_data.action = self.originalAction
    def setKeyFrame(self,kf):
        '''Sets a certain frame'''
        bpy.context.scene.frame_set(kf)
    def restoreOriginalKeyframe(self):
        '''Restores the original frame defined by the user'''
        self.setKeyFrame(self.originalKeyFrame)
    def __addErrorCorrectingFrames(self, keyframes):
        kfs = {k for k in keyframes}
        for i in range(1, len(keyframes)):
            k1, k2 = keyframes[i-1], keyframes[i]
            if abs(k1-k2) > 5:
                newframes=self.__addErrorCorrectingFrames([k1,int((k1+k2)/2), k2])
                for e in newframes:
                    kfs.add(e)
        r = list(kfs)
        r.sort()
        return r
    def getKeyFramesIndices(self):
        '''Gets all key-frames for the current action'''
        keyframes = []
        for k in self.actionOb.fcurves[0].keyframe_points:
            keyframes.append(int(k.co[0]))
        return self.__addErrorCorrectingFrames(keyframes)
    def getKeyFrames(self):
        '''From every keyframe obtains the key frame index, and how are located and rotated the bones of the
        current skeleton'''
        for kfi in self.getKeyFramesIndices():
            self.setKeyFrame(kfi)
            frame = Frame(kfi)
            bones = []
            SkeletonPoseExporter(self.skeletonOb, self.meshOb, self.poseBones, bones).export()
            for bone in bones:
                frame.addBone(bone)
            self.outAction.addKeyFrame(frame)
    def setFps(self):
        self.outAction.FPS = ACTION_FPS
    def export(self):
        self.setAction()
        self.setFps()
        self.getKeyFrames()
        self.restoreOriginalKeyframe()
        self.restoreOriginalAction()


class SkeletalActionsExporter:
    def __init__(self, skeletonOb, meshOb, poseBones, outActions):
        self.skeletonOb = skeletonOb
        self.meshOb = meshOb
        self.poseBones = poseBones
        self.outActions = outActions
    def actionBoneNames(self, action):
        '''Gets all bones used in a certain action'''
        names = set()
        path_resolve = self.skeletonOb.path_resolve
        for fcu in action.fcurves:
            try:
                prop = path_resolve(fcu.data_path, False)
            except:
                prop = None
            if prop is not None:
                data = prop.data
                if isinstance(data, bpy.types.PoseBone):
                    names.add(data.name)
        return names
    def getSkeletonActions(self):
        '''Obtains all actions for this skeleton, if only one bone between skeleton
        and action channels match, we have an action'''
        actions = D.actions
        bones =  set([b.name for b in self.poseBones])
        myActions = []
        for ac in actions:
            actionBoneNames = self.actionBoneNames(ac)
            if len(bones.intersection(actionBoneNames))>0:
                myActions.append(ac)
        return myActions
    def exportThreadTarget(self, ac, skeletonOb, action):
        SingleSkeletalActionExporter(ac, self.skeletonOb, self.meshOb, self.poseBones, action).export()
        l = threading.Lock()
        l.acquire()
        self.outActions.append(action)
        l.release()
    def export(self):
        self.actions = self.getSkeletonActions()
        for ac in self.actions:
            action = Action(ac.name, ACTIONTYPE_SKELETAL)
            t = threading.Thread(target=self.exportThreadTarget, args=(ac, self.skeletonOb, action))
            t.start()
            t.join()
            #SingleSkeletalActionExporter(ac, self.skeletonOb, action).export()
            #self.outActions.append(action)

class SkeletonExporter:
    def __init__(self, skeletonOb, meshOb, outSkeleton, poseBones, boneAligner):
        self.skeletonOb = skeletonOb
        self.meshOb = meshOb
        self.poseBones = poseBones
        self.outSkeleton = outSkeleton
        self.actions = None
        self.boneAligner = boneAligner
    def setName(self):
        self.outSkeleton.setName(self.skeletonOb.name)
    def __getBonesRecursive(self, parentBone, children):
        '''Recursive function to gets all bones'''
        for child in children:
            b = Bone(child.name)
            parentBone.addChildBone(b)
            self.__getBonesRecursive(b, child.children)
    def getBoneHierarchy(self):
        '''Gets the bone hierarchy'''
        arm = self.skeletonOb.data
        bones = arm.bones
        root = Bone(bones[0].name)
        self.__getBonesRecursive(root, bones[0].children)
        self.outSkeleton.setRootBone(root)
    def getSkeletonPose(self):
        bones = []
        SkeletonPoseExporter(self.skeletonOb, self.meshOb, self.poseBones, bones).export()
        self.outSkeleton.Pose = bones
    def getBoneOrder(self):
        for pbone in self.poseBones:
            self.outSkeleton.BoneOrder.append(pbone.name)
    def export(self):
        self.getBoneHierarchy()
        self.getBoneOrder()
        self.getSkeletonPose()
        SkeletalActionsExporter(self.skeletonOb, self.meshOb, self.poseBones, self.outSkeleton.Actions).export()


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

class LightExporter:
    def __init__(self, lightOb, outLight):
        self.lightOb = lightOb
        self.light = lightOb.data
        self.outLight = outLight
    def getName(self):
        self.outLight.Name = self.lightOb.name
    def getLightType(self):
        typ = self.light.type
        if typ == 'SPOT':
            self.outLight.LightType = LIGHTTYPE_SPOT
        elif typ == 'POINT':
            self.outLight.LightType = LIGHTTYPE_POINT
    def getColor(self):
        self.outLight.Color = self.light.color
    def getAttenuations(self):
        self.outLight.LinearAttenuation = self.light.linear_attenuation
        self.outLight.QuadraticAttenuation = self.light.quadratic_attenuation
    def getSpotSize(self):
        self.outLight.SpotSize = self.light.spot_size
    def exportPointLight(self):
        self.getAttenuations()
    def exportSpotLight(self):
        self.getAttenuations()
        self.getSpotSize()
    def setUniformKeys(self):
        keys = self.outLight.UniformKeys
        keys.addUniformKey(LightPositionKey())
        keys.addUniformKey(LightColorKey())
    def export(self):
        self.getLightType()
        self.getName()
        self.getColor()
        if self.outLight.LightType == LIGHTTYPE_POINT:
            self.exportPointLight()
        elif self.outLight.LightType == LIGHTTYPE_SPOT:
            self.exportPointLight()
        TransformExporter(self.lightOb, self.outLight.Transform).export()
        self.setUniformKeys()



class SceneExporter:
    def __init__(self, outScene):
        self.outScene = outScene
    def setLightsUniformKeys(self):
        keys = self.outScene.UniformKeys
        lights = Exporter.sceneObjectsList.getByType(SCENEOBJTYPE_LIGHT)
        if len(lights) == 0:
            return
        keys.addUniformKey(LightsPositionArrayKey(len(lights)))
        keys.addUniformKey(LightsColorArrayKey(len(lights)))
    def setUniformKeys(self):
        keys = self.outScene.UniformKeys
        keys.addUniformKey(MVPUniformKey())
        self.setLightsUniformKeys()
    def export(self):
        self.setUniformKeys()

class SceneObjectsListExporter:
    def __init__(self, sceneObjs, outList):
        self.sceneObjs = sceneObjs
        self.outList = outList
    def export(self):
        scene = Scene()
        self.outList.addSceneObj(scene)
        meshes = []
        for obj in self.sceneObjs:
            if (obj.type == 'MESH'):
                meshes.append(obj)
            elif (obj.type == 'CAMERA'):
                camera = Camera()
                CameraExporter(obj, camera).export()
                self.outList.addSceneObj(camera, scene)
            elif (obj.type == 'LAMP'):
                light = Light()
                LightExporter(obj, light).export()
                self.outList.addSceneObj(light, scene)
        for obj in meshes:
            model = Model()
            ModelExporter(obj, model).export()
            self.outList.addSceneObj(model, scene)
        SceneExporter(scene).export()


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

Exporter().export()