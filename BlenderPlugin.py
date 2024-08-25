import subprocess, sys, os

os.system('rm /tmp/HolyBlender*')

blender = 'blender'
if sys.platform == 'win32': # Windows
    blender = 'C:/Program Files/Blender Foundation/Blender 4.2/blender.exe'
elif sys.platform == 'darwin': # Apple
    blender = '/Applications/Blender.app/Contents/MacOS/Blender'
command = []
for arg in sys.argv:
	if arg.endswith('.blend'):
		command.append(os.path.expanduser(arg))
	elif arg.endswith('.exe'): # Windows
		blender = arg
	elif arg.endswith('.app'): # Apple
		blender = arg + '/Contents/MacOS/Blender'
	elif arg.endswith(('blender', 'Blender')):
		blender = arg

command = [blender] + command + [ '--python', 'MakeBlenderPlugin.py' ]
print(command)

if not os.path.isdir('./Blender_bevy_components_workflow'):
	cmd = 'git clone https://github.com/OpenSourceJesus/Blender_bevy_components_workflow --depth=1'
	print(cmd)
	subprocess.check_call(cmd.split())

subprocess.check_call(command)
