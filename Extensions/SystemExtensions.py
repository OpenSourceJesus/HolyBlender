import os, sys

def GetAllFilePathsOfType (rootFolderPath : str, fileExtension : str) -> list[str]:
	output = []
	foldersRemaining = [ rootFolderPath ]
	while len(foldersRemaining) > 0:
		folderPath = os.path.expanduser(foldersRemaining[0])
		for path in os.listdir(folderPath):
			fullPath = os.path.join(folderPath, path)
			if os.path.isdir(fullPath):
				foldersRemaining.append(fullPath)
			elif os.path.isfile(fullPath) and fullPath.endswith(fileExtension):
				output.append(fullPath)
		del foldersRemaining[0]
	return output

def MakeFolderForFile (path : str):
	if sys.platform == 'win32':
		separator = '\\'
	else:
		separator = '/'
	_path = path[: path.find(separator)]
	while _path != path:
		if _path != '' and not os.path.isdir(_path):
			os.mkdir(_path)
		indexOfSeparator = path.find(separator, len(_path) + 1)
		if indexOfSeparator == -1:
			break
		_path = path[: indexOfSeparator]

def CopyFile (fromPath : str, toPath : str):
	open(toPath, 'wb').write(open(fromPath, 'rb').read())