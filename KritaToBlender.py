import subprocess

command = [ 'krita', '--python', 'MakeKritaBlenderFile.py' ]
print(command)

subprocess.check_call(command)