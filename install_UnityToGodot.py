import os

def ExcludeFolder (relativePath):
	contents.insert(12, "\t\t<Compile Remove=\"" + os.getcwd() + "/" + relativePath + "/**\" />\n")

filePath = os.getcwd() + "/Unity2Many.csproj"
with open(filePath, "r") as file:
	contents = file.readlines()
ExcludeFolder ("BareUEProject")
ExcludeFolder ("obj")
ExcludeFolder ("CSharpToPython/src/CSharpToPython.Tests")
with open(filePath, "w") as file:
	file.writelines(contents)