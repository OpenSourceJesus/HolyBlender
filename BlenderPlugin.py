import subprocess, sys, os
os.system('rm /tmp/HolyBlender*')
monogame = netghost = False

TEST_BEVY = '''
txt = bpy.data.texts.new(name='rotate.rs')
txt.from_string('trs.rotate_y(5.0 * time.delta_seconds());)')
bpy.data.objects["Cube"].bevy_script0 = txt
bpy.ops.bevy.export()
'''

TEST_SERVER = '''
import bpy
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

LOCALHOST_PORT = 8000

class BlenderServer (BaseHTTPRequestHandler):
	def do_GET (self):
		self.send_response(200)
		self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
		self.send_header("Pragma", "no-cache")
		self.send_header("Expires", "0")

		ret = 'OK'
		hint = ''
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
		elif os.path.isfile(self.path[1:]): # the .wasm file
			ret = open(self.path[1:], 'rb').read()
		elif self.path.endswith('.glb'):
			bpy.ops.object.select_all(action='DESELECT')
			name = self.path.split('/')[-1][: -len('.glb') ]
			if name in bpy.data.objects:
				ob = bpy.data.objects[name]
				ob.select_set(True)
				tmp = '/tmp/__httpd__.glb'
				bpy.ops.export_scene.gltf(filepath=tmp, export_selected = True)
				ret = open(tmp,'rb').read()
		elif self.path[1:] in bpy.data.objects:
			ret = str(bpy.data.objects[self.path[1:]])

		if ret is None:
			ret = 'None?'
		if type(ret) is not bytes:
			ret = ret.encode('utf-8')

		self.send_header("Content-Length", str(len(ret)))
		self.end_headers()

		try:
			self.wfile.write( ret )
		except BrokenPipeError:
			print('CLIENT WRITE ERROR: failed bytes', len(ret))

httpd = HTTPServer(('localhost', LOCALHOST_PORT), BlenderServer)
httpd.timeout=0.1
print(httpd)
timer = None
@bpy.utils.register_class
class HttpServerOperator (bpy.types.Operator):
	"HolyBlender HTTP Server"
	bl_idname = "httpd.run"
	bl_label = "httpd"
	bl_options = {'REGISTER'}

	def modal (self, context, event):
		if event.type == "TIMER":
			if HTTPD_ACTIVE:
				httpd.handle_request() # this blocks for a short time
		return {'PASS_THROUGH'} # will not supress event bubbles

	def invoke (self, context, event):
		global timer
		if timer is None:
			timer = self._timer = context.window_manager.event_timer_add(
				time_step=0.016666667,
				window=context.window
			)
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {'FINISHED'}

	def execute (self, context):
		return self.invoke(context, None)

HTTPD_ACTIVE = True
bpy.ops.httpd.run()

'''

TEST_HTML = '''
from random import random

SERVER = """%s"""
server = bpy.data.texts.new(name='__server__.py')
server.from_string(SERVER)
bpy.data.worlds[0].holyserver = server

JS = """
window.alert(self);
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
	console.log(this.readyState);
	console.log(this.status);
	console.log(self);
	if (this.readyState == 4 && this.status == 200) {
		self.innerHTML = xhttp.responseText.replaceAll('<', '[').replaceAll('>', ']');
	}
};
xhttp.overrideMimeType( "text/plain; charset=utf-8" );
xhttp.open("GET", self.getAttribute('id'), true);
xhttp.send();
"""

onclick = bpy.data.texts.new(name='onclick.js')
onclick.from_string(JS)

CSS = """
box-shadow: 5px 5px 10px black;
"""
css = bpy.data.texts.new(name='css')
css.from_string(CSS)

for i in range(4):
	bpy.ops.mesh.primitive_cube_add()
	ob = bpy.context.active_object
	ob.location.x = i * 3
	ob.location.z = -i * 3
	ob.rotation_euler = [random(), random(), random()]
	ob.html_on_click = onclick
	ob.html_css = css
bpy.ops.html.export()
''' % TEST_SERVER

blender = 'blender'
if sys.platform == 'win32': # Windows
	blender = 'C:/Program Files/Blender Foundation/Blender 4.2/blender.exe'
elif sys.platform == 'darwin': # Apple
	blender = '/Applications/Blender.app/Contents/MacOS/Blender'
command = []
user_script = None
user_opts = []
test_bevy = False
for i,arg in enumerate(sys.argv):
	if arg.endswith('.blend'):
		command.append(os.path.expanduser(arg))
	elif arg.endswith('.exe'): # Windows
		blender = arg
	elif arg.endswith('.app'): # Apple
		blender = arg + '/Contents/MacOS/Blender'
	elif arg.endswith(('blender', 'Blender')):
		blender = arg
	elif arg == '--eval':
		user_script = sys.argv[i + 1]
	elif arg == '--test-bevy':
		test_bevy = True
		tmp = '/tmp/__test_bevy__.py'
		open(tmp,'w').write(TEST_BEVY)
		user_script = tmp
	elif arg == '--test-html':
		user_script = '/tmp/__test_html__.py'
		open(user_script,'w').write(TEST_HTML)
	elif arg == '--ghost':
		netghost = True
	elif arg == '--monogame' in sys.argv:
		monogame = True
	elif arg.startswith('--'):
		user_opts.append(arg)

command = [blender] + command + [ '--python', 'MakeBlenderPlugin.py' ]

if user_script or user_opts:
	command.append('--')
if user_script:
	command.append(user_script)
if user_opts:
	command += user_opts
print(command)

if not os.path.isdir('./Blender_bevy_components_workflow'):
	cmd = 'git clone https://github.com/OpenSourceJesus/Blender_bevy_components_workflow --depth=1'
	print(cmd)
	
	subprocess.check_call(cmd.split())

if netghost and not os.path.isdir('./Net-Ghost-SE'):
	cmd = 'git clone https://github.com/brentharts/Net-Ghost-SE.git --depth=1'
	print(cmd)
	subprocess.check_call(cmd.split())

if monogame:
	if not os.path.isdir('./MonoGame'):
		cmd = 'git clone https://github.com/MonoGame/MonoGame.git --depth=1'
		print(cmd)
		subprocess.check_call(cmd.split())
	subprocess.check_call(['bash', './build.sh'], cwd='./MonoGame')

## run blender
subprocess.check_call(command)
