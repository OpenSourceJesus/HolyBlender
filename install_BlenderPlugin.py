import os

UNITY_2_MANY_PATH = os.path.expanduser('~/HolyBlender')

if not os.path.isdir(UNITY_2_MANY_PATH + '/Blender_bevy_components_workflow'):
	os.system('git clone https://github.com/OpenSourceJesus/Blender_bevy_components_workflow --depth=1')
os.system('''sudo apt install snapd
	sudo snap install blender --classic
	sudo apt -y install make''')