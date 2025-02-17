import bpy, subprocess, os, sys#, webbrowser
thisDir = os.path.split(os.path.abspath(__file__))[0]
thisDir = thisDir.replace('/dist/BlenderPlugin/_internal', '')
if thisDir not in sys.path:
	sys.path.append(thisDir)
from lib_HolyBlender import *
if not os.path.isdir( os.path.join(thisDir, 'Blender_bevy_components_workflow') ):
	cmd = 'git clone https://github.com/OpenSourceJesus/Blender_bevy_components_workflow --depth=1'
	print(cmd)

	subprocess.check_call(cmd.split(), cwd = thisDir)

sys.path.append(os.path.join(thisDir, 'Blender_bevy_components_workflow/tools'))
import bevy_components
print(bevy_components)
import gltf_auto_export
print(gltf_auto_export)
bpy.ops.preferences.addon_enable(module='bevy_components')
bpy.ops.preferences.addon_enable(module='gltf_auto_export')

bpy.types.World.bevy_project_path = bpy.props.StringProperty(
	name = 'Bevy project path',
	description = '',
	default = os.path.join(INIT_EXPORT_PATH, 'TestBevyProject')
)
for i in range(MAX_SCRIPTS_PER_OBJECT):
	setattr(bpy.types.Object, 'bevyScript' + str(i), bpy.props.PointerProperty(name='Attach bevy script', type=bpy.types.Text))
registryText = open(TEMPLATE_REGISTRY_PATH, 'rb').read().decode('utf-8')
registryText = registryText.replace('ꗈ', '')
open(REGISTRY_PATH, 'wb').write(registryText.encode('utf-8'))
registry = bpy.context.window_manager.components_registry
registry.schemaPath = REGISTRY_PATH
bpy.ops.object.reload_registry()
EXAMPLES_DICT = {
	'Hello World (bevy)' : 'println!("Hello World!");',
	'Rotate (bevy)'      : 'trs.rotate_y(5.0 * time.delta_seconds());)'
}

## TODO
#@bpy.utils.register_class
class Unity2BevyImportButton (bpy.types.Operator):
	bl_idname = 'bevy.import_from_unity'
	bl_label = 'Export To Bevy'
	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		InstallDepencies ()
		bevyExportPath = os.path.expanduser(context.scene.world.bevy_project_path)
		if not os.path.isdir(bevyExportPath):
			MakeFolderForFile (bevyExportPath + '/')
		importPath = os.path.expanduser(context.scene.world.unity_project_import_path)
		if importPath != '':
			BuildTool ('UnityToBevy')
			command = [ 'python3', os.path.join(thisDir, 'UnityToBevy.py'), 'input=' + importPath, 'output=' + bevyExportPath, 'exclude=/Library', 'webgl' ]
			print(command)

			subprocess.check_call(command)

@bpy.utils.register_class
class BevyExportButton (bpy.types.Operator):
	bl_idname = 'bevy.export'
	bl_label = 'Export To Bevy'
	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		InstallDepencies ()
		bevyExportPath = os.path.expanduser(context.scene.world.bevy_project_path)
		if not os.path.isdir(bevyExportPath):
			MakeFolderForFile (bevyExportPath + '/')
		data = bevyExportPath
		scripts_dict = {}
		for ob in bpy.data.objects:
			scripts = []
			for i in range(MAX_SCRIPTS_PER_OBJECT):
				txt = getattr(ob, 'bevyScript%s' % i)
				if txt:
					scripts.append(txt)
			if scripts:
				scripts_dict[ob] = scripts
				for script in scripts:
					data += '\n' + ob.name + '☢️' + '☣️'.join(script.name)
		open('/tmp/HolyBlender Data (BlenderToBevy)', 'wb').write(data.encode('utf-8'))
		import MakeBevyBlenderApp as makeBevyBlenderApp
		makeBevyBlenderApp.Do (scripts_dict)
		# webbrowser.open('http://localhost:1334')

@bpy.utils.register_class
class BevyTranslateButton (bpy.types.Operator):
	bl_idname = 'bevy.translate'
	bl_label = 'Translate To Bevy'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		global operatorContext
		global currentTextBlock
		BuildTool ('UnityToBevy')
		operatorContext = context
		script = currentTextBlock.name
		if not currentTextBlock.name.endswith('.cs'):
			script += '.cs'
		filePath = '/tmp/' + script
		open(filePath, 'wb').write(currentTextBlock.as_string().encode('utf-8'))
		ConvertCSFileToRust (filePath)

