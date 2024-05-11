import os

def ExcludeFolder (relativePath):
	fileLines.insert(12, '\t\t<Compile Remove=\"' + os.getcwd() + '/' + relativePath + '/**\" />\n')

if not os.path.isdir('CSharpToPython'):
	os.system('''git clone https://github.com/OpenSourceJesus/CSharpToPython.git --depth=1''')
if not os.path.isdir('py2many'):
	os.system('''git clone https://github.com/OpenSourceJesus/py2many.git --depth=1''')
os.system('''sudo apt install python3-setuptools
sudo apt install python3-toposort
sudo apt install clang-format
sudo apt install git-lfs''')
if not os.path.isdir('stride'):
	os.system('''git-lfs clone https://github.com/stride3d/stride --depth=1
		sudo apt install libfreetype6-dev
		sudo apt install libopenal-dev
		sudo apt install libsdl2-dev''')
os.system('''sudo apt install dotnet-sdk-8.0
cd BarerStrideProject/BarerStrideProject.Linux
dotnet add package Microsoft.CodeAnalysis
dotnet add package Microsoft.CodeAnalysis.CSharp
dotnet add package IronPython
dotnet add package Stride
dotnet add package Stride.Core
dotnet add package Stride.Core.Assets
dotnet add package Stride.Core.Assets.Quantum
dotnet add package Stride.Core.BuildEngine.Common
dotnet add package Stride.Core.Design
dotnet add package Stride.Core.IO
dotnet add package Stride.Core.Mathematics
dotnet add package Stride.Core.MicroThreading
dotnet add package Stride.Core.Packages
dotnet add package Stride.Core.Presentation
dotnet add package Stride.Core.Presentation.Quantum
dotnet add package Stride.Core.MicroThreading
dotnet add package Stride.Core.ProjectTemplating
dotnet add package Stride.Core.Quantum
dotnet add package Stride.Core.Reflection
dotnet add package Stride.Core.Serialization
dotnet add package Stride.Core.Shaders
dotnet add package Stride.Core.Tasks
dotnet add package Stride.Core.Translation
dotnet add package Stride.Core.Yaml
dotnet add package Stride.Core.FixProjectReferences
dotnet add package Stride.Irony
dotnet add package Stride.Shaders
dotnet add package Stride.Shaders.Compiler
dotnet add package Stride.Shaders.Parser
dotnet add package Stride.StorageTool
dotnet add package Stride.VisualStudio.Commands.Interfaces
dotnet add package xunit.runner.stride
dotnet add package Stride.Engine
dotnet add package Stride.Core.ObjectCollector''')

filePath = os.getcwd() + '/Unity2Many.csproj'
fileLines = open(filePath, "r").readlines()
ExcludeFolder ('BareUEProject')
ExcludeFolder ('obj')
ExcludeFolder ('CSharpToPython/src/CSharpToPython.Tests')