import os

def ExcludeFolder (relativePath):
	fileLines.insert(12, '\t\t<Compile Remove=\"' + os.getcwd() + '/' + relativePath + '/**\" />\n')

if not os.path.isdir('CSharpToPython'):
	os.system('git clone https://github.com/OpenSourceJesus/CSharpToPython --depth=1')
if not os.path.isdir('py2many'):
	os.system('git clone https://github.com/OpenSourceJesus/py2many --depth=1')
if not os.path.isdir('Blender_bevy_components_workflow'):
	os.system('git clone https://github.com/OpenSourceJesus/Blender_bevy_components_workflow --depth=1')
os.system('''sudo apt-get install g++ pkg-config libx11-dev libasound2-dev libudev-dev libxkbcommon-x11-0
sudo apt -y install python3-numpy
sudo apt install python3-setuptools
sudo apt -y install python3-toposort
sudo apt -y install clang-format
sudo snap install blender --classic
sudo snap install rustup --classic
rustup default stable
sudo snap install dotnet-sdk --classic
dotnet new console --force
rm Program.cs
dotnet add package Microsoft.CodeAnalysis
dotnet add package Microsoft.CodeAnalysis.CSharp
dotnet add package IronPython
mkdir -p assets''')
if not os.path.isdir('src'):
	os.system('''cargo init
		cargo add bevy
		cargo add bevy_asset_loader
		cargo add bevy_gltf_components
		cargo add bevy_registry_export
		cargo add bevy_gltf_blueprints''')
filePath = os.getcwd() + '/Unity2Many.csproj'
fileLines = open(filePath, "r").readlines()
ExcludeFolder ('BareUEProject')
ExcludeFolder ('obj')
ExcludeFolder ('CSharpToPython/src/CSharpToPython.Tests')
ExcludeFolder ('stride')
ExcludeFolder ('BareStrideProject')
open(filePath, 'w').writelines(fileLines)