import os

thisDir = os.path.split(os.path.abspath(__file__))[0]
if not os.path.isdir(os.path.join(thisDir, 'blender-to-unity-fbx-exporter')):
	os.system('git clone https://github.com/OpenSourceJesus/blender-to-unity-fbx-exporter --depth=1')