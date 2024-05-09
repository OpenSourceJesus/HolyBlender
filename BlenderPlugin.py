import os, subprocess, sys

os.system('rm -r ' + os.getcwd() + '''/BlenderPlugin
make build_BlenderPlugin''')

command = [ 'blender', '--python', 'MakeBlenderPlugin.py' ]
for arg in sys.argv:
    print('WOW' + arg)
    command.append(arg)
print(command)

subprocess.check_call(command)