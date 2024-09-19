import bpy, subprocess, os, sys, hashlib, mathutils, math, base64, webbrowser

user_args = None
for arg in sys.argv:
	if arg == '--': user_args = []
	elif type(user_args) is list: user_args.append(arg)
if user_args: print('user_args:', user_args)

_thisdir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(_thisdir)
import libholy_bevy, libholy_godot, libholy_unity, libholy_unreal, libholyblender
sys.path.append(os.path.join(_thisdir, 'Blender_bevy_components_workflow/tools'))
print(sys.path)
import bevy_components
print(bevy_components)
import gltf_auto_export
print(gltf_auto_export)
bpy.ops.preferences.addon_enable(module='bevy_components')
bpy.ops.preferences.addon_enable(module='gltf_auto_export')

sys.path.append(os.path.join(_thisdir, 'Extensions'))
from SystemExtensions import *
from StringExtensions import *
from CollectionExtensions import *

if os.path.isdir(os.path.join(_thisdir,'Net-Ghost-SE')):
	sys.path.append(os.path.join(_thisdir,'Net-Ghost-SE'))
	import ghostblender
	print(ghostblender)
else:
	ghostblender = None

bl_info = {
	'name': 'HolyBlender',
	'blender': (2, 80, 0),
	'category': 'System',
}
REPLACE_INDICATOR = 'ꗈ'
EXAMPLES_DICT = {
	'Hello World (Unity)' : '''using UnityEngine;

public class HelloWorld : MonoBehaviour
{
	void Start ()
	{
		print("Hello World!");
	}
}''',
	'Rotate (Unity)': '''using UnityEngine;

public class Rotate : MonoBehaviour
{
	public float rotateSpeed = 50.0f;

	void Update ()
	{
		transform.eulerAngles += Vector3.up * rotateSpeed * Time.deltaTime;
	}
}''',
	'Grow And Shrink (Unity)': '''using UnityEngine;

public class GrowAndShrink : MonoBehaviour
{
	public float maxSize = 5.0f; 
	public float minSize = 0.2f;
	public float speed = 0.375f;

	void Update ()
	{
		transform.localScale = Vector3.one * (((Mathf.Sin(speed * Time.time) + 1) / 2) * (maxSize - minSize) + minSize);
	}
}''',
	'Keyboard And Mouse Controls (Unity)' : '''using UnityEngine;

public class WASDAndMouseControls : MonoBehaviour
{
	public float moveSpeed = 5.0f;

	void Update ()
	{
		Vector3 move = Vector3.zero;
		if (Input.GetKey(KeyCode.A))
			move.x -= 1.0f;
		if (Input.GetKey(KeyCode.D))
			move.x += 1.0f;
		if (Input.GetKey(KeyCode.S))
			move.y -= 1.0f;
		if (Input.GetKey(KeyCode.W))
			move.y += 1.0f;
		move.Normalize();
		transform.position += move * moveSpeed * Time.deltaTime;
		Vector3 mousePosition = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
		transform.up = mousePosition - transform.position;
	}
}''',
	'First Person Controls (Unity) (Unfinished)' : '''using UnityEngine;
using UnityEngine.InputSystem;

public class FirstPersonControls : MonoBehaviour
{
	public float moveSpeed = 5.0f;
	public float lookSpeed = 50.0f;
	Vector2 previousMousePosition;

	void Update ()
	{
		Vector3 move = Vector3.zero;
		if (Keyboard.current.aKey.isPressed)
			move.x -= 1.0f;
		if (Keyboard.current.dKey.isPressed)
			move.x += 1.0f;
		if (Keyboard.current.sKey.isPressed)
			move.y -= 1.0f;
		if (Keyboard.current.wKey.isPressed)
			move.y += 1.0f;
		move.Normalize();
		transform.position += move * moveSpeed * Time.deltaTime;
		Vector2 mousePosition = Mouse.current.position.ReadValue();
		Vector2 look = (mousePosition - previousMousePosition) * lookSpeed;
		transform.Rotate(new Vector3(look.y, look.x));
		previousMousePosition = mousePosition;
	}
}''',
	'Hello World (bevy)' : 'println!("Hello World!");',
	'Rotate (bevy)' : 'trs.rotate_y(5.0 * time.delta_seconds());)'
}
INIT_HTML = '''
<script>
function Test ()
{
	alert("Ok");
	//TODO xmlhttprequest
}
</script>
<button onclick="Test ()">Hello World!</button>
<a href="/bpy/data/objects/Cube">Cube</a>
'''
BLENDER_SERVER = '''
import bpy, json, base64, mathutils
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

LOCALHOST_PORT = 8000
POLL_INDICATOR = 'poll?'
JOIN_INDICATOR = 'join?'
LEFT_INDICATOR = 'left?'
JSON_INDICATOR = 'exec?'

events = []
clientIds = []
lastClientId = 0
unsentClientsEventsDict = {}

class BlenderServer (BaseHTTPRequestHandler):
	def do_GET (self):
		global events
		global clientIds
		global lastClientId
		global unsentClientsEventsDict
		self.send_response(200)
		self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
		self.send_header('Pragma', 'no-cache')
		self.send_header('Expires', '0')
		ret = 'OK'
		clientId = -1
		data = ''
		urlComponents = self.path.split('?')
		if len(urlComponents) > 1:
			clientId = urlComponents[-2]
			try:
				clientId = int(clientId)
			except:
				print('Player ' + str(lastClientId) + ' joined')
			data = urlComponents[-1]
		if self.path.endswith('.ico'):
			pass
		elif self.path == '/':
			if '__index__.html' in bpy.data.texts:
				ret = bpy.data.texts['__index__.html'].as_string()
			else:
				for t in bpy.data.texts:
					if t.name.endswith('.html'):
						ret = t.as_string()
						break
		elif self.path.startswith('/bpy/data/objects/'):
			name = self.path.split('/')[-1]
			if name in bpy.data.objects:
				ret = str(bpy.data.objects[name])
		elif os.path.isfile(self.path[1:]): # The .wasm file
			ret = open(self.path[1:], 'rb').read()
		elif self.path.endswith('.glb'):
			bpy.ops.object.select_all(action='DESELECT')
			name = self.path.split('/')[-1][: -len('.glb')]
			if name in bpy.data.objects:
				ob = bpy.data.objects[name]
				ob.select_set(True)
				tmp = '/tmp/__httpd__.glb'
				bpy.ops.export_scene.gltf(filepath=tmp, export_selected = True)
				ret = open(tmp,'rb').read()
		elif data in bpy.data.objects:
			ret = str(bpy.data.objects[data])
		elif self.path[1 :].startswith(JOIN_INDICATOR):
			clientIds.append(lastClientId)
			unsentClientsEventsDict[lastClientId] = events
			ret = str(lastClientId)
			lastClientId += 1
		elif self.path[1 :].startswith(LEFT_INDICATOR):
			clientIds.remove(clientId)
			del unsentClientsEventsDict[clientId]
		elif self.path[1 :].startswith(JSON_INDICATOR):
			jsonText = data
			jsonText = jsonText.encode("ascii")
			jsonText = base64.b64decode(jsonText)
			jsonText = jsonText.decode("ascii")
			jsonData = json.loads(jsonText)
			events.append(jsonData)
			obj = bpy.data.objects[jsonData['objectName']]
			valueName = jsonData['valueName']
			value = jsonData['value']
			if valueName == 'location':
				obj.location = mathutils.Vector((float(value['x']), float(value['y']), float(value['z'])))
			for _clientId in clientIds:
				if _clientId != clientId:
					unsentClientsEventsDict[_clientId].append(jsonData)
		else: # elif self.path[1 :].startswith(POLL_INDICATOR):
			ret = ''
			for event in unsentClientsEventsDict[clientId]:
				ret += str(event) + \'\\n\'
			unsentClientsEventsDict[clientId].clear()
		if ret is None:
			ret = 'None?'
		if type(ret) is not bytes:
			ret = ret.encode('utf-8')
		self.send_header('Content-Length', str(len(ret)))
		self.end_headers()
		try:
			self.wfile.write(ret)
		except BrokenPipeError:
			print('CLIENT WRITE ERROR: failed bytes', len(ret))

httpd = HTTPServer(('localhost', LOCALHOST_PORT), BlenderServer)
httpd.timeout=0.1
print(httpd)
timer = None
@bpy.utils.register_class
class HttpServerOperator (bpy.types.Operator):
	'HolyBlender HTTP Server'
	bl_idname = 'httpd.run'
	bl_label = 'httpd'
	bl_options = {'REGISTER'}

	def modal (self, context, event):
		if event.type == 'TIMER' and HTTPD_ACTIVE:
			httpd.handle_request() # Blocks for a short time
		return {'PASS_THROUGH'} # Doesn't supress event bubbles

	def invoke (self, context, event):
		global timer
		if timer is None:
			timer = self._timer = context.window_manager.event_timer_add(
				time_step=0.033333334,
				window=context.window
			)
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {'FINISHED'}

	def execute (self, context):
		return self.invoke(context, None)

HTTPD_ACTIVE = True
bpy.ops.httpd.run()'''
WATTS_TO_CANDELAS = 0.001341022
PI = 3.141592653589793
UNITY_SCRIPTS_PATH = os.path.join(_thisdir, 'Unity Scripts')
GODOT_SCRIPTS_PATH = os.path.join(_thisdir, 'Godot Scripts')
EXTENSIONS_PATH = os.path.join(_thisdir, 'Extensions')
TEMPLATES_PATH = os.path.join(_thisdir, 'Templates')
TEMPLATE_REGISTRY_PATH = os.path.join(TEMPLATES_PATH, 'registry.json')
REGISTRY_PATH = os.path.join('/tmp', 'registry.json')
MAX_SCRIPTS_PER_OBJECT = 16
NULL_INT = 1234567936
NULL_COLOR = [NULL_INT, NULL_INT, NULL_INT, NULL_INT]
unrealCodePath = ''
unrealCodePathSuffix = os.path.join('', 'Source', '')
excludeItems = [ os.path.join('', 'Library') ]
operatorContext = None
currentTextBlock = None
mainClassNames = []
attachedUnityScriptsDict = {}
attachedUnrealScriptsDict = {}
attachedGodotScriptsDict = {}
attachedBevyScriptsDict = {}
previousRunningScripts = []
textBlocksTextsDict = {}
previousTextBlocksTextsDict = {}
varaiblesTypesDict = {}
propertyNames = []
childrenDict = {}
gameObjectAndTrsVarsDict = {}

