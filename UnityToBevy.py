import os, subprocess, sys

os.system('rm -r ' + os.getcwd() + '''/UnityToBevy
make build_UnityToBevy''')

command = [ 'blender', '--python', 'MakeBevyBlenderApp.py' ]
for arg in sys.argv:
    command.append(arg)
print(command)

subprocess.check_call(command)