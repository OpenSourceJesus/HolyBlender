import os, subprocess, sys
# from GetUnityProjectInfo import *
from StringExtensions import *
from SystemExtensions import *

UNITY_PROJECT_PATH = ''
UNREAL_COMMAND_PATH = os.getcwd() + '/../UnrealEngine/Engine/Binaries/Linux/UnrealEditor-Cmd'
UNREAL_PROJECT_PATH = ''
MAKE_UNREAL_PROJECT_SCRIPT_PATH = os.getcwd() + '/MakeUnrealProject.py'
CODE_PATH = UNREAL_PROJECT_PATH + '/Source/' + UNREAL_PROJECT_PATH[UNREAL_PROJECT_PATH.rfind('/') + 1 :]
INPUT_PATH_INDICATOR = 'input='
OUTPUT_PATH_INDICATOR = 'output='
EXCLUDE_ITEM_INDICATOR = 'exclude='
SCRIPT_INDICATOR = '  m_Script: '
GUID_INDICATOR = 'guid: '
CLASS_MEMBER_INDICATOR = '#💠'
mainClassNames = []
excludeItems = []
membersDict = {}

for arg in sys.argv:
	if arg.startswith(INPUT_PATH_INDICATOR):
		UNITY_PROJECT_PATH = os.path.expanduser(arg[len(INPUT_PATH_INDICATOR) :])
	elif arg.startswith(OUTPUT_PATH_INDICATOR):
		UNREAL_PROJECT_PATH = os.path.expanduser(arg[len(OUTPUT_PATH_INDICATOR) :])
		CODE_PATH = UNREAL_PROJECT_PATH + '/Source/' + UNREAL_PROJECT_PATH[UNREAL_PROJECT_PATH.rfind('/') + 1 :]
	elif arg.startswith(EXCLUDE_ITEM_INDICATOR):
		excludeItems.append(arg[len(EXCLUDE_ITEM_INDICATOR) :])

metaFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.meta')
fileGuidsDict = {}
for metaFilePath in metaFilesPaths:
	isExcluded = False
	for excludeItem in excludeItems:
		if excludeItem in metaFilePath:
			isExcluded = True
			break
	if isExcluded:
		continue
	metaFileText = open(metaFilePath, 'rb').read().decode('utf-8')
	indexOfGuid = metaFileText.find(GUID_INDICATOR) + len(GUID_INDICATOR)
	indexOfNewLine = metaFileText.find('\n', indexOfGuid)
	if indexOfNewLine == -1:
		indexOfNewLine = len(metaFileText)
	guid = metaFileText[indexOfGuid : indexOfNewLine]
	fileGuidsDict[guid] = metaFilePath.replace('.meta', '')

# os.system('rm -r ' + UNREAL_PROJECT_PATH)
# os.system('cp -r "../BareUEProject" ' + UNREAL_PROJECT_PATH)
os.system('make build_UnityToUnreal')

def ConvertPythonFileToCpp (filePath):
	global membersDict
	global mainClassNames
	lines = []
	for line in open(filePath, 'rb').read().decode('utf-8').splitlines():
		if line.startswith('import ') or line.startswith('from '):
			print('Skipping line:', line)
			continue
		lines.append(line)
	text = '\n'.join(lines)
	open(filePath, 'wb').write(text.encode('utf-8'))
	outputFilePath = CODE_PATH + filePath[filePath.rfind('/') :]
	command = [ 'python3', os.getcwd() + '/py2many/py2many.py', '--cpp=1', outputFilePath, '--unreal=1', '--outdir=' + CODE_PATH ]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(UNITY_PROJECT_PATH)
	print(command)
	
	subprocess.check_call(command)

	outputFileText = open(outputFilePath.replace('.py', '.cpp'), 'rb').read().decode('utf-8')
	for mainClassName in mainClassNames:
		indexOfMainClassName = 0
		while indexOfMainClassName != -1:
			indexOfMainClassName = outputFileText.find(mainClassName, indexOfMainClassName + len(mainClassName))
			if indexOfMainClassName != -1 and outputFileText[indexOfMainClassName - 1 : indexOfMainClassName] != 'A' and not IsInString_CS(outputFileText, indexOfMainClassName):
				outputFileText = outputFileText[: indexOfMainClassName] + 'A' + outputFileText[indexOfMainClassName :]
		equalsNullIndicator = '= nullptr'
		indexOfEqualsNull = 0
		while indexOfEqualsNull != -1:
			indexOfEqualsNull = outputFileText.find(equalsNullIndicator, indexOfEqualsNull + len(equalsNullIndicator))
			if indexOfEqualsNull != -1:
				indexOfSpace = outputFileText.rfind(' ', 0, indexOfEqualsNull - 1)
				indexOfMainClassName = outputFileText.rfind(mainClassName, 0, indexOfSpace)
				if indexOfMainClassName == indexOfSpace - len(mainClassName):
					outputFileText = Remove(outputFileText, indexOfEqualsNull, len(equalsNullIndicator))
	pythonFileText = open(outputFilePath, 'rb').read().decode('utf-8')
	pythonFileLines = pythonFileText.split('\n')
	headerFileText = open(outputFilePath.replace('.py', '.h'), 'rb').read().decode('utf-8')
	for i in range(len(pythonFileLines) - 1, -1, -1):
		line = pythonFileLines[i]
		if not line.startswith(' '):
			line = line.replace(' ', '')
			indexOfColon = line.find(':')
			variableName = line[: indexOfColon]
			mainClassName = os.path.split(outputFilePath)[-1].split('.')[0]
			outputFileText = outputFileText.replace(variableName, variableName + '_' + mainClassName)
			headerFileText = headerFileText.replace(variableName, variableName + '_' + mainClassName)
			indexOfVariableName = headerFileText.find(variableName)
			indexOfNewLine = headerFileText.rfind('\n', 0, indexOfVariableName)
			headerFileText = headerFileText[: indexOfNewLine] + '\n\tUPROPERTY(EditAnywhere)' + headerFileText[indexOfNewLine :]
			indexOfEquals = line.find('=', indexOfColon + 1)
			if indexOfEquals != -1:
				variableName += '_' + mainClassName
				mainConstructor = '::A' + mainClassName + '() {'
				indexOfMainConstructor = outputFileText.find(mainConstructor)
				value = membersDict.get(variableName, None)
				if value == None:
					value = line[indexOfEquals + 1 :]
				outputFileText = outputFileText[: indexOfMainConstructor + len(mainConstructor) + 1] + '\t' + variableName + ' = ' + value + ';\n' + outputFileText[indexOfMainConstructor + len(mainConstructor) + 1 :]
		else:
			break
	outputFileLines = outputFileText.split('\n')
	for i in range(len(outputFileLines) - 2, -1, -1):
		line = outputFileLines[i]
		if line != '':
			for mainClassName in mainClassNames:
				if line.startswith('A' + mainClassName):
					# indexOfSpace = line.find(' ')
					# line = line[: indexOfSpace] + '*' + line[indexOfSpace :]
					line = line.replace('A' + mainClassName, 'APrefab*')
					outputFileLines[i] = line
					break
			mainClassName = os.path.split(outputFilePath)[-1].split('.')[0]
			for memberName in membersDict:
				indexOfMemberName = 0
				while indexOfMemberName != -1:
					indexOfMemberName = line.find(memberName, indexOfMemberName + 1)
					if indexOfMemberName != -1:
						memberValue = membersDict[memberName]
						line = line.replace(line[indexOfMemberName :], memberName + '_' + mainClassName + ' = ' + memberValue + ';')
						line = line.replace('_' + mainClassName + '_' + mainClassName, '_' + mainClassName)
						outputFileLines[i] = line
		else:
			break
	for i in range(len(outputFileLines)):
		line = outputFileLines[i]
		line = line.replace(' ', '')
		indexOfX = 0
		while indexOfX != -1:
			indexOfX = line.find('.X', indexOfX + 1)
			if indexOfX != -1:
				indexOfEquals = line.find('=', indexOfX)
				if indexOfEquals != -1 and indexOfEquals <= indexOfX + 3:
					outputFileLines[i] = line[: indexOfEquals + 1] + '-' + line[indexOfEquals + 1 :]
	outputFileText = '\n'.join(outputFileLines)
	indexOfUProperty = 0
	uPropertyIndicator = 'UPROPERTY('
	while indexOfUProperty != -1:
		indexOfUProperty = headerFileText.find(uPropertyIndicator, indexOfUProperty + len(uPropertyIndicator))
		indexOfNewLine = headerFileText.find('\n', indexOfUProperty)
		indexOfSpace = headerFileText.find(' ', indexOfNewLine + 1)
		variableType = headerFileText[indexOfNewLine + 1 : indexOfSpace]
		variableType = variableType.replace('\t', '')
		if variableType.startswith('A'):
			variableType = variableType[1 :]
			if variableType in mainClassNames:
				# headerFileText = headerFileText[: indexOfSpace] + '*' + headerFileText[indexOfSpace :]
				headerFileText = RemoveStartEnd(headerFileText, indexOfNewLine + 1, indexOfSpace)
				headerFileText = headerFileText[: indexOfNewLine + 1] + 'APrefab*' + headerFileText[indexOfNewLine + 1 :]
	open(outputFilePath.replace('.py', '.cpp'), 'wb').write(outputFileText.encode('utf-8'))
	open(outputFilePath.replace('.py', '.h'), 'wb').write(headerFileText.encode('utf-8'))
	command = [ 'cat', outputFilePath.replace('.py', '.cpp') ]
	print(command)

	subprocess.check_call(command)

def ConvertCSFileToCPP (filePath):
	assert os.path.isfile(filePath)
	command = [
		'dotnet',
		os.path.expanduser('~/Unity2Many/UnityToUnreal/Unity2Many.dll'),
		'includeFile=' + filePath,
		'unreal=true',
		'output=' + CODE_PATH,
	]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(UNITY_PROJECT_PATH)
	print(command)

	subprocess.check_call(command)

	outputFilePath = CODE_PATH + filePath[filePath.rfind('/') :]
	outputFilePath = outputFilePath.replace('.cs', '.py')
	print(outputFilePath)
	assert os.path.isfile(outputFilePath)

	os.system('cat ' + outputFilePath)

	ConvertPythonFileToCpp (outputFilePath)

def ImportAsset (assetPath : str):
	lastIndexOfPeriod = assetPath.rfind('.')
	projectFilePath = UNREAL_PROJECT_PATH + '/Content' + assetPath[assetPath.rfind('/') :]
	os.system('cp \'' + assetPath + '\' \'' + projectFilePath + '\'')

def MakeUProperty ():
	pass

codeFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.cs')
i = 0
while True:
	if i >= len(codeFilesPaths):
		break
	codeFilePath = codeFilesPaths[i]
	isExcluded = False
	for excludeItem in excludeItems:
		if excludeItem in codeFilePath:
			isExcluded = True
			codeFilesPaths.pop(i)
			i -= 1
	if not isExcluded:
		mainClassNames.append(os.path.split(codeFilePath)[-1].split('.')[0])
	i += 1
sceneFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.unity')
for sceneFilePath in sceneFilesPaths:
	sceneFileText = open(sceneFilePath, 'rb').read().decode('utf-8')
	sceneFileLines = sceneFileText.split('\n')
	scriptName = ''
	for line in sceneFileLines:
		if line.endswith(':'):
			currentType = line[: len(line) - 1]
		elif line.startswith('  '):
			if currentType == 'MonoBehaviour':
				if line.startswith(SCRIPT_INDICATOR):
					indexOfGuid = line.find(GUID_INDICATOR)
					scriptPath = fileGuidsDict.get(line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')], None)
					if scriptPath != None:
						scriptName = scriptPath[scriptPath.rfind('/') + 1 : scriptPath.rfind('.')]
				elif not line.startswith('  m_'):
					indexOfColon = line.find(': ')
					memberName = line[2 : indexOfColon] + '_' + scriptName
					value = line[indexOfColon + 2 :]
					# if value.startswith('{'):
					# 	indexOfGuid = value.find(GUID_INDICATOR)
					# 	indexOfComma = value.rfind(',')
					# 	guid = value[indexOfGuid + len(GUID_INDICATOR) : indexOfComma]
					# 	print('YAY' + guid)
					# 	filePath = fileGuidsDict[guid]
					# 	value = 'TSharedPtr<const APrefab>(&APrefab(' + filePath + ')).Get()'
					membersDict[memberName] = value
for codeFilePath in codeFilesPaths:
	ConvertCSFileToCPP (codeFilePath)

command = 'dotnet ' + os.getcwd() + '/../UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll BareUEProject Development Linux -Project="' + UNREAL_PROJECT_PATH + '/BareUEProject.uproject" -TargetType=Editor -Progress'
print(command)

os.system(command)

data = '\n'.join(sys.argv)
open('/tmp/Unity2Many Data (UnityToUnreal)', 'wb').write(data.encode('utf-8'))

command = UNREAL_COMMAND_PATH + ' ' + UNREAL_PROJECT_PATH + '/BareUEProject.uproject -nullrhi -ExecutePythonScript=' + MAKE_UNREAL_PROJECT_SCRIPT_PATH
print(command)

os.system(command)

command = UNREAL_COMMAND_PATH + ' ' + UNREAL_PROJECT_PATH + '/BareUEProject.uproject -buildlighting'
print(command)

os.system(command)

# command = '../UnrealEngine/Engine/Build/BatchFiles/RunUAT.sh BuildCookRun -project="' + UNREAL_PROJECT_PATH + '/BareUEProject.uproject" -noP4 -platform=Linux -clientconfig=Development -serverconfig=Development -cook -maps=AllMaps -compile -stage -pak -archive -archivedirectory="Output" -build'
# print(command)

# os.system(command)