import os

thisDir = os.path.split(os.path.abspath(__file__))[0]
if not os.path.isdir(os.path.join(thisDir, 'blender-to-unity-fbx-exporter')):
	os.system('git clone https://github.com/OpenSourceJesus/blender-to-unity-fbx-exporter --depth=1')

cmd = '''wget https://packages.microsoft.com/config/debian/12/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt-get update && \
	sudo apt-get install -y dotnet-sdk-8.0'''

os.system(cmd)