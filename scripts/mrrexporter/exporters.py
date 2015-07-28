from commons import *
from models import *
from shaders import *

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
        self.outMesh.Name = cleanName(self.mesh.name)
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
            #if self.ob.rotation_mode == 'QUATERNION':
            #    quat = self.ob.rotation_quaternion.copy()
            #elif self.ob.rotation_mode != 'AXIS_ANGLES':
            #    quat = self.ob.rotation_euler.to_quaternion()
            #else:
            #    self.ob.rotation_mode = 'QUATERNION'
            #    quat = self.ob.rotation_quaternion.copy()
            quat = self.ob.matrix_world.decompose()[1]
        self.ob.rotation_mode = curMode
        return quat
    def export(self):
        t = self.outTrans
        l, r, s = self.ob.matrix_world.decompose()
        t.Location = [mround(e) for e in l]
        t.Rotation = [mround(e) for e in self.getRotation()]
        t.Scale =    [mround(e) for e in s]

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
        #TODO: Change the Exporter here!!!
        #TODO: Seriously, this reference must not be here!
        self.outModel.ShaderProgram = ShaderGenerator(self.outModel, SceneObjectsList()).genShaderProgram()
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
        keys.addUniformKey(NormalMatrixUniformKey())
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
        self.outAction.FPS = C.scene.render.fps
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
        keys.addUniformKey(ModelViewMatrixUniformKey())
        #keys.addUniformKey(NormalMatrixUniformKey())
    def setUniformKeys(self):
        keys = self.outScene.UniformKeys
        keys.addUniformKey(MVPUniformKey())
        self.setLightsUniformKeys()
    def export(self):
        self.setUniformKeys()

class SceneObjectsExporter:
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
        organizer = ShaderOrganizer(self.outList.getModels())
        organizer.setMaxShader()
        SceneExporter(scene).export()

class SceneObjectExporter2:
    def __init__(self, name, sceneObjs):
        self.name = name
        self.sceneObjs = sceneObjs
    def export(self):
        try:
            obj = self.sceneObjs[self.name]
        except:
            return None
        if (obj.type == 'MESH'):
            model = Model()
            ModelExporter(obj, model).export()
            #self.outList.addSceneObj(model, scene)
            return model
        elif (obj.type == 'CAMERA'):
            camera = Camera()
            CameraExporter(obj, camera).export()
            #self.outList.addSceneObj(camera, scene)
            return camera
        elif (obj.type == 'LAMP'):
            light = Light()
            LightExporter(obj, light).export()
            #self.outList.addSceneObj(light, scene)
            return light
            


