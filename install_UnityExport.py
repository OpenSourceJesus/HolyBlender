import os

cmd = 'pip install -U unityparser'
if os.uname().nodename != 'pop-os':
	cmd += ' --break-system-packages'

os.system(cmd)