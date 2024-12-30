import bpy, subprocess, os, sys, hashlib, mathutils, math, base64, webbrowser

thisDir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(thisDir)
from lib_HolyBlender import *


bpy.types.World.godotExportPath = bpy.props.StringProperty(
	name = 'Godot project path',
	description = '',
	default = '~/TestGodotProject'
)

for i in range(MAX_SCRIPTS_PER_OBJECT):
	setattr(bpy.types.Object, 'godotScript' + str(i), bpy.props.PointerProperty(name='Attach Godot script', type=bpy.types.Text))


@bpy.utils.register_class
class WorldPanel(bpy.types.Panel):
	bl_idname = 'WORLD_PT_WorldGodot_Panel'
	bl_label = 'HolyGodot'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'
	def draw (self, context):
		self.layout.prop(context.world, 'godotExportPath')
		self.layout.operator('godot.export', icon='CONSOLE')


@bpy.utils.register_class
class GodotScriptsPanel (bpy.types.Panel):
	bl_idname = 'OBJECT_PT_Godot_Scripts_Panel'
	bl_label = 'HolyBlender Godot Scripts'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'

	def draw (self, context):
		self.layout.label(text='Attach Godot scripts')
		foundUnassignedScript = False
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			hasScript = getattr(context.active_object, 'godotScript' + str(i)) != None
			if hasScript or not foundUnassignedScript:
				self.layout.prop(context.active_object, 'godotScript' + str(i))
			if not foundUnassignedScript:
				foundUnassignedScript = not hasScript


@bpy.utils.register_class
class GodotExportButton(bpy.types.Operator):
	bl_idname = 'godot.export'
	bl_label = 'Export To Godot'
	SCENE_TEMPLATE = '[gd_scene load_steps=3 format=3 uid="uid://lop2cefb4wqg"]'
	RESOURCE_TEMPLATE = '[ext_resource type="ꗈ0" uid="uid://ꗈ1" path="res://ꗈ2" id="ꗈ3"]'
	SUB_RESOURCE_TEMPLATE = '[sub_resource type="ꗈ0" id="ꗈ1"]'
	MODEL_TEMPLATE = '[node name="ꗈ0" parent="ꗈ1" instance=ExtResource("ꗈ2")]'
	TRANSFORM_TEMPLATE = 'transform = Transform3D(ꗈ0, ꗈ1, ꗈ2, ꗈ3, ꗈ4, ꗈ5, ꗈ6, ꗈ7, ꗈ8, ꗈ9, ꗈ10, ꗈ11)'
	NODE_TEMPLATE = '[node name="ꗈ0" type="ꗈ1" parent="ꗈ2"]'
	godotExportPath = ''
	resources = ''
	nodes = ''
	idIndex = 0
	exportedObjs = []

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		self.godotExportPath = os.path.expanduser(context.scene.world.godotExportPath)
		if not os.path.isdir(self.godotExportPath):
			MakeFolderForFile (os.path.join(self.godotExportPath, ''))

		self.idIndex = 0			
		os.system('mkdir ' + self.godotExportPath + '\ncd ' + self.godotExportPath + '\ntouch project.godot')
		
		MakeFolderForFile (os.path.join(self.godotExportPath, 'Scenes', ''))
		MakeFolderForFile (os.path.join(self.godotExportPath, 'Scripts', ''))
		CopyFile (os.path.join(GODOT_SCRIPTS_PATH, 'AddMeshCollision.gd'), os.path.join(self.godotExportPath, 'Scripts', 'AddMeshCollision.gd'))
		CopyFile (os.path.join(GODOT_SCRIPTS_PATH, 'SendAndRecieveServerEvents.gd'), os.path.join(self.godotExportPath, 'Scripts', 'SendAndRecieveServerEvents.gd'))
		self.resources = ''
		self.nodes = ''
		self.exportedObjs = []
		for obj in bpy.data.objects:
			if obj not in self.exportedObjs:
				self.MakeObject (obj)
		id = self.GetId(7)
		resource = self.RESOURCE_TEMPLATE
		resource = resource.replace(REPLACE_INDICATOR + '0', 'Script')
		resource = resource.replace(REPLACE_INDICATOR + '1', self.GetId(13))
		resource = resource.replace(REPLACE_INDICATOR + '2', os.path.join('Scripts', 'SendAndRecieveServerEvents.gd'))
		resource = resource.replace(REPLACE_INDICATOR + '3', id)
		self.resources += resource
		node3d = self.NODE_TEMPLATE
		node3d = node3d.replace(REPLACE_INDICATOR + '0', 'Send And Recieve Click Events')
		node3d = node3d.replace(REPLACE_INDICATOR + '1', 'Node3D')
		node3d = node3d.replace(REPLACE_INDICATOR + '2', '.')
		node3d += '\nscript = ExtResource("' + id + '")'
		self.nodes += node3d
		sceneText = self.SCENE_TEMPLATE
		sceneText += '\n' + self.resources + '\n[node name="' + bpy.context.scene.name + '" type="Node3D"]\n' + self.nodes
		open(os.path.join(self.godotExportPath, 'Scenes', bpy.context.scene.name + '.tscn'), 'wb').write(sceneText.encode('utf-8'))
		
		os.system('flatpak run org.godotengine.Godot ' + os.path.join(self.godotExportPath, 'project.godot'))

	def MakeObject (self, obj):
		#global attachedGodotScriptsDict
		attachedGodotScriptsDict = GetScripts('godot')
		for obj2 in bpy.data.objects:
			if obj in obj2.children and obj2 not in self.exportedObjs:
				self.MakeObject (obj2)
		if obj.type == 'MESH':
			fileExportFolder = os.path.join(self.godotExportPath, 'Art', 'Models')
			fileExportPath = os.path.join(fileExportFolder, '')
			MakeFolderForFile (fileExportPath)
			fileExportPath = ExportObject(obj, fileExportFolder)
			id = self.GetId(7)
			resource = self.RESOURCE_TEMPLATE
			resource = resource.replace(REPLACE_INDICATOR + '0', 'PackedScene')
			resource = resource.replace(REPLACE_INDICATOR + '1', self.GetId(13))
			resource = resource.replace(REPLACE_INDICATOR + '2', fileExportPath.replace(os.path.join(self.godotExportPath, ''), ''))
			resource = resource.replace(REPLACE_INDICATOR + '3', id)
			self.resources += resource + '\n'
			parentPath = self.GetParentPath(obj)
			if obj.rigid_body != None:
				rigidBody = self.NODE_TEMPLATE
				for modifier in obj.modifiers:
					if modifier.type == 'COLLISION':
						rigidBody = self.NODE_TEMPLATE[: -1] + 'node_paths=PackedStringArray("meshInstance")]'
						scriptId = self.GetId(7)
						resource = self.RESOURCE_TEMPLATE
						resource = resource.replace(REPLACE_INDICATOR + '0', 'Script')
						resource = resource.replace(REPLACE_INDICATOR + '1', self.GetId(13))
						resource = resource.replace(REPLACE_INDICATOR + '2', os.path.join('Scripts', 'AddMeshCollision.gd'))
						resource = resource.replace(REPLACE_INDICATOR + '3', scriptId)
						self.resources += resource + '\n'
						rigidBody += '\nscript = ExtResource("' + scriptId + '")'
						meshInstancePath = obj.name + '/' + obj.name
						rigidBody += '\nmeshInstance = NodePath("' + meshInstancePath + '")'
						break
				rigidBodyName = obj.name + ' (RigidBody3D)'
				rigidBodyParentPath = parentPath.replace(rigidBodyName + '/', '')
				if rigidBodyParentPath == '':
					rigidBodyParentPath = '.'
				rigidBody = rigidBody.replace(REPLACE_INDICATOR + '0', rigidBodyName)
				rigidBody = rigidBody.replace(REPLACE_INDICATOR + '1', 'RigidBody3D')
				rigidBody = rigidBody.replace(REPLACE_INDICATOR + '2', rigidBodyParentPath)
				rigidBody += '\nmass = ' + str(obj.rigid_body.mass)
				rigidBody += '\nlinear_damp_mode = 1'
				rigidBody += '\nlinear_damp = ' + str(obj.rigid_body.linear_damping)
				rigidBody += '\nangular_damp_mode = 1'
				rigidBody += '\nangular_damp = ' + str(obj.rigid_body.angular_damping)
				rigidBody += '\nfreeze = ' + str(int(not obj.rigid_body.enabled))
				self.nodes += rigidBody + '\n'
			model = self.MODEL_TEMPLATE
			model = model.replace(REPLACE_INDICATOR + '0', obj.name)
			model = model.replace(REPLACE_INDICATOR + '1', parentPath)
			model = model.replace(REPLACE_INDICATOR + '2', id)
			model += '\n' + self.GetTransformText(obj)
			self.nodes += model + '\n'
			self.MakeClickableChild (obj)
		elif obj.type == 'LIGHT':
			light = self.NODE_TEMPLATE
			light = light.replace(REPLACE_INDICATOR + '0', obj.name)
			lightObj = None
			for _light in bpy.data.lights:
				if _light.name == obj.name:
					lightObj = _light
					break
			if lightObj.type == 'SUN':
				light = light.replace(REPLACE_INDICATOR + '1', 'DirectionalLight3D')
			elif lightObj.type == 'POINT':
				light = light.replace(REPLACE_INDICATOR + '1', 'OmniLight3D')
			elif lightObj.type == 'SPOT':
				light = light.replace(REPLACE_INDICATOR + '1', 'SpotLight3D')
			else:# elif lightObject.type == 'AREA':
				print('Area lights are not supported in Godot')
				return
			light = light.replace(REPLACE_INDICATOR + '2', self.GetParentPath(obj))
			if lightObj.type == 'POINT':
				light += '\nomni_range = ' + str(lightObj.cutoff_distance)
			elif lightObj.type == 'SPOT':
				light += '\nspot_range = ' + str(lightObj.cutoff_distance)
				light += '\nspot_angle = ' + str(lightObj.spot_size)
			light += '\nlight_energy = ' + str(lightObj.energy * WATTS_TO_CANDELAS)
			light += '\nlight_color = ' + 'Color(' + str(lightObj.color[0]) + ', ' + str(lightObj.color[1]) + ', ' + str(lightObj.color[2]) + ', 1)'
			light += '\n' + self.GetTransformText(obj)
			self.nodes += light + '\n'
		elif obj.type == 'CAMERA':
			camera = self.NODE_TEMPLATE
			camera = camera.replace(REPLACE_INDICATOR + '0', obj.name)
			camera = camera.replace(REPLACE_INDICATOR + '1', 'Camera3D')
			camera = camera.replace(REPLACE_INDICATOR + '2', self.GetParentPath(obj))
			cameraObj = None
			for _camera in bpy.data.cameras:
				if _camera.name == obj.name:
					cameraObj = _camera
					break
			if cameraObj.type == 'ORTHO':
				camera += '\nprojection = 1'
				camera += '\nsize = ' + str(cameraObj.ortho_scale)
			else:
				camera += '\nprojection = 0'
				camera += '\nfov = ' + str(math.degrees(cameraObj.angle))
			camera += '\nnear = ' + str(cameraObj.clip_start)
			camera += '\nfar = ' + str(cameraObj.clip_end)
			camera += '\n' + self.GetTransformText(obj)
			self.nodes += camera + '\n'
		attachedScripts = attachedGodotScriptsDict.get(obj, [])
		for attachedScript in attachedScripts:
			script = attachedScript
			if not attachedScript.endswith('.gd'):
				script += '.gd'
			for textBlock in bpy.data.texts:
				if textBlock.name == attachedScript:
					open(os.path.join(self.godotExportPath, 'Scripts', script), 'wb').write(textBlock.as_string().encode('utf-8'))
					break
			id = self.GetId(7)
			resource = self.RESOURCE_TEMPLATE
			resource = resource.replace(REPLACE_INDICATOR + '0', 'Script')
			resource = resource.replace(REPLACE_INDICATOR + '1', self.GetId(13))
			resource = resource.replace(REPLACE_INDICATOR + '2', os.path.join('Scripts', script))
			resource = resource.replace(REPLACE_INDICATOR + '3', id)
			self.resources += resource + '\n'
			self.nodes += '\nscript = ExtResource("' + id + '")'
		self.exportedObjs.append(obj)
	
	def GetTransformText (self, obj):
		transform = self.TRANSFORM_TEMPLATE
		location = obj.location
		if obj.type == 'MESH':
			location = mathutils.Vector((0, 0, 0))
		previousObjectRotationMode = obj.rotation_mode
		obj.rotation_mode = 'XYZ'
		size = mathutils.Vector((obj.scale.x, obj.scale.z, obj.scale.y))
		matrix = mathutils.Matrix.LocRotScale(mathutils.Vector((0, 0, 0)), obj.rotation_euler, size)
		right = mathutils.Vector((1, 0, 0)) @ matrix
		up = mathutils.Vector((0, 0, 1)) @ matrix
		forward = mathutils.Vector((0, 1, 0)) @ matrix
		obj.rotation_mode = previousObjectRotationMode
		transform = transform.replace(REPLACE_INDICATOR + '10', str(location.z))
		transform = transform.replace(REPLACE_INDICATOR + '11', str(-location.y))
		transform = transform.replace(REPLACE_INDICATOR + '0', str(right.x))
		transform = transform.replace(REPLACE_INDICATOR + '1', str(right.y))
		transform = transform.replace(REPLACE_INDICATOR + '2', str(right.z))
		transform = transform.replace(REPLACE_INDICATOR + '3', str(up.x))
		transform = transform.replace(REPLACE_INDICATOR + '4', str(up.y))
		transform = transform.replace(REPLACE_INDICATOR + '5', str(up.z))
		transform = transform.replace(REPLACE_INDICATOR + '6', str(forward.x))
		transform = transform.replace(REPLACE_INDICATOR + '7', str(forward.y))
		transform = transform.replace(REPLACE_INDICATOR + '8', str(forward.z))
		transform = transform.replace(REPLACE_INDICATOR + '9', str(location.x))
		return transform
	
	def GetParentPath (self, obj):
		output = ''
		parent = obj
		if obj.rigid_body != None:
			output = obj.name + ' (RigidBody3D)/'
		for obj2 in bpy.data.objects:
			if parent in obj2.children:
				parent = obj2
				if obj2.rigid_body != None:
					output += obj2.name + ' (RigidBody3D)/'
				output += obj2.name + '/'
		if output == '':
			output = '.'
		return output

	def GetId (self, length : int):
		output = '1'
		for i in range(1, length):
			output += '0'
		output = str(int(output) + self.idIndex)
		self.idIndex += 1
		return output

	def MakeClickableChild (self, obj):
		parentPath = self.GetParentPath(obj)
		rigidBody = self.NODE_TEMPLATE[: -1] + 'node_paths=PackedStringArray("meshInstance")]'
		rigidBody = rigidBody.replace(REPLACE_INDICATOR + '0', obj.name + ' (Clickable)')
		rigidBody = rigidBody.replace(REPLACE_INDICATOR + '1', 'RigidBody3D')
		rigidBody = rigidBody.replace(REPLACE_INDICATOR + '2', parentPath + obj.name)
		rigidBody += '\nfreeze = true'
		rigidBody += '\ncollision_layer = 2147483648'
		rigidBody += '\ncollision_mask = 0'
		id = self.GetId(7)
		rigidBody += '\nscript = ExtResource("' + id + '")'
		meshInstancePath = '../' + obj.name
		rigidBody += '\nmeshInstance = NodePath("' + meshInstancePath + '")'
		self.nodes += rigidBody + '\n'
		resource = self.RESOURCE_TEMPLATE
		resource = resource.replace(REPLACE_INDICATOR + '0', 'Script')
		resource = resource.replace(REPLACE_INDICATOR + '1', self.GetId(13))
		resource = resource.replace(REPLACE_INDICATOR + '2', os.path.join('Scripts', 'AddMeshCollision.gd'))
		resource = resource.replace(REPLACE_INDICATOR + '3', id)
		self.resources += resource + '\n'

