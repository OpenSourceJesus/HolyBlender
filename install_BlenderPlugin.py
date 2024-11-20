import os

HOLY_BLENDER_PATH = os.path.expanduser('~/HolyBlender')

if not os.path.isdir(HOLY_BLENDER_PATH + '/Blender_bevy_components_workflow'):
	os.system('git clone https://github.com/OpenSourceJesus/Blender_bevy_components_workflow --depth=1')
os.system('''sudo apt -y install snapd
	sudo snap install blender --classic''')