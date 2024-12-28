import os

HOLY_BLENDER_PATH = os.path.expanduser('~/HolyBlender')

def ExcludeFolder (relativePath):
	fileLines.insert(12, '\t\t<Compile Remove=\"' + HOLY_BLENDER_PATH + '/' + relativePath + '/**\" />\n')

if not os.path.isdir('CSharpToPython'):
	os.system('''git clone https://github.com/OpenSourceJesus/CSharpToPython.git --depth=1''')
if not os.path.isdir('py2many'):
	os.system('''git clone https://github.com/OpenSourceJesus/py2many.git --depth=1''')
os.system('''sudo apt -y install python3-setuptools
	sudo apt -y install python3-toposort
	sudo apt -y install clang-format
	cd ~
	git clone https://github.com/OpenSourceJesus/UnrealEngine --depth=1
	cd UnrealEngine
	./Setup.sh
	./GenerateProjectFiles.sh
	make
	cd ~/HolyBlender
	wget https://dot.net/v1/dotnet-install.sh -O dotnet-install.sh
	chmod +x ./dotnet-install.sh
	./dotnet-install.sh --version 6.0.423
	dotnet new console --force
	rm Program.cs
	dotnet add package Microsoft.CodeAnalysis
	dotnet add package Microsoft.CodeAnalysis.CSharp
	dotnet add package IronPython
	dotnet add package System.Resources.Extensions''')

filePath = HOLY_BLENDER_PATH + '/HolyBlender.csproj'
fileLines = open(filePath, "rb").read().decode('utf-8').split('\n')
ExcludeFolder ('BareUEProject')
ExcludeFolder ('obj')
ExcludeFolder ('CSharpToPython/src/CSharpToPython.Tests')
ExcludeFolder ('stride')
ExcludeFolder ('BareStrideProject')
open(filePath, 'wb').write('\n'.join(fileLines).encode('utf-8'))
actorClassPath = os.path.expanduser('~/UnrealEngine/Engine/Source/Runtime/Engine/Private/Actor.cpp')
fileLines = open(actorClassPath, 'rb').read().decode('utf-8').split('\n')
i = 0
while i < len(fileLines):
	line = fileLines[i]
	if 'check(ThreadContext.TestRegisterTickFunctions == nullptr);' in line:
		fileLines[i] = '//' + line
		break
	i += 1
open(actorClassPath, 'wb').write('\n'.join(fileLines).encode('utf-8'))