from commons import *
#from models import *
import models
from keys import *


#VoidShader = ShaderProgram("VoidShader", [],[],"","")

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
        self.src += "\tvec4 color = vcolor;\n"
    def genColorFromTexture(self):
        self.src += "\tvec4 color = texture2D(" + UNAME_TEXTURE_SAMPLER + ", " + "vtexco" +");\n"
    def genAssignColor(self):
        self.src += "\tgl_FragColor = color;\n"
    def genLightReflectionFunction(self):
        #this works for diffuse only
        s = ""
        #s += "precision highp float;\n"
        s += "vec3 mrAmbientLightColor = vec3(0.0, 0.0, 0.0);\n"

        s += "vec4 blinnPhongColor(vec4 diffColor) {\n"
        s += "\tvec3 linearColor;\n"
        s += "\tvec3 gammaCorrectedColor;\n"

        s += "\tvec3 normal = vnormal;\n"
        s += "\tnormal = normal/length(normal);\n"
        s += "\tvec3 viewDir = normalize(-vvert);\n"
        s += "\tviewDir = viewDir/length(viewDir);\n"
        s += "\tvec3 ambient = vambientColor * mrAmbientLightColor;\n"

        s += "\tvec3 lightPos;\n"
        s += "\tvec3 lightCol;\n"
        s += "\tvec3 lightDir;\n"
        s += "\tvec3 halfDir;\n"
        s += "\tfloat distance;\n"
        s += "\tfloat att;\n"
        s += "\tfloat lambertian;\n"
        s += "\tfloat specAngle;\n"

        s += "\tfloat specular = 0.0;\n"
        s += "\tfloat diffuse;\n"
        s += "\tfloat shininnes = 16.0;\n"
        s += "\tvec3 gammaVec = vec3(1.0/2.2);\n"

        s += "\tlinearColor = ambient;\n"
        for l in self.configurer.getLights():
            lk = l.UniformKeys.getByGenerator(UNIFORMGENERATOR_LIGHT_POSITION)[0]
            namePos = lk.getUniform().Name
            ck = l.UniformKeys.getByGenerator(UNIFORMGENERATOR_LIGHT_COLOR)[0]
            nameCol = ck.getUniform().Name
            s += "\tlightPos = " + namePos + ".xyz;\n"
            s += "\tlightCol = " + nameCol + ".xyz;\n"
            s += "\tlightDir = lightPos - vvert;\n"
            s += "\tlightDir = lightDir/length(lightDir);\n"
            s += "\tdistance = length(lightPos - vvert);\n"
            s += "\tatt = 1.0/(1.0+0.3*distance);\n"
            s += "\tlambertian = max(dot(lightDir, normal), 0.0);\n"
            s += "\tdiffuse = lambertian;\n"
            s += "\tif (lambertian > 0.0) {\n"
            s += "\t\thalfDir = normalize(lightDir + viewDir);\n"
            s += "\t\tspecAngle = max(dot(halfDir, normal), 0.0);\n"
            s += "\t\tspecular = pow(specAngle, 50.0);\n"
            s += "\t}\n"
            #Falta el light energy
            #s += "\tlinearColor += att*(lambertian * diffColor.xyz * lightCol + specular * vspecularColor * lightCol);\n"
            #this works for diffuse
            s += "\tlinearColor += att * (diffuse * diffColor.xyz * lightCol  +  0.5 * specular * vspecularColor * lightCol);\n"
            #s += "\tif (lambertian > 1.1) { linearColor = vec3(1.0,0.0,0.0);}\n"
            #s += "\t else { linearColor += (diffuse * diffColor.xyz * lightCol);}\n"
        s += "\tgammaCorrectedColor = pow(linearColor, gammaVec);\n"
        s += "\treturn vec4(gammaCorrectedColor, 1.0);\n"
        s += "}\n"
        s += "\n"
        self.src += s
    def genCallToBlinnPhong(self):
        self.src += "\tcolor = blinnPhongColor(color);\n"
    def genPrecission(self):
        self.src += "precision highp float;\n"
    def genSource(self):
        self.genPrecission()
        self.genHeaders(at=False)
        if self.configurer.hasLights():
            self.genLightReflectionFunction()
        self.genMainOpen()
        if self.configurer.hasTextures():
            self.genColorFromTexture()
        elif self.configurer.hasMaterials():
            self.genColorFromMaterial()
        if self.configurer.hasLights():
            self.genCallToBlinnPhong()
        self.genAssignColor()
        self.genMainClose()
        return self.src



class VertexShaderSourceGenerator(ShaderSourceGeneratorBase):
    def __init__(self, configurer):
        ShaderSourceGeneratorBase.__init__(self, configurer, configurer.vsuniforms)
    #TODO: Los outs deben ir a otra parte
    def genMaterialColorOut(self):
        n = self.configurer.getMaterialsCount()
        if n > 1:
            self.src += "\tint matIndexInt = int(" + ANAME_MATERIAL + ");\n"
            self.src += "\tvcolor = " + UNAME_MATERIAL_DIFFUSE_COLOR +"[matIndexInt];\n"
        else:
            self.src += "\tvcolor = " + UNAME_MATERIAL_DIFFUSE_COLOR + ";\n"
    def genTextureOut(self):
        self.src += "\tvtexco = " + ANAME_TEXTURECO + ";\n"
    def genSkinMatrixFunction(self):
        s = ""
        s += "mat4 getSkinMatrix() {\n"
        s += "\tvec4 indices = " + ANAME_BIND + ";\n"
        s += "\tvec4 w = " + ANAME_WEIGHT + ";\n"
        s += "\t if (int(indices.x) < 0) {\n"
        s += "\t\treturn mat4(1.0);\n"
        s += "\t}\n"
        if self.configurer.getBonesCount() == 1:
            s += "\tmat4 mat = " + UNAME_BONE_MATRIX + " * w.x;\n"
            s += "\treturn mat;\n"
            s += "}\n"
            s += "\n"
            self.src += s
            return
        s += "\tmat4 mat = " + UNAME_BONE_MATRIX + "[int(indices.x)] * w.x;\n"
        s += "\tfor (int i = 1; i < 4; i++) {\n"
        s += "\t\tindices = indices.yzwx;\n"
        s += "\t\tw = w.yzwx;\n"
        s += "\t\tif (int(indices.x) > 0 && w.x > 0.0) {\n"
        s += "\t\t\tmat = mat + " + UNAME_BONE_MATRIX + "[int(indices.x)] * w.x;\n"
        s += "\t\t}\n"
        s += "\t}\n"
        s += "\treturn mat;\n"
        s += "}\n"
        s += "\n"
        self.src += s
    def genMVPVertex(self):
        self.src += "\tgl_Position = " + UNAME_MVP_MATRIX + " * " + "vec4(" + ANAME_VERTEX +",1);\n"
    def genBoneApplyMVPVertex(self):
        self.src += "\tmat4 skinMatrix = getSkinMatrix();\n"
        self.src += "\tvec4 pos4 = skinMatrix * vec4(" + ANAME_VERTEX + ", 1);\n"
        self.src += "\tvec3 pos = vec3(pos4)/pos4.w;\n"
        self.src += "\tgl_Position = " + UNAME_MVP_MATRIX + " * vec4(pos, 1);\n"
    def genLightRefractionVertex(self):
        s = ""
        if self.configurer.hasBones():
            s += "\tvec4 surfPos = " + UNAME_MODEL_MATRIX + " * " + "vec4(pos, 1);\n"
            s += "\tvvert = vec3(surfPos)/surfPos.w;\n"
            s += "\tmat3 auxMat = mat3(" + UNAME_MODEL_MATRIX + " * " + "skinMatrix);\n"
            s += "\tmat3 normalMatrix = transpose(inverse(auxMat));\n"
            s += "\tvnormal = normalMatrix * " + ANAME_NORMAL + ";\n"
        else:
            s = ""
            s += "\tvec4 surfPos = " + UNAME_MODEL_MATRIX + " * " + "vec4(" + ANAME_VERTEX + ", 1);\n"
            s += "\tvvert = vec3(surfPos)/surfPos.w;\n"
            s += "\tmat3 normalMatrix = mat3(" + UNAME_NORMAL_MATRIX + ");\n"
            #s += "\tmat3 normalMatrix = transpose(inverse(mat3(" + UNAME_MODEL_MATRIX + ")));\n"
            s += "\tvnormal = normalMatrix * " + ANAME_NORMAL + ";\n"
        if self.configurer.hasMaterials():
            s += "\tvambientColor = " + UNAME_MATERIAL_AMBIENT_COLOR + ".xyz;\n"
            s += "\tvspecularColor = " + UNAME_MATERIAL_SPECULAR_COLOR + ".xyz;\n"
        self.src += s
    def genSource(self):
        self.genHeaders()
        if self.configurer.hasBones():
            self.genSkinMatrixFunction()
        self.genMainOpen()
        if self.configurer.hasTextures():
            self.genTextureOut()
        elif self.configurer.hasMaterials():
            self.genMaterialColorOut()
        if self.configurer.hasBones():
            self.genBoneApplyMVPVertex()
        else:
            self.genMVPVertex()
        if self.configurer.hasLights():
            self.genLightRefractionVertex()
        self.genMainClose()
        return self.src

#TODO: Change the Exporter.sceneObjectsList
class ShaderConfigurer:
    def __init__(self, obj, objectList=None):
        self.obj = obj
        self.objectList = objectList
        self.attributes = dict()
        self.uniforms = list()
        self.uniformsDict = dict()
        self.vsuniforms = dict()
        self.fsuniforms = dict()
        self.varyings = list()
        self.__getAttributesOfObject()
        self.__getUniformsOfObject()
        self.__getVaryingsOfObject()
    def getCharacteristicVector(self):
        d = dict()
        if self.hasLights():
            d["Lights"] = self.getLightsCount()
        if self.hasTextures():
            d["Textures"] = 1
        if self.hasMaterials():
            d["Materials"] = self.getMaterialsCount()
        if self.hasBones():
            d["Bones"] = self.getBonesCount()
        return d
    def updateWithCharacteristicVector(self, v):
        def updateUniform(keyName, value, uniforms):
            for u in uniforms:
                if keyName in u.Uniform.lower():
                    u.Count = value
        for key in v:
            if key == "Lights":
                updateUniform("light", v[key], self.uniforms)
            if key == "Materials":
                updateUniform("material", v[key], self.uniforms)
            if key == "Bones":
                updateUniform("bone", v[key], self.uniforms)
    def getUniforms(self):
        return self.uniforms
    def getVsUniforms(self):
        return self.vsuniforms.values()
    def getFsUniforms(self):
        return self.fsuniforms.values()
    def getAttributes(self):
        return self.attributes
    def getVaryings(self):
        return self.varyings
    def getMaterialsCount(self):
        if UNIFORM_MATERIAL_DIFFUSE_COLOR not in self.uniformsDict:
            return 0
        return self.uniformsDict[UNIFORM_MATERIAL_DIFFUSE_COLOR].Count
    def getBonesCount(self):
        if UNIFORM_BONE_MATRIX not in self.uniformsDict:
            return 0
        return self.uniformsDict[UNIFORM_BONE_MATRIX].Count
    def hasMaterials(self):
        return UNIFORM_MATERIAL_DIFFUSE_COLOR in self.uniformsDict
    def hasMultipleMaterialsAndTextures(self):
        return UNIFORM_TEXTURE in self.uniformsDict and self.uniformsDict[UNIFORM_MATERIAL_DIFFUSE_COLOR].Count > 1
    def hasTextures(self):
        return UNIFORM_TEXTURE in self.uniformsDict
    def hasBones(self):
        return UNIFORM_BONE_MATRIX in self.uniformsDict
    def hasLights(self):
        b = len(self.objectList.getLights()) > 0
        return b
    def getLightsCount(self):
        return len(self.objectList.getLights())
    def getLights(self):
        return self.objectList.getLights()
    def __getVaryingsOfObject(self):
        if isinstance(self.obj, models.Model):
            #if self.hasMultipleMaterialsAndTextures():
            #    self.varyings.append("varying vec2 vtexco;")
            #    self.varyings.append("varying vec4 vcolor;")
            #    return
            if self.hasTextures():
                self.varyings.append("varying vec2 vtexco;")
            if self.hasMaterials() and not self.hasTextures():
                self.varyings.append("varying vec4 vcolor;")
            if self.hasLights():
                self.varyings.append("varying vec3 vnormal;")
                self.varyings.append("varying vec3 vvert;")
                self.varyings.append("varying vec3 vambientColor;")
                self.varyings.append("varying vec3 vspecularColor;")
    def __getAttributesOfObject(self):
        if isinstance(self.obj, models.Model):
            for key in self.obj.Mesh.AttributeKeys:
                atr = getAttributeFromAttributeKey(key)
                self.attributes[atr.Attribute] = atr
    def __getUniformsOfObject(self):
        for key in self.obj.UniformKeys:
            unif = key.getUniform()
            self.uniformsDict[unif.Uniform] = unif
        if isinstance(self.obj, models.Model):
            self.__getModelUniforms()
    def __getModelUniforms(self):
        d = self.uniformsDict.copy()
        #d.pop(UNIFORM_MODEL_MATRIX, None)
        if (self.hasLights()):
            self.vsuniforms[UNIFORM_MODELVIEW_MATRIX] = ModelViewMatrixUniformKey().getUniform()
            fsmodelview = ModelViewMatrixUniformKey().getUniform()
            fsmodelview.Name = "fs"+fsmodelview.Name
            #fsmodelview.Uniform = "FS_" + UNIFORM_MODELVIEW_MATRIX
            self.fsuniforms[fsmodelview.Uniform] = fsmodelview
            if not self.hasBones():
                self.vsuniforms[UNIFORM_NORMAL_MATRIX] = NormalMatrixUniformKey().getUniform()
            #TODO: Solo funciona para una luz
            for l in self.objectList.getLights():
                for uk in l.UniformKeys:
                    self.fsuniforms[uk.Uniform] = uk.getUniform()
            #for i in range(self.getLightsCount()):
            #    lpk = LightPositionKey(index=i)
            #    lck = LightColorKey(index=i)
            #    self.fsuniforms[lpk.Uniform] = LightPositionKey().getUniform()
            #    self.fsuniforms[lck.Uniform] = LightColorKey().getUniform()
        self.vsuniforms[UNIFORM_MVP_MATRIX] = MVPUniformKey().getUniform()
        for unif in d:
            if unif == UNIFORM_TEXTURE:
                self.fsuniforms[UNIFORM_TEXTURE] = d[unif]
            else:
                self.vsuniforms[unif] = d[unif]
        self.uniformsDict = self.vsuniforms.copy()
        self.uniformsDict.update(self.fsuniforms)
        self.uniforms.extend(self.vsuniforms.values())
        self.uniforms.extend(self.fsuniforms.values())


class ShaderGenerator:
    counter = 0
    baseName = "ShaderProgram_"
    def __init__(self, obj, objectList=None):
        self.obj = obj
        self.configurer = ShaderConfigurer(self.obj, objectList)
        self.name = self.__genName()
    def __genName(self):
        name = ShaderGenerator.baseName + str(ShaderGenerator.counter)
        ShaderGenerator.counter += 1
        return name
    def genSource(self):
        vs, fs = None, None
        if isinstance(self.obj, models.Model):
            vs = VertexShaderSourceGenerator(self.configurer).genSource()
            fs = FragmentShaderSourceGenerator(self.configurer).genSource()
        print("VertexShader")
        print(vs)
        print("FragmentShader")
        print(fs)
        return vs, fs
    def genShaderProgram(self):
        vs, fs = self.genSource()
        return models.ShaderProgram(self.name, self.configurer, vs, fs)