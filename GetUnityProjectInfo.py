import os, sys
from StringExtensions import *
from SystemExtensions import *

INPUT_PATH_INDICATOR = 'input='
EXCLUDE_ITEM_INDICATOR = 'exclude='
GUID_INDICATOR = 'guid: '
UNITY_PROJECT_PATH = ''
excludeItems = []

for arg in sys.argv:
	if arg.startswith(INPUT_PATH_INDICATOR):
		UNITY_PROJECT_PATH = os.path.expanduser(arg[len(INPUT_PATH_INDICATOR) :])
	elif arg.startswith(EXCLUDE_ITEM_INDICATOR):
		excludeItems.append(arg[len(EXCLUDE_ITEM_INDICATOR) :])

if UNITY_PROJECT_PATH != '':
	metaFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.meta')
else:
	metaFilesPaths = []
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