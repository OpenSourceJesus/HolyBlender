import subprocess, sys

command = [ 'blender', '--python', 'MakeBlenderPlugin.py' ]
# for arg in sys.argv:
#     command.append(arg)
print(command)

subprocess.check_call(command)