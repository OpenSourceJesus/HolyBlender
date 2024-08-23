import os

UNITY_2_MANY_PATH = os.path.expanduser('~/HolyBlender')

def ExcludeFolder (relativePath):
	fileLines.insert(12, '\t\t<Compile Remove=\"' + UNITY_2_MANY_PATH + '/' + relativePath + '/**\" />\n')

if not os.path.isdir(UNITY_2_MANY_PATH + '/CSharpToPython'):
	os.system('git clone https://github.com/OpenSourceJesus/CSharpToPython --depth=1')
if not os.path.isdir(UNITY_2_MANY_PATH + '/Blender_bevy_components_workflow'):
	os.system('git clone https://github.com/OpenSourceJesus/Blender_bevy_components_workflow --depth=1')
os.system('''sudo snap install blender --classic
	sudo apt -y install make
	sudo apt -y install dotnet-sdk-8.0
	dotnet new console --force
	rm Program.cs
	dotnet add package Microsoft.CodeAnalysis
	dotnet add package Microsoft.CodeAnalysis.CSharp
	dotnet add package IronPython
	dotnet add package System.Resources.Extensions
	pip install pynput --break-system-packages''')

filePath = UNITY_2_MANY_PATH + '/HolyBlender.csproj'
fileLines = open(filePath, "rb").read().decode('utf-8').split('\n')
ExcludeFolder ('BareUEProject')
ExcludeFolder ('obj')
ExcludeFolder ('CSharpToPython/src/CSharpToPython.Tests')
ExcludeFolder ('stride')
ExcludeFolder ('BareStrideProject')
open(filePath, 'wb').write('\n'.join(fileLines).encode('utf-8'))