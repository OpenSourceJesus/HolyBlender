import os

HOLY_BLENDER_PATH = os.path.expanduser('~/HolyBlender')
LIBS_PATH = os.path.join(HOLY_BLENDER_PATH, 'libs')

thisDir = os.path.split(os.path.abspath(__file__))[0]
thisDir = thisDir.replace('/dist/BlenderPlugin/_interrnal', '')
if not os.path.isdir(os.path.join(thisDir, 'Blender_To_Unity_FBX_Export')):
	os.system('git clone https://github.com/OpenSourceJesus/Blender_To_Unity_FBX_Export --depth=1')
if not os.path.isdir(os.path.join(thisDir, 'UnityGLTF')):
	os.system('git clone https://github.com/OpenSourceJesus/UnityGLTF --depth=1')
os.system('''pip install Wand --break-system-packages
	cp -r ~/.local/lib/python3.12/site-packages/wand ''' + HOLY_BLENDER_PATH + '''/wand''')