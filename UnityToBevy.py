import subprocess, sys, os

os.system('rm -r ' + os.path.expanduser('~/Unity2Many/UnityToBevy') + '''
    make build_UnityToBevy''')

command = [ 'blender' ]
for arg in sys.argv:
    if arg.endswith('.blend'):
        command.append(os.path.expanduser(arg))
command += [ '--python', 'MakeBevyBlenderApp.py', 'fromUnity' ]
print(command)

subprocess.check_call(command)