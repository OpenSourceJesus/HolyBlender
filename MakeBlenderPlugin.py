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
		command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToUnreal.py'), 'input=' + os.path.expanduser(context.scene.world.unity_project_import_path), 'output=' + os.path.expanduser(context.scene.world.unreal_project_path), 'exclude=/Library' ]

		subprocess.check_call(command)
	
class TEXT_EDITOR_OT_BevyExportButton (bpy.types.Operator):
	bl_idname = 'bevy.export'
	bl_label = 'Export To Bevy'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToBevy.py'), 'input=' + os.path.expanduser(context.scene.world.unity_project_import_path), 'output=' + os.path.expanduser(context.scene.world.bevy_project_path), 'exclude=/Library' ]

		subprocess.check_call(command)
	
class TEXT_EDITOR_OT_UnityExportButton (bpy.types.Operator):
	bl_idname = 'unity.export'
	bl_label = 'Export To Unity'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		exportPath = os.path.expanduser(context.scene.world.unity_project_export_path)
		for textBlock in bpy.data.texts:
			if text.name.endswith('.cs'):
				text = textBlock.as_string()
				open(exportPath + '/Assets/Standard Assets/Scripts/' + text.name, 'wb').write(text.encode('utf-8'))
		command = [os.path.expanduser('~/Unity/Hub/Editor/' + context.scene.world.unity_export_version + '/Editor/Unity'), '-createProject', exportPath ]

		subprocess.check_call(command)

classes = [
	TEXT_EDITOR_OT_UnrealExportButton,
	TEXT_EDITOR_OT_BevyExportButton,
	TEXT_EDITOR_OT_UnityExportButton
]

def DrawUnityImportField (self, context):
	self.layout.prop(context.world, 'unity_project_import_path')

def DrawUnityExportPathField (self, context):
	self.layout.prop(context.world, 'unity_project_export_path')

def DrawUnityExportVersionField (self, context):
	self.layout.prop(context.world, 'unity_export_version')

def DrawUnrealExportField (self, context):
	self.layout.prop(context.world, 'unreal_project_path')

def DrawBevyExportField (self, context):
	self.layout.prop(context.world, 'bevy_project_path')

def DrawUnrealExportButton (self, context):
	self.layout.operator('unreal.export', icon='CONSOLE')

def DrawBevyExportButton (self, context):
	self.layout.operator('bevy.export', icon='CONSOLE')

def DrawUnityExportButton (self, context):
	self.layout.operator('unity.export', icon='CONSOLE')

def register ():
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.World.unity_project_import_path = bpy.props.StringProperty(
		name = 'Unity project import path',
		description = 'My description',
		default = ''
	)
	bpy.types.World.unity_project_export_path = bpy.props.StringProperty(
		name = 'Unity project export path',
		description = 'My description',
		default = ''
	)
	bpy.types.World.unity_export_version = bpy.props.StringProperty(
		name = 'Unity export version',
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
	bpy.types.TEXT_HT_footer.append(DrawUnityExportButton)
	bpy.types.WORLD_PT_context_world.append(DrawUnityImportField)
	bpy.types.WORLD_PT_context_world.append(DrawUnityExportPathField)
	bpy.types.WORLD_PT_context_world.append(DrawUnityExportVersionField)
	bpy.types.WORLD_PT_context_world.append(DrawUnrealExportField)
	bpy.types.WORLD_PT_context_world.append(DrawBevyExportField)

def unregister ():
	bpy.types.TEXT_HT_footer.remove(DrawUnrealExportButton)
	bpy.types.TEXT_HT_footer.remove(DrawBevyExportButton)
	bpy.types.TEXT_HT_footer.remove(DrawUnityExportButton)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityImportField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityExportPathField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityExportVersionField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnrealExportField)
	bpy.types.WORLD_PT_context_world.remove(DrawBevyExportField)
	for cls in classes:
		bpy.utils.unregister_class(cls)

if __name__ == '__main__':
	register ()