class ExamplesOperator (bpy.types.Operator):
	bl_idname = 'u2m.show_template'
	bl_label = 'Add or Remove'
	template : bpy.props.StringProperty(default = '')

	def invoke (self, context, event):
		if context.edit_text != None:
			context.edit_text.from_string(EXAMPLES_DICT[self.template])
		return {'FINISHED'}

class ExamplesMenu (bpy.types.Menu):
	bl_idname = 'TEXT_MT_u2m_menu'
	bl_label = 'HolyBlender Templates'

	def draw (self, context):
		layout = self.layout
		for name in EXAMPLES_DICT:
			op = layout.operator('u2m.show_template', text=name)
			op.template = name

class AttachedObjectsMenu (bpy.types.Menu):
	bl_idname = 'TEXT_MT_u2m_menu_obj'
	bl_label = 'HolyBlender Attached Objects'

	def draw (self, context):
		layout = self.layout
		if not context.edit_text:
			layout.label(text='No text block')
			return
		objs = []
		for obj in bpy.data.objects:
			attachedScripts = attachedUnityScriptsDict.get(obj, [])
			if context.edit_text.name in attachedScripts:
				objs.append(obj)
			attachedScripts = attachedBevyScriptsDict.get(obj, [])
			if context.edit_text.name in attachedScripts:
				objs.append(obj)
			attachedScripts = attachedUnrealScriptsDict.get(obj, [])
			if context.edit_text.name in attachedScripts:
				objs.append(obj)
		if objs:
			for obj in objs:
				layout.label(text=obj.name)
		else:
			layout.label(text='Script not attached to any objects')