@bpy.utils.register_class
class WorldPanel (bpy.types.Panel):
	bl_idname = 'WORLD_PT_WorldBevy_Panel'
	bl_label = 'HolyBevy'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'
	
	def draw (self, context):
		self.layout.prop(context.world, 'bevy_project_path')
		self.layout.prop(context.world, 'holyserver')
		self.layout.prop(context.world, 'html_code')
		self.layout.operator('bevy.export', icon = 'CONSOLE')

@bpy.utils.register_class
class BevyScriptsPanel (bpy.types.Panel):
	bl_idname = 'OBJECT_PT_bevy_Scripts_Panel'
	bl_label = 'HolyBlender Bevy Scripts'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'

	def draw (self, context):
		self.layout.label(text='Attach bevy scripts')
		foundUnassignedScript = False
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			hasScript = getattr(context.active_object, 'bevyScript' + str(i)) != None
			if hasScript or not foundUnassignedScript:
				self.layout.prop(context.active_object, 'bevyScript' + str(i))
			if not foundUnassignedScript:
				foundUnassignedScript = not hasScript

def InstallDepencies ():
	sys.path.append(os.path.join(HOLY_BLENDER_PATH, 'Install Scripts'))
	import install_UnityToBevy

def ConvertCSFileToRust (filePath):
	global mainClassName
	mainClassName = filePath[filePath.rfind('/') + 1 : filePath.rfind('.')]
	assert os.path.isfile(filePath)
	MakeFolderForFile ('/tmp/src/main.rs')
	MakeFolderForFile ('/tmp/assets/registry.json')
	data = 'output=/tmp\n' + filePath
	open('/tmp/HolyBlender Data (UnityToBevy)', 'wb').write(data.encode('utf-8'))
	command = [
		'dotnet',
		os.path.join(thisDir,' HolyBlender.dll'), 
		'includeFile=' + filePath,
		'bevy=true',
		'output=/tmp'
	]
	# for arg in sys.argv:
	# 	command.append(arg)
	print(command)

	subprocess.check_call(command)

	outputFilePath = '/tmp/main.py'
	print(outputFilePath)
	assert os.path.isfile(outputFilePath)

	os.system('cat ' + outputFilePath)

	ConvertPythonFileToRust (outputFilePath)

def ConvertPythonFileToRust (filePath):
	global mainClassName
	lines = []
	for line in open(filePath, 'rb').read().decode('utf-8').splitlines():
		if line.startswith('import ') or line.startswith('from '):
			print('Skipping line:', line)
			continue
		lines.append(line)
	text = '\n'.join(lines)
	open(filePath, 'wb').write(text.encode('utf-8'))
	hasCorrectTextBlock = False
	textBlockName = filePath[filePath.rfind('/') + 1 :]
	for textBlock in bpy.data.texts:
		if textBlock.name == textBlockName:
			hasCorrectTextBlock = True
			break
	if not hasCorrectTextBlock:
		bpy.data.texts.new(textBlockName)
	textBlock = bpy.data.texts[textBlockName]
	textBlock.clear()
	textBlock.write(text)
	command = [ 'python3', 'py2many/py2many.py', '--rust=1', '--force', filePath, '--outdir=/tmp/src' ]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(os.path.expanduser(operatorContext.scene.world.unity_project_import_path))
	print(command)
	
	subprocess.check_call(command)

	outputFilePath = '/tmp/src/main.rs'
	assert os.path.isfile(outputFilePath)
	print(outputFilePath)

	os.system('cat ' + outputFilePath)
	
	data = open('/tmp/HolyBlender Data (UnityToBevy)', 'rb').read().decode('utf-8')
	filePath = data[data.find('\n') + 1 :]
	for textBlock in bpy.data.texts:
		if textBlock.name == filePath[filePath.rfind('/') + 1 :].replace('.rs', '.cs'):
			textBlock.name = textBlock.name.replace('.cs', '.rs')
			textBlock.clear()
			outputFileText = open('/tmp/src/main.rs', 'rb').read().decode('utf-8')
			textBlock.write(outputFileText)
