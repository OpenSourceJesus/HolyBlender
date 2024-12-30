import bpy, subprocess, os, sys, hashlib
from mathutils import *

thisDir = os.path.split(os.path.abspath(__file__))[0]
HOLY_BLENDER_PATH = os.path.join(thisDir, '..')
sys.path.append(os.path.join(HOLY_BLENDER_PATH, 'Blender_To_Unity_FBX_Export'))
try:
	import Blender_To_Unity_FBX_Export as fbxExporter
	print(fbxExporter)
except:
	fbxExporter = None
if fbxExporter != None:
	bpy.ops.preferences.addon_enable(module='Blender_To_Unity_FBX_Export')

REPLACE_INDICATOR = 'ꗈ'
WATTS_TO_CANDELAS = 0.001341022
PI = 3.141592653589793
UNITY_SCRIPTS_PATH = os.path.join(HOLY_BLENDER_PATH, 'Unity Scripts')
GODOT_SCRIPTS_PATH = os.path.join(HOLY_BLENDER_PATH, 'Godot Scripts')
EXTENSIONS_PATH = os.path.join(HOLY_BLENDER_PATH, 'Extensions')
TEMPLATES_PATH = os.path.join(HOLY_BLENDER_PATH, 'Templates')
TEMPLATE_REGISTRY_PATH = os.path.join(TEMPLATES_PATH, 'registry.json')
REGISTRY_PATH = os.path.join('/tmp', 'registry.json')
MAX_SCRIPTS_PER_OBJECT = 32
NULL_INT = 1234567936
NULL_COLOR = [NULL_INT, NULL_INT, NULL_INT, NULL_INT]
unrealCodePath = ''
unrealCodePathSuffix = os.path.join('', 'Source', '')
excludeItems = [ os.path.join('', 'Library') ]
operatorContext = None
currentTextBlock = None
mainClassNames = []
previousRunningScripts = []
textBlocksTextsDict = {}
previousTextBlocksTextsDict = {}
varaiblesTypesDict = {}
propertyNames = []
childrenDict = {}
gameObjectAndTrsVarsDict = {}

bpy.types.World.holyserver = bpy.props.PointerProperty(name='Python Server', type=bpy.types.Text)
bpy.types.World.html_code = bpy.props.PointerProperty(name='HTML code', type=bpy.types.Text)
bpy.types.Object.html_on_click = bpy.props.PointerProperty(name='JavaScript on click', type=bpy.types.Text)
bpy.types.Object.html_css = bpy.props.PointerProperty(name='CSS', type=bpy.types.Text)

def GetScripts (mode):
	assert mode in 'unity unreal bevy godot'.split()
	scripts_dict = {}
	for ob in bpy.data.objects:
		scripts = []
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			txt = getattr(ob, '%s_script%s' % (mode,i))
			if txt:
				scripts.append(txt)
		if scripts:
			scripts_dict[ob] = scripts
	return scripts_dict

sys.path.append(EXTENSIONS_PATH)
from SystemExtensions import *
from StringExtensions import *
from CollectionExtensions import *

def BuildTool (toolName : str):
	command = [ 'make', 'build_' + toolName ]
	print(command)

	subprocess.check_call(command)

def ExportObject (obj, folder : str) -> str:
	filePath = os.path.join(folder, obj.name)
	filePath = filePath.replace(' ', '_')
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	if obj.parent == None:
		fbxExporter.fix_object(obj)
	bpy.ops.export_scene.gltf(filepath=filePath, use_selection=True)
	filePath += '.glb'
	return filePath

def GetObjectBounds (obj) -> (Vector, Vector):
	_min = Vector((float('inf'), float('inf'), float('inf')))
	_max = Vector((float('-inf'), float('-inf'), float('-inf')))
	if obj.type == 'MESH':
		for vertex in obj.data.vertices:
			vertex = obj.matrix_world @ vertex.co
			_min.x = min(vertex.x, _min.x)
			_min.y = min(vertex.y, _min.y)
			_min.z = min(vertex.z, _min.z)
			_max.x = max(vertex.x, _max.x)
			_max.y = max(vertex.y, _max.y)
			_max.z = max(vertex.z, _max.z)
	else:
		print('GetObjectBounds is not implemented for object types besides meshes')
	return ((_min + _max) / 2, _max - _min)

def GetGuid (filePath : str):
	return hashlib.md5(filePath.encode('utf-8')).hexdigest()
