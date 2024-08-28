#!/usr/bin/env python3
import subprocess, sys, os
os.system('rm /tmp/HolyBlender*')

TEST_BEVY = '''
txt = bpy.data.texts.new(name='rotate.rs')
txt.from_string('trs.rotate_y(5.0 * time.delta_seconds());)')
bpy.data.objects["Cube"].bevy_script0 = txt
bpy.ops.bevy.export()
'''

TEST_HTML = '''
from random import random
for i in range(4):
	bpy.ops.mesh.primitive_cube_add()
	ob = bpy.context.active_object
	ob.location.x = i * 10
	ob.location.z = -i * 10
	ob.rotation_euler = [random(), random(), random()]
bpy.ops.html.export()
'''

blender = 'blender'
if sys.platform == 'win32': # Windows
	blender = 'C:/Program Files/Blender Foundation/Blender 4.2/blender.exe'
elif sys.platform == 'darwin': # Apple
	blender = '/Applications/Blender.app/Contents/MacOS/Blender'
command = []
user_script = None
user_opts   = []
test_bevy   = False
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
		user_script = sys.argv[ i+1 ]
	elif arg == '--test-bevy':
		test_bevy = True
		tmp = '/tmp/__test_bevy__.py'
		open(tmp,'w').write(TEST_BEVY)
		user_script = tmp
	elif arg == '--test-html':
		user_script = '/tmp/__test_html__.py'
		open(user_script,'w').write(TEST_HTML)

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

subprocess.check_call(command)
