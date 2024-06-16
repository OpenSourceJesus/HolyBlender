import os

UNITY_2_MANY_PATH = os.path.expanduser('~/Unity2Many')

if not os.path.isdir(UNITY_2_MANY_PATH + '/CSharpToPython'):
	os.system('git clone https://github.com/OpenSourceJesus/CSharpToPython --depth=1')
if not os.path.isdir(UNITY_2_MANY_PATH + '/Blender_bevy_components_workflow'):
	os.system('git clone https://github.com/OpenSourceJesus/Blender_bevy_components_workflow --depth=1')
os.system('''sudo snap install blender --classic
	sudo apt -y install make''')