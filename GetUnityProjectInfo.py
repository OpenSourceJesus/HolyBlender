import os, sys
from StringExtensions import *
from SystemExtensions import *

EXCLUDE_ITEM_INDICATOR = 'exclude='
GUID_INDICATOR = 'guid: '
UNITY_PROJECT_PATH = os.path.expanduser('~/TestUnityProject')
excludeItems = []

for arg in sys.argv:
	if arg.startswith(EXCLUDE_ITEM_INDICATOR):
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