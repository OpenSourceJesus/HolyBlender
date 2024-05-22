import os

UNITY_2_MANY_PATH = os.path.expanduser('~/Unity2Many')

def ExcludeFolder (relativePath):
	fileLines.insert(12, '\t\t<Compile Remove=\"' + UNITY_2_MANY_PATH + '/' + relativePath + '/**\" />\n')

if not os.path.isdir('CSharpToPython'):
	os.system('''git clone https://github.com/OpenSourceJesus/CSharpToPython.git --depth=1''')
if not os.path.isdir('py2many'):
	os.system('''git clone https://github.com/OpenSourceJesus/py2many.git --depth=1''')
os.system('''sudo apt install python3-setuptools
sudo apt install python3-toposort
sudo apt install clang-format
cd ~
git clone https://github.com/OpenSourceJesus/UnrealEngine --depth=1
cd UnrealEngine
./Setup.sh
./GenerateProjectFiles.sh
make
cd ../Unity2Many
sudo apt install dotnet-sdk-6.0
dotnet new console --force
rm Program.cs
dotnet add package Microsoft.CodeAnalysis
dotnet add package Microsoft.CodeAnalysis.CSharp
dotnet add package IronPython
dotnet add package System.Resources.Extensions''')

filePath = UNITY_2_MANY_PATH + '/Unity2Many.csproj'
fileLines = open(filePath, "r").readlines()
ExcludeFolder ('BareUEProject')
ExcludeFolder ('obj')
ExcludeFolder ('CSharpToPython/src/CSharpToPython.Tests')
ExcludeFolder ('stride')
ExcludeFolder ('BareStrideProject')
open(filePath, 'w').writelines(fileLines)
actorClassPath = os.path.expanduser('~/UnrealEngine/Engine/Source/Runtime/Engine/Private/Actor.cpp')
fileLines = open(actorClassPath, 'wb').readliens()
i = 0
while i < len(fileLines):
	line = fileLines[i]
	if 'check(' in line:
		fileLines[i] = '//' + line
	i += 1
open(actorClassPath, 'wb').writelines(fileLines)