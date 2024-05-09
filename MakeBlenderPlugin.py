import bpy, subprocess, os

bl_info = {
	'name': 'Blender Plugin',
	'blender': (2, 80, 0),
	'category': 'System',
}
	
class TEXT_EDITOR_OT_UnrealExportButton (bpy.types.Operator):
	bl_idname = 'unreal.export'
	bl_label = 'Export To Unreal'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		# open('/tmp/' + textBlockName,  'wb').write()
		command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToUnreal.py'), 'input=' + os.path.expanduser(context.scene.world.unity_project_path), 'output=' + os.path.expanduser(context.scene.world.unreal_project_path), 'exclude=/Library' ]

		subprocess.check_call(command)
	
class TEXT_EDITOR_OT_BevyExportButton (bpy.types.Operator):
	bl_idname = 'bevy.export'
	bl_label = 'Export To Bevy'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		# open('/tmp/' + textBlockName,  'wb').write()
		command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToBevy.py'), 'input=' + os.path.expanduser(context.scene.world.unity_project_path), 'output=' + os.path.expanduser(context.scene.world.bevy_project_path), 'exclude=/Library' ]

		subprocess.check_call(command)

classes = [
	TEXT_EDITOR_OT_UnrealExportButton,
	TEXT_EDITOR_OT_BevyExportButton
]

def DrawUnityImportField (self, context):
	self.layout.prop(context.world, 'unity_project_path')

def DrawUnrealExportField (self, context):
	self.layout.prop(context.world, 'unreal_project_path')

def DrawBevyExportField (self, context):
	self.layout.prop(context.world, 'bevy_project_path')

def DrawUnrealExportButton (self, context):
	self.layout.operator('unreal.export', icon='CONSOLE')

def DrawBevyExportButton (self, context):
	self.layout.operator('bevy.export', icon='CONSOLE')

def register ():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.World.unity_project_path = bpy.props.StringProperty(
		name = 'Unity project path',
		description = 'My description',
		default = ''
	)
	bpy.types.World.unreal_project_path = bpy.props.StringProperty(
		name = 'Unreal project path',
		description = 'My description',
		default = ''
	)
	bpy.types.World.bevy_project_path = bpy.props.StringProperty(
		name = 'Bevy project path',
		description = 'My description',
		default = ''
	)
	bpy.types.TEXT_HT_footer.append(DrawUnrealExportButton)
	bpy.types.TEXT_HT_footer.append(DrawBevyExportButton)
	bpy.types.WORLD_PT_context_world.append(DrawUnityImportField)
	bpy.types.WORLD_PT_context_world.append(DrawUnrealExportField)
	bpy.types.WORLD_PT_context_world.append(DrawBevyExportField)
	print(str(bpy.types.World.bevy_project_path))

def unregister ():
	bpy.types.TEXT_HT_footer.remove(DrawUnrealExportButton)
	bpy.types.TEXT_HT_footer.remove(DrawBevyExportButton)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityImportField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnrealExportField)
	bpy.types.WORLD_PT_context_world.remove(DrawBevyExportField)
	for cls in classes:
		bpy.utils.unregister_class(cls)

if __name__ == '__main__':
	register ()