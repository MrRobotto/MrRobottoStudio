from commons import *
from models import Attribute, AttributeKey, UniformKey

class VertexAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_VERTEX, ANAME_VERTEX, INDEX_VERTEX, DATATYPEATTR_VERTEX)

class NormalAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_NORMAL, ANAME_NORMAL, INDEX_NORMAL, DATATYPEATTR_NORMAL)

class MaterialAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_MATERIAL, ANAME_MATERIAL, INDEX_MATERIAL, DATATYPEATTR_MATERIAL)

class TextureAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_TEXTURE, ANAME_TEXTURECO, INDEX_TEXTURE, DATATYPEATTR_TEXTURE)

class WeightAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_WEIGHT, ANAME_WEIGHT, INDEX_WEIGHT, DATATYPEATTR_WEIGHT)

class BIndAttribute(Attribute):
    def __init__(self):
        Attribute.__init__(self,ATTRNAME_BIND, ANAME_BIND, INDEX_BIND, DATATYPEATTR_BIND)



class VertexKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_VERTEX, SIZEKEY_VERTEX, DATATYPEKEY_VERTEX)

class NormalKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_NORMAL, SIZEKEY_NORMAL ,DATATYPEKEY_NORMAL)

class MaterialKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_MATERIAL, SIZEKEY_MATERIAL, DATATYPEKEY_MATERIAL)

class TextureKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_TEXTURE, SIZEKEY_TEXTURE, DATATYPEKEY_TEXTURE)

class WeightKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_WEIGHT, SIZEKEY_WEIGHT, DATATYPEKEY_WEIGHT)

class BIndKey(AttributeKey):
    def __init__(self):
        AttributeKey.__init__(self,ATTRNAME_BIND, SIZEKEY_BIND, DATATYPEKEY_BIND)






class MVPUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_MVP_MATRIX,  UNIFORM_MVP_MATRIX, RENDERING_LEVEL_SCENE, 1)
        self.uniformName = UNAME_MVP_MATRIX
        self.uniformDataType = DATATYPE_MAT4

class ModelMatrixUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_MODEL_MATRIX, UNIFORM_MODEL_MATRIX, RENDERING_LEVEL_OBJECT, 1)
        self.uniformName = UNAME_MODEL_MATRIX
        self.uniformDataType = DATATYPE_MAT4

class ViewMatrixUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_VIEW_MATRIX, UNIFORM_VIEW_MATRIX, RENDERING_LEVEL_OBJECT, 1)
        self.uniformName = UNAME_VIEW_MATRIX
        self.uniformDataType = DATATYPE_MAT4

class ModelViewMatrixUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_MODELVIEW_MATRIX, UNIFORM_MODELVIEW_MATRIX, RENDERING_LEVEL_SCENE, 1)
        self.uniformName = UNAME_MODELVIEW_MATRIX
        self.uniformDataType = DATATYPE_MAT4

class NormalMatrixUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_NORMAL_MATRIX, UNIFORM_NORMAL_MATRIX, RENDERING_LEVEL_SCENE, 1)
        self.uniformName = UNAME_NORMAL_MATRIX
        self.uniformDataType = DATATYPE_MAT4

class ProjectionMatrixUniformKey(UniformKey):
    def __init__(self):
        UniformKey.__init__(self, UNIFORMGENERATOR_PROJECTION_MATRIX , UNIFORM_PROJECTION_MATRIX, RENDERING_LEVEL_OBJECT, 1)
        self.uniformName = UNAME_PROJECTION_MATRIX
        self.uniformDataType = DATATYPE_MAT4

class MaterialAmbientColorKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_AMBIENT_COLOR, UNIFORM_MATERIAL_AMBIENT_COLOR, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = UNAME_MATERIAL_AMBIENT_COLOR
        self.uniformDataType = DATATYPE_VEC4

class MaterialAmbientIntensityKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_AMBIENT_INTENSITY, UNIFORM_MATERIAL_AMBIENT_INTENSITY, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = UNAME_MATERIAL_AMBIENT_INTENSITY
        self.uniformDataType = DATATYPE_FLOAT

class MaterialDiffuseColorKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_DIFFUSE_COLOR, UNIFORM_MATERIAL_DIFFUSE_COLOR, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = UNAME_MATERIAL_DIFFUSE_COLOR
        self.uniformDataType = DATATYPE_VEC4

class MaterialDiffuseIntensityKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_DIFFUSE_INTENSITY, UNIFORM_MATERIAL_DIFFUSE_INTENSITY, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = UNAME_MATERIAL_DIFFUSE_INTENSITY
        self.uniformDataType = DATATYPE_FLOAT

class MaterialSpecularColorKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_SPECULAR_COLOR, UNIFORM_MATERIAL_SPECULAR_COLOR, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = UNAME_MATERIAL_SPECULAR_COLOR
        self.uniformDataType = DATATYPE_VEC4

class MaterialSpecularIntensityKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_MATERIAL_SPECULAR_INTENSITY ,UNIFORM_MATERIAL_SPECULAR_INTENSITY, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = UNAME_MATERIAL_SPECULAR_INTENSITY
        self.uniformDataType = DATATYPE_FLOAT

class BoneMatrixKey(UniformKey):
    def __init__(self, count):
        UniformKey.__init__(self, UNIFORMGENERATOR_BONE_MATRIX, UNIFORM_BONE_MATRIX, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = UNAME_BONE_MATRIX
        self.uniformDataType = DATATYPE_MAT4

class TexturedMaterialKey(UniformKey):
    def __init__(self, count=1):
        UniformKey.__init__(self, UNIFORMGENERATOR_TEXTURED_MATERIAL, UNIFORM_TEXTURED_MATERIAL, count)
        self.uniformName = UNAME_TEXTURED_MATERIAL
        self.uniformDataType = DATATYPE_FLOAT

class TextureSamplerKey(UniformKey):
    def __init__(self, count=1, index=0):
        UniformKey.__init__(self, UNIFORMGENERATOR_TEXTURE, UNIFORM_TEXTURE, RENDERING_LEVEL_OBJECT, count)
        self.uniformName = UNAME_TEXTURE_SAMPLER
        self.uniformDataType = DATATYPE_SAMPLER2D

class LightPositionKey(UniformKey):
    def __init__(self,count=1,index=0):
        UniformKey.__init__(self, UNIFORMGENERATOR_LIGHT_POSITION, UNIFORM_LIGHT_POSITION, RENDERING_LEVEL_OBJECT, count, index)
        self.uniformName = UNAME_LIGHT_POSITION
        self.uniformDataType = DATATYPE_VEC4

class LightColorKey(UniformKey):
    def __init__(self,count=1,index=0):
        UniformKey.__init__(self, UNIFORMGENERATOR_LIGHT_COLOR, UNIFORM_LIGHT_COLOR, RENDERING_LEVEL_OBJECT, count, index)
        self.uniformName = UNAME_LIGHT_COLOR
        self.uniformDataType = DATATYPE_VEC4

class LightsPositionArrayKey(UniformKey):
    def __init__(self,count=1):
        UniformKey.__init__(self, UNIFORMGENERATOR_LIGHT_POSITION_ARRAY, UNIFORM_LIGHT_POSITION_ARRAY, RENDERING_LEVEL_SCENE, count)
        self.uniformName = UNAME_LIGHT_POSITION_ARRAY
        self.uniformDataType = DATATYPE_VEC4

class LightsColorArrayKey(UniformKey):
    def __init__(self,count=1):
        UniformKey.__init__(self, UNIFORMGENERATOR_LIGHT_COLOR_ARRAY, UNIFORM_LIGHT_COLOR_ARRAY, RENDERING_LEVEL_SCENE, count)
        self.uniformName = UNAME_LIGHT_COLOR_ARRAY
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