class PlayButton (bpy.types.Operator):
	bl_idname = 'blender.play'
	bl_label = 'Start Playing (Unfinished)'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		for textBlock in bpy.data.texts:
			textBlock.run_cs = True

timer = None
class Loop (bpy.types.Operator):
	bl_idname = 'blender_plugin.start'
	bl_label = 'blender_plugin_start'
	bl_options = { 'REGISTER' }

	def modal (self, context, event):
		for area in bpy.data.screens['Layout'].areas:
			if area.type == 'VIEW_3D':
				for region in area.regions:
					if region.type == 'WINDOW':
						region.tag_redraw()
		return {'PASS_THROUGH'} # Won't supress event bubbles

	def invoke (self, context, event):
		global timer
		if timer is None:
			timer = self._timer = context.window_manager.event_timer_add(
				time_step=0.016666667,
				window=context.window)
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {'FINISHED'}

	def execute (self, context):
		return self.invoke(context, None)

classes = [
	PlayButton,
	ExamplesOperator,
	ExamplesMenu,
	AttachedObjectsMenu,
	Loop
]

def BuildTool (toolName : str):
	command = [ 'make', 'build_' + toolName ]
	print(command)

	subprocess.check_call(command)

def ExportObject (obj, folder : str) -> str:
	filePath = os.path.join(folder, obj.name + '.fbx')
	filePath = filePath.replace(' ', '_')
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	if obj.parent == None:
		fbxExporter.fix_object(obj)
	bpy.ops.export_scene.fbx(filepath=filePath, use_selection=True, use_custom_props=True, mesh_smooth_type='FACE')
	return filePath

def GetObjectBounds (obj) -> (mathutils.Vector, mathutils.Vector):
	_min = mathutils.Vector((float('inf'), float('inf'), float('inf')))
	_max = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))
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

def GetObjectId (obj):
	id = str(obj)
	idIndicator = 'at '
	id = id[id.rfind(idIndicator) + len(idIndicator) :]
	print('YAY' + id)
	return id

def GetGuid (filePath : str):
	return hashlib.md5(filePath.encode('utf-8')).hexdigest()

def ConvertCSFileToCPP (filePath):
	global mainClassNames
	global unrealCodePath
	global unrealCodePathSuffix
	assert os.path.isfile(filePath)
	unrealCodePath = os.path.expanduser(operatorContext.scene.world.unrealExportPath)
	unrealProjectName = unrealCodePath[unrealCodePath.rfind('/') + 1 :]
	unrealCodePathSuffix = '/Source/' + unrealProjectName
	unrealCodePath += unrealCodePathSuffix
	mainClassNames = [ os.path.split(filePath)[-1].split('.')[0] ]
	command = [
		'dotnet',
		os.path.expanduser('~/HolyBlender/UnityToUnreal/HolyBlender.dll'),
		'includeFile=' + filePath,
		'unreal=true',
		'output=' + unrealCodePath,
	]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(os.path.expanduser(operatorContext.scene.world.unity_project_import_path))
	print(command)

	subprocess.check_call(command)

	outputFilePath = unrealCodePath + filePath[filePath.rfind('/') :]
	outputFilePath = outputFilePath.replace('.cs', '.py')
	print(outputFilePath)
	assert os.path.isfile(outputFilePath)

	os.system('cat ' + outputFilePath)

	ConvertPythonFileToCPP (outputFilePath)

def ConvertPythonFileToCPP (filePath):
	global mainClassNames
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
	outputFilePath = unrealCodePath + '/' + textBlockName
	command = [ 'python3', os.path.expanduser('~/HolyBlender') + '/py2many/py2many.py', '--cpp=1', outputFilePath, '--unreal=1', '--outdir=' + unrealCodePath ]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(os.path.expanduser(operatorContext.scene.world.unrealExportPath))
	print(command)
	
	subprocess.check_call(command)

	outputFileText = open(outputFilePath.replace('.py', '.cpp'), 'rb').read().decode('utf-8')
	for mainClassName in mainClassNames:
		indexOfMainClassName = 0
		while indexOfMainClassName != -1:
			indexOfMainClassName = outputFileText.find(mainClassName, indexOfMainClassName + len(mainClassName))
			if indexOfMainClassName != -1 and outputFileText[indexOfMainClassName - 1 : indexOfMainClassName] != 'A' and not IsInString_CS(outputFileText, indexOfMainClassName):
				outputFileText = outputFileText[: indexOfMainClassName] + 'A' + outputFileText[indexOfMainClassName :]
		equalsNullIndicator = '= nullptr'
		indexOfEqualsNull = 0
		while indexOfEqualsNull != -1:
			indexOfEqualsNull = outputFileText.find(equalsNullIndicator, indexOfEqualsNull + len(equalsNullIndicator))
			if indexOfEqualsNull != -1:
				indexOfSpace = outputFileText.rfind(' ', 0, indexOfEqualsNull - 1)
				indexOfMainClassName = outputFileText.rfind(mainClassName, 0, indexOfSpace)
				if indexOfMainClassName == indexOfSpace - len(mainClassName):
					outputFileText = Remove(outputFileText, indexOfEqualsNull, len(equalsNullIndicator))
	pythonFileText = open(outputFilePath, 'rb').read().decode('utf-8')
	pythonFileLines = pythonFileText.split('\n')
	headerFileText = open(outputFilePath.replace('.py', '.h'), 'rb').read().decode('utf-8')
	for i in range(len(pythonFileLines) - 1, -1, -1):
		line = pythonFileLines[i]
		if not line.startswith(' '):
			line = line.replace(' ', '')
			indexOfColon = line.find(':')
			variableName = line[: indexOfColon]
			mainClassName = os.path.split(outputFilePath)[-1].split('.')[0]
			outputFileText = outputFileText.replace(variableName, variableName + '_' + mainClassName)
			headerFileText = headerFileText.replace(variableName, variableName + '_' + mainClassName)
			indexOfVariableName = headerFileText.find(variableName)
			indexOfNewLine = headerFileText.rfind('\n', 0, indexOfVariableName)
			headerFileText = headerFileText[: indexOfNewLine] + '\n\tUPROPERTY(EditAnywhere)' + headerFileText[indexOfNewLine :]
			indexOfEquals = line.find('=', indexOfColon + 1)
			variableName += '_' + mainClassName
			mainConstructor = '::A' + mainClassName + '() {'
			indexOfMainConstructor = outputFileText.find(mainConstructor)
			if indexOfEquals != -1:
				value = line[indexOfEquals + 1 :]
				outputFileText = outputFileText[: indexOfMainConstructor + len(mainConstructor) + 1] + '\t' + variableName + ' = ' + value + ';\n' + outputFileText[indexOfMainConstructor + len(mainConstructor) + 1 :]
		else:
			break
	outputFileLines = outputFileText.split('\n')
	for i in range(len(outputFileLines)):
		line = outputFileLines[i]
		line = line.replace(' ', '')
		indexOfX = 0
		while indexOfX != -1:
			indexOfX = line.find('.X', indexOfX + 1)
			if indexOfX != -1:
				indexOfEquals = line.find('=', indexOfX)
				if indexOfEquals != -1 and indexOfEquals <= indexOfX + 3:
					outputFileLines[i] = line[: indexOfEquals + 1] + '-' + line[indexOfEquals + 1 :]
	outputFileText = '\n'.join(outputFileLines)
	cppFilePath = outputFilePath.replace('.py', '.cpp')
	open(cppFilePath, 'wb').write(outputFileText.encode('utf-8'))
	open(outputFilePath.replace('.py', '.h'), 'wb').write(headerFileText.encode('utf-8'))
	command = [ 'cat', cppFilePath ]
	print(command)

	subprocess.check_call(command)
	
	for textBlock in bpy.data.texts:
		textBlockName = cppFilePath[cppFilePath.rfind('/') + 1 :].replace('.cpp', '')
		if textBlock.name == textBlockName:
			textBlockName += '.cpp+.h'
			hasCorrectTextBlock = False
			for textBlock in bpy.data.texts:
				if textBlock.name == textBlockName:
					hasCorrectTextBlock = True
					break
			if not hasCorrectTextBlock:
				bpy.data.texts.new(textBlockName)
			textBlock = bpy.data.texts[textBlockName]
			textBlock.clear()
			textBlock.write(outputFileText)
			textBlock.write(headerFileText)

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
		os.path.expanduser('~/HolyBlender/UnityToBevy/HolyBlender.dll'), 
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

def DrawExamplesMenu (self, context):
	self.layout.menu(ExamplesMenu.bl_idname)

def DrawAttachedObjectsMenu (self, context):
	self.layout.menu(AttachedObjectsMenu.bl_idname)

def SetupTextEditorFooterContext (self, context):
	global currentTextBlock
	global previousRunningScripts
	currentTextBlock = context.edit_text
	previousRunningScripts = []
	for textBlock in bpy.data.texts:
		if textBlock.run_cs and textBlock.name != '.gltf_auto_export_gltf_settings':
			previousRunningScripts.append(textBlock.name)

def DrawRunCSToggle (self, context):
	self.layout.prop(context.edit_text, 'run_cs')

def DrawIsInitScriptToggle (self, context):
	self.layout.prop(context.edit_text, 'is_init_script')

def OnUpdateUnityScripts (self, context):
	global attachedUnityScriptsDict
	attachedScripts = []
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		script = getattr(self, 'unity_script' + str(i))
		if script != None:
			attachedScripts.append(script.name)
			UpdateScriptVariables (script)
	attachedUnityScriptsDict[self] = attachedScripts

def OnUpdateUnrealScripts (self, context):
	global attachedUnrealScriptsDict
	attachedScripts = []
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		script = getattr(self, 'unreal_script' + str(i))
		if script != None:
			attachedScripts.append(script.name)
			UpdateScriptVariables (script)
	attachedUnrealScriptsDict[self] = attachedScripts

def OnUpdateGodotScripts (self, context):
	global attachedGodotScriptsDict
	attachedScripts = []
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		script = getattr(self, 'godotScript' + str(i))
		if script != None:
			attachedScripts.append(script.name)
			UpdateScriptVariables (script)
	attachedGodotScriptsDict[self] = attachedScripts

def OnUpdateBevyScripts (self, context):
	global attachedBevyScriptsDict
	attachedScripts = []
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		script = getattr(self, 'bevy_script' + str(i))
		if script != None:
			attachedScripts.append(script.name)
			UpdateScriptVariables (script)
	attachedBevyScriptsDict[self] = attachedScripts

def UpdateScriptVariables (textBlock):
	global attachedUnityScriptsDict
	global gameObjectAndTrsVarsDict
	global varaiblesTypesDict
	global propertyNames
	text = textBlock.as_string()
	publicIndicator = 'public '
	indexOfPublicIndicator = text.find(publicIndicator)
	while indexOfPublicIndicator != -1:
		indexOfType = indexOfPublicIndicator + len(publicIndicator)
		if text[indexOfType :].startswith('class '):
			indexOfPublicIndicator = text.find(publicIndicator, indexOfType)
			continue
		indexOfVariableName = indexOfType
		while indexOfVariableName < len(text) - 1:
			indexOfVariableName += 1
			if text[indexOfVariableName] != ' ':
				break
		if text[indexOfVariableName + 1] == '(':
			indexOfPublicIndicator = text.find(publicIndicator, indexOfType)
			continue
		indexOfVariableName = text.find(' ', indexOfVariableName + 1)
		type = text[indexOfType : indexOfVariableName]
		indexOfPotentialEndOfVariable = IndexOfAny(text, [ ' ', ';' , '=' ], indexOfVariableName + 1)
		variableName = text[indexOfVariableName : indexOfPotentialEndOfVariable]
		variableName = variableName.strip()
		shouldBreak = False
		for obj in attachedUnityScriptsDict.keys():
			for attachedScript in attachedUnityScriptsDict[obj]:
				if attachedScript == textBlock.name:
					propertyName = attachedScript + '_' + variableName
					if propertyName not in propertyNames:
						value = ''
						isSetToValue = False
						if text[indexOfPotentialEndOfVariable] == '=':
							indexOfSemicolon = text.find(';', indexOfPotentialEndOfVariable + 1)
							value = text[indexOfPotentialEndOfVariable + 1 : indexOfSemicolon]
							value = value.strip()
							isSetToValue = True
						if type == 'int':
							if not isSetToValue:
								value = 0
							else:
								try:
									i = 0.0
									i = value.replace('f', '')
									i = int(i)
									value = i
								except:
									print('Couldn\'t find the value' + variableName +  ' should be set to')
							setattr(bpy.types.Object, propertyName, bpy.props.IntProperty(name=propertyName, default=NULL_INT))
						elif type == 'float' or type == 'double':
							if not isSetToValue:
								value = 0.0
							else:
								try:
									f = value.replace('f', '')
									f = float(f)
									value = f
								except:
									print('Couldn\'t find the value' + variableName +  ' should be set to')
							setattr(bpy.types.Object, propertyName, bpy.props.FloatProperty(name=propertyName, default=NULL_INT))
						elif type == 'bool':
							if not isSetToValue:
								value = False
							elif value == 'true':
								value = True
							else:
								value = False
							setattr(bpy.types.Object, propertyName, bpy.props.BoolProperty(name=propertyName, default=NULL_INT))
						elif type == 'Color':
							color = [1, 1, 1, 1]
							if isSetToValue:
								try:
									colorIndicator = 'new Color('
									indexOfComma = value.find(',')
									color[0] = float(value[len(colorIndicator) : indexOfComma].replace('f', ''))
									indexOfComponentEnd = value.find(',', indexOfComma)
									color[1] = float(value[indexOfComma + 1 : indexOfComponentEnd].replace('f', ''))
									indexOfComma = indexOfComponentEnd
									indexOfComponentEnd = value.find(',', indexOfComma)
									gaveAlpha = indexOfComponentEnd != -1
									if not gaveAlpha:
										indexOfComponentEnd = value.find(')')
									color[2] = float(value[indexOfComma + 1 : indexOfComponentEnd].replace('f', ''))
									if gaveAlpha:
										indexOfComma = indexOfComponentEnd
										indexOfComponentEnd = value.find(')')
										color[3] = float(value[indexOfComma + 1 : indexOfComponentEnd].replace('f', ''))
								except:
									print('Couldn\'t find the value' + variableName +  ' should be set to')
							value = color
							setattr(bpy.types.Object, propertyName, bpy.props.FloatVectorProperty(name=propertyName, size=4, subtype='COLOR', soft_min=0, soft_max=1, default=NULL_COLOR))
						elif type == 'GameObject' or type == 'Transform':
							value = obj
							setattr(bpy.types.Object, propertyName, bpy.props.PointerProperty(name=propertyName, type=bpy.types.Object))
							if obj in gameObjectAndTrsVarsDict:
								gameObjectAndTrsVarsDict[obj].append(propertyName)
							else:
								gameObjectAndTrsVarsDict[obj] = [propertyName]
						setattr(obj, propertyName, value)
						propertyNames.append(propertyName)
					varaiblesTypesDict[propertyName] = type
					shouldBreak = True
					break
			if shouldBreak:
				break
		indexOfPublicIndicator = text.find(publicIndicator, indexOfType)

def OnRedrawView ():
	global currentTextBlock
	global textBlocksTextsDict
	global attachedUnityScriptsDict
	global previousRunningScripts
	global previousTextBlocksTextsDict
	textBlocksTextsDict = {}
	for textBlock in bpy.data.texts:
		if textBlock.name == '.gltf_auto_export_gltf_settings':
			continue
		textBlocksTextsDict[textBlock.name] = textBlock.as_string()
		if textBlock.name not in previousTextBlocksTextsDict or previousTextBlocksTextsDict[textBlock.name] != textBlock.as_string():
			UpdateScriptVariables (textBlock)
	previousTextBlocksTextsDict = textBlocksTextsDict.copy()
	bpy.types.TEXT_HT_footer.remove(SetupTextEditorFooterContext)
	bpy.types.TEXT_HT_footer.append(SetupTextEditorFooterContext)
	if currentTextBlock != None:
		if currentTextBlock.run_cs:
			import RunCSInBlender as runCSInBlender
			for obj in attachedUnityScriptsDict:
				if currentTextBlock.name in attachedUnityScriptsDict[obj]:
					filePath = os.path.expanduser('/tmp/HolyBlender Data (UnityInBlender)/' + currentTextBlock.name)
					filePath = filePath.replace('.cs', '.py')
					if not filePath.endswith('.py'):
						filePath += '.py'
					if currentTextBlock.name not in previousRunningScripts:
						MakeFolderForFile (filePath)
						open(filePath, 'wb').write(currentTextBlock.as_string().encode('utf-8'))
						BuildTool ('UnityInBlender')
						command = [
							'dotnet',
							os.path.expanduser('~/HolyBlender/UnityInBlender/HolyBlender.dll'), 
							'includeFile=' + filePath,
							'output=/tmp/HolyBlender Data (UnityInBlender)'
						]
						print(command)

						subprocess.check_call(command)

					runCSInBlender.Run (filePath, obj)

def register ():
	MakeFolderForFile ('/tmp/')
	registryText = open(TEMPLATE_REGISTRY_PATH, 'rb').read().decode('utf-8')
	registryText = registryText.replace('ꗈ', '')
	open(REGISTRY_PATH, 'wb').write(registryText.encode('utf-8'))
	registry = bpy.context.window_manager.components_registry
	registry.schemaPath = REGISTRY_PATH
	bpy.ops.object.reload_registry()
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.World.unity_project_import_path = bpy.props.StringProperty(
		name = 'Unity project import path',
		description = '',
		default = ''
	)
	bpy.types.World.unity_project_export_path = bpy.props.StringProperty(
		name = 'Unity project export path',
		description = '',
		default = '~/TestUnityProject'
	)
	# bpy.types.World.unity_export_version = bpy.props.StringProperty(
	# 	name = 'Unity export version',
	# 	description = '',
	# 	default = ''
	# )
	bpy.types.World.unrealExportPath = bpy.props.StringProperty(
		name = 'Unreal project path',
		description = '',
		default = '~/TestUnrealProject'
	)
	bpy.types.World.godotExportPath = bpy.props.StringProperty(
		name = 'Godot project path',
		description = '',
		default = '~/TestGodotProject'
	)
	bpy.types.World.bevy_project_path = bpy.props.StringProperty(
		name = 'Bevy project path',
		description = '',
		default = '~/TestBevyProject'
	)
	bpy.types.World.htmlExportPath = bpy.props.StringProperty(
		name = 'HTML project path',
		description = '',
		default = '~/TestHtmlProject'
	)
	bpy.types.World.holyserver = bpy.props.PointerProperty(name='Python Server', type=bpy.types.Text)
	bpy.types.World.html_code = bpy.props.PointerProperty(name='HTML code', type=bpy.types.Text)
	bpy.types.Object.html_on_click = bpy.props.PointerProperty(name='JavaScript on click', type=bpy.types.Text)
	bpy.types.Object.html_css = bpy.props.PointerProperty(name='CSS', type=bpy.types.Text)
	bpy.types.Text.run_cs = bpy.props.BoolProperty(
		name = 'Run C# Script',
		description = ''
	)
	bpy.types.Text.is_init_script = bpy.props.BoolProperty(
		name = 'Is Initialization Script',
		description = ''
	)
	bpy.types.TEXT_HT_header.append(DrawExamplesMenu)
	bpy.types.TEXT_HT_header.append(DrawAttachedObjectsMenu)
	bpy.types.TEXT_HT_footer.append(DrawRunCSToggle)
	bpy.types.TEXT_HT_footer.append(DrawIsInitScriptToggle)
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		setattr(bpy.types.Object, 'unity_script' + str(i), bpy.props.PointerProperty(name='Attach Unity script', type=bpy.types.Text, update=OnUpdateUnityScripts))
		setattr(bpy.types.Object, 'unreal_script' + str(i), bpy.props.PointerProperty(name='Attach Unreal script', type=bpy.types.Text, update=OnUpdateUnrealScripts))
		setattr(bpy.types.Object, 'godotScript' + str(i), bpy.props.PointerProperty(name='Attach Godot script', type=bpy.types.Text, update=OnUpdateGodotScripts))
		setattr(bpy.types.Object, 'bevy_script' + str(i), bpy.props.PointerProperty(name='Attach bevy script', type=bpy.types.Text, update=OnUpdateBevyScripts))
	for obj in bpy.context.scene.objects:
		attachedScripts = []
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			script = getattr(obj, 'unity_script' + str(i))
			if script != None:
				attachedScripts.append(script.name)
		attachedUnityScriptsDict[obj] = attachedScripts
		attachedScripts = []
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			script = getattr(obj, 'unreal_script' + str(i))
			if script != None:
				attachedScripts.append(script.name)
		attachedUnrealScriptsDict[obj] = attachedScripts
		attachedScripts = []
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			script = getattr(obj, 'godotScript' + str(i))
			if script != None:
				attachedScripts.append(script.name)
		attachedGodotScriptsDict[obj] = attachedScripts
		attachedScripts = []
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			script = getattr(obj, 'bevy_script' + str(i))
			if script != None:
				attachedScripts.append(script.name)
		attachedBevyScriptsDict[obj] = attachedScripts
	bpy.types.SpaceView3D.draw_handler_add(OnRedrawView, tuple([]), 'WINDOW', 'POST_PIXEL')
	bpy.ops.blender_plugin.start()

def unregister ():
	bpy.types.TEXT_HT_header.remove(DrawExamplesMenu)
	bpy.types.TEXT_HT_header.append(DrawAttachedObjectsMenu)
	bpy.types.TEXT_HT_footer.remove(DrawUnrealTranslateButton)
	bpy.types.TEXT_HT_footer.remove(DrawBevyTranslateButton)
	bpy.types.TEXT_HT_footer.remove(DrawRunCSToggle)
	bpy.types.TEXT_HT_footer.remove(DrawIsInitScriptToggle)
	for cls in classes:
		bpy.utils.unregister_class(cls)

def InitTexts ():
	if '__Html__.html' not in bpy.data.texts:
		textBlock = bpy.data.texts.new(name='__Html__.html')
		textBlock.from_string(INIT_HTML)
		if bpy.data.worlds[0].html_code == None:
			bpy.data.worlds[0].html_code = textBlock
	if '__Server__.py' not in bpy.data.texts:
		textBlock = bpy.data.texts.new(name='__Server__.py')
		textBlock.from_string(BLENDER_SERVER)
		if bpy.data.worlds[0].holyserver == None:
			bpy.data.worlds[0].holyserver = textBlock

if __name__ == '__main__':
	register ()
	InitTexts ()
	if user_args:
		for arg in user_args:
			if arg.endswith('.py'):
				print('exec:', arg)
				exec(open(arg).read())
			elif arg == '--test-unity':
				bpy.ops.unity.export()
