import bpy, subprocess, os, sys, hashlib, mathutils, math, base64, webbrowser

user_args = None
for arg in sys.argv:
	if arg == '--': user_args = []
	elif type(user_args) is list: user_args.append(arg)
if user_args: print('user_args:', user_args)

_thisdir = os.path.split(os.path.abspath(__file__))[0]
if _thisdir not in sys.path: sys.path.append(_thisdir)

import libholy_unity
import libholy_unreal
import libholy_bevy
import libholy_godot


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


class WorldPanel (bpy.types.Panel):
	bl_idname = 'WORLD_PT_World_Panel'
	bl_label = 'HolyBlender Export'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'

	def draw (self, context):
		self.layout.prop(context.world, 'unity_project_import_path')
		self.layout.prop(context.world, 'unity_project_export_path')
		self.layout.prop(context.world, 'unrealExportPath')
		self.layout.prop(context.world, 'godotExportPath')
		self.layout.prop(context.world, 'bevy_project_path')
		self.layout.prop(context.world, 'htmlExportPath')
		self.layout.prop(context.world, 'holyserver')
		self.layout.prop(context.world, 'html_code')
		self.layout.operator(UnityExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(UnrealExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(GodotExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(BevyExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(HTMLExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(PlayButton.bl_idname, icon='CONSOLE')

class ScriptVariablesPanel (bpy.types.Panel):
	bl_label = "Scripts Public Variables"
	bl_idname = "OBJECT_PT_Script_Public_Variables"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "object"

	def draw (self, context):
		for propertyName in propertyNames:
			if varaiblesTypesDict[propertyName] == 'Color':
				if not Equals(getattr(context.active_object, propertyName), NULL_COLOR):
					self.layout.prop(context.active_object, propertyName)
			elif varaiblesTypesDict[propertyName] == 'GameObject' or varaiblesTypesDict[propertyName] == 'Transform':
				if propertyName in gameObjectAndTrsVarsDict[context.active_object]:
					self.layout.prop(context.active_object, propertyName)
			else:
				self.layout.prop(context.active_object, propertyName)



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

class HTMLExportButton (bpy.types.Operator):
	bl_idname = 'html.export'
	bl_label = 'Export To HTML'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		htmlExportPath = os.path.expanduser(context.scene.world.htmlExportPath)
		previousVisibleObjects = []
		for obj in bpy.data.objects:
			if obj.type == 'MESH' and not obj.hide_get():
				previousVisibleObjects.append(obj)
				obj.hide_render = True
		bpy.context.scene.render.resolution_percentage = 10
		camera = bpy.data.cameras[0]
		cameraObj = bpy.data.objects[camera.name]
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.view_layer.objects.active = cameraObj
		cameraObj.select_set(True)
		bpy.context.scene.camera = cameraObj
		for area in bpy.context.screen.areas:
			if area.type == 'VIEW_3D':
				area.spaces.active.region_3d.view_perspective = 'CAMERA'
				break
		bpy.context.scene.render.film_transparent = True
		bpy.context.scene.render.image_settings.color_mode = 'RGBA'
		previousCameraLocation = cameraObj.location
		previousCameraRotationMode = cameraObj.rotation_mode
		cameraObj.rotation_mode = 'XYZ'
		previousCameraRotation = cameraObj.rotation_euler
		previousCameraType = camera.type
		camera.type = 'ORTHO'
		previousCameraOrthoScale = camera.ortho_scale
		html = [
			'<!DOCTYPE html>',
			'<html><head><script>',
		]
		js_blocks = {}
		imgs = []
		for obj in bpy.data.objects:
			if obj.type == 'MESH':
				obj.hide_render = False
				bpy.context.scene.render.filepath = htmlExportPath + '/' + obj.name
				cameraObj.rotation_euler = mathutils.Vector((math.radians(90), 0, 0))
				bounds = GetObjectBounds(obj)
				cameraObj.location = bounds[0] - mathutils.Vector((0, bounds[1].y, 0))
				camera.ortho_scale = max(bounds[1].x, bounds[1].z) * 2
				if os.path.isfile( htmlExportPath + '/' + obj.name ) and '--skip-render' in sys.argv:
					pass
				else:
					bpy.ops.render.render(animation=False, write_still=True)
				obj.hide_render = True
				imagePath = bpy.context.scene.render.filepath + '.png'
				command = [ 'convert', '-delay', '10', '-loop', '0', imagePath, imagePath.replace('.png', '.gif') ]
				subprocess.check_call(command)
				imagePath = imagePath.replace('.png', '.gif')
				cameraSize = mathutils.Vector((camera.sensor_width, camera.sensor_height))
				imageData = open(imagePath, 'rb').read()
				base64EncodedStr = base64.b64encode(imageData).decode('utf-8')
				multiplyUnits = 50
				zIndex = int(bounds[0].y)
				zIndex += 10
				if zIndex < 0:
					zIndex = 0
				onclick =  ''
				if obj.html_on_click:
					fname = '__on_click_' + obj.html_on_click.name.replace('.','_')
					if obj.html_on_click.name not in js_blocks:
						js = 'function %s(self){%s}' % (fname, obj.html_on_click.as_string())
						js_blocks[obj.html_on_click.name] = js
					onclick = 'javascript:%s(this)' % fname
				userCss = ''
				if obj.html_css:
					userCss = obj.html_css.as_string().replace('\n', ' ').strip()
				imageText = '<img id="%s" onclick="%s" style="position:fixed; left:%spx; top:%spx; z-index:%s;%s" src="data:image/gif;base64,%s">\n' %(
					obj.name,
					onclick,
					bounds[0].x * multiplyUnits,
					-bounds[0].z * multiplyUnits,
					zIndex,
					userCss,
					base64EncodedStr
				)
				imgs.append(imageText)
		for obj in previousVisibleObjects:
			obj.hide_render = False
		cameraObj.location = previousCameraLocation
		cameraObj.rotation_mode = previousCameraRotationMode
		cameraObj.rotation_euler = previousCameraRotation
		camera.type = previousCameraType
		camera.ortho_scale = previousCameraOrthoScale
		for tname in js_blocks:
			html.append('//' + tname)
			html.append(js_blocks[tname])
		html.append('</script>')
		html.append('</head>')
		html.append('<body>')
		html += imgs
		html.append('</body></html>')
		htmlText = '\n'.join(html)
		open(htmlExportPath + '/index.html', 'wb').write(htmlText.encode('utf-8'))
		if '__index__.html' not in bpy.data.texts:
			bpy.data.texts.new(name='__index__.html')
		bpy.data.texts['__index__.html'].from_string(htmlText)
		if bpy.data.worlds[0].holyserver:
			scope = globals()
			exec(bpy.data.worlds[0].holyserver.as_string(), scope, scope)
			webbrowser.open('http://localhost:8000/')
		else:
			webbrowser.open(htmlExportPath + '/index.html')
		return {'FINISHED'}



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


if __name__ == '__main__':
	if user_args:
		for arg in user_args:
			if arg.endswith('.py'):
				print('exec:', arg)
				exec(open(arg).read())
			elif arg == '--test-unity':
				bpy.ops.unity.export()
