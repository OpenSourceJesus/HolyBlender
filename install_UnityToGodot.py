import os

UNITY_2_MANY_PATH = os.path.expanduser('~/HolyBlender')

def ExcludeFolder (relativePath):
	fileLines.insert(12, '\t\t<Compile Remove=\"' + UNITY_2_MANY_PATH + '/' + relativePath + '/**\" />\n')

filePath = UNITY_2_MANY_PATH + "/HolyBlender.csproj"
fileLines = open(filePath, "r").readlines()
ExcludeFolder ("BareUEProject")
ExcludeFolder ("obj")
ExcludeFolder ("CSharpToPython/src/CSharpToPython.Tests")
open(actorClassPath, 'wb').writelines(fileLines)