import subprocess, sys, os

os.system('''rm /tmp/Unity2Many Data (UnityToBevy)
	rm /tmp/Unity2Many Data (UnityToUnreal)''')

blender = 'blender'
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