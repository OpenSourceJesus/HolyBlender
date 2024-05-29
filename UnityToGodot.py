import os, subprocess, sys
from SystemExtensions import *
from StringExtensions import *

UNITY_PROJECT_PATH = os.path.expanduser('~/TestUnityProject')
GODOT_PROJECT_PATH = os.path.expanduser('~/Test Godot Project')
CODE_PATH = GODOT_PROJECT_PATH + '/Scripts'
EXCLUDE_ITEM_INDICATOR = 'exclude='
excludeItems = []

os.system('make build_UnityToGodot')

for arg in sys.argv:
	if arg.startswith(EXCLUDE_ITEM_INDICATOR):
		excludeItems.append(arg[len(EXCLUDE_ITEM_INDICATOR) :])

def ConvertGDFileToCS (filePath):
	assert os.path.isfile(filePath)
	mainClassName = filePath[filePath.rfind('/') + 1 : filePath.rfind('.')]
	command = [
		'dotnet', os.path.expanduser('~/Unity2Many') + '/UnityToGodot/Unity2Many.dll',
		'includeFile=' + filePath,
		'unreal=true',
		'output=' + CODE_PATH,
		'exclude=/Library'
	]
	for arg in sys.argv:
		command.append(arg)
	command.append(UNITY_PROJECT_PATH)
	print(command)

	subprocess.check_call(command)
	# lines = []
	# for line in open(filePath, 'rb').read().decode('utf-8').splitlines():
	# 	if line.startswith('using ') or line.startswith('from ') or line.startswith('namespace ') or '{' in line or '}' in line:
	# 		continue
	# 	line = line.replace('public ', '')
	# 	line = line.replace('this', 'self')
	# 	line = line.replace('new ', '')
	# 	line = line.replace('++', '+= 1')
	# 	line = line.replace('--', '-= 1')
	# 	line = line.replace(';', '')
	# 	if 'void ' in line:
	# 		line = line.replace('void ', 'func ')
	# 		indexOfLeftParenthesis = line.find('(')
	# 		if indexOfLeftParenthesis != -1:
	# 			indexOfRightParenthesis = line.find(')')
	# 			parameterList = line[indexOfLeftParenthesis + 1 : indexOfRightParenthesis]
	# 	lines.append(line)
	outputFile = CODE_PATH + '/' + mainClassName.replace('.cs', '.gd')
	# text = '\n'.join(lines)
	# open(outputFile, 'wb').write(text.encode('utf-8'))
	command = [ 'cat', outputFile ]
	print(command)

	subprocess.check_call(command)

codeFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.cs')
for codeFilePath in codeFilesPaths:
	isExcluded = False
	for excludeItem in excludeItems:
		if excludeItem in codeFilePath:
			isExcluded = True
			break
	if not isExcluded:
		ConvertGDFileToCS (codeFilePath)