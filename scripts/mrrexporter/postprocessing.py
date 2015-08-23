from scripts.mrrexporter.models import ShaderProgram
from scripts.mrrexporter.shaders import VertexShaderSourceGenerator, FragmentShaderSourceGenerator


class ShaderOrganizer:
    def __init__(self, models):
        self.modelsDict = {m.Name : m for m in models}
        self.shadersDict = {m.Name : m.ShaderProgram for m in models}
    def areEquals(self, d1, d2):
        if len(d1) != len(d2):
            return False
        for k in d1.keys():
            if not k in d2.keys():
                return False
        return True
    def isGreater(self, d1, d2):
        for k in d1:
            if d1[k] < d2[k]:
                return False
        return True
    def getGreater(self, d1, d2):
        d = dict()
        for k in d1:
            d[k] = max(d1[k], d2[k])
        return d
    def updateConfigurer(self, s, shaders):
        v = s.configurer.getCharacteristicVector()
        for r in shaders:
            w = r.configurer.getCharacteristicVector()
            if self.areEquals(v, w):
                v = self.getGreater(v, w)
        s.configurer.updateWithCharacteristicVector(v)
    def setMaxShader(self):
        for shader in self.shadersDict.values():
            self.updateConfigurer(shader, self.shadersDict.values())
        aux = list()
        for model in self.modelsDict.values():
            v = model.ShaderProgram.configurer.getCharacteristicVector()
            #Checks if it is already hashed
            inside = False
            l = None
            for e in aux:
                k = e[0]
                if self.areEquals(k, v):
                    inside = True
                    l = e[1]
                    break
            if inside:
                l.append(model)
            else:
                aux.append((v, [model]))
        baseName = "ShaderProgram_"
        i = 0
        for e in aux:
            l = e[1]
            configurer = l[0].ShaderProgram.configurer
            vs = VertexShaderSourceGenerator(configurer).genSource()
            fs = FragmentShaderSourceGenerator(configurer).genSource()
            name = baseName + str(i)
            i = i+1
            program = ShaderProgram(name, configurer, vs, fs)
            for m in l:
                m.ShaderProgram = program

    def getMaxShader(self, s, shaders):
        v = s.configurer.getCharacteristicVector()
        m = s
        for r in shaders:
            w = r.configurer.getCharacteristicVector()
            if self.areEquals(v, w):
                if self.isGreater(v, w):
                    m = r
        return m
