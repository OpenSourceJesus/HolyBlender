import subprocess, sys, os

os.system('''rm /tmp/Unity2Many Data (UnityToBevy)
    rm /tmp/Unity2Many Data (UnityToUnreal)''')

command = [ 'blender' ]
for arg in sys.argv:
    if arg.endswith('.blend'):
        command.append(os.path.expanduser(arg))
command += [ '--python', 'MakeBlenderPlugin.py' ]
print(command)

subprocess.check_call(command)