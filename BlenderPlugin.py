import subprocess, sys, os

os.system('''rm /tmp/Unity2Many Data (UnityToBevy)
	rm /tmp/Unity2Many Data (UnityToUnreal)''')

blender = 'blender'
if sys.platform == 'win32': # Windows
    blender = 'C:/Program Files/Blender Foundation/Blender 4.1/blender.exe'
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

subprocess.check_call(command)