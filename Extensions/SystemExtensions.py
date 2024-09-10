import os

def GetAllFilePathsOfType (rootFolderPath : str, fileExtension : str) -> list[str]:
	output = []
	foldersRemaining = [ rootFolderPath ]
	while len(foldersRemaining) > 0:
		folderPath = os.path.expanduser(foldersRemaining[0])
		for path in os.listdir(folderPath):
			fullPath = folderPath + '/' + path
			if os.path.isdir(fullPath):
				foldersRemaining.append(fullPath)
			elif os.path.isfile(fullPath) and fullPath.endswith(fileExtension):
				output.append(fullPath)
		del foldersRemaining[0]
	return output

def MakeFolderForFile (path : str):
	_path = path[: path.find('/')]
	while _path != path:
		if _path != '' and not os.path.isdir(_path):
			os.mkdir(_path)
		indexOfSlash = path.find('/', len(_path) + 1)
		if indexOfSlash == -1:
			break
		_path = path[: indexOfSlash]

def CopyFile (fromPath : str, toPath : str):
	open(toPath, 'wb').write(open(fromPath, 'rb').read())