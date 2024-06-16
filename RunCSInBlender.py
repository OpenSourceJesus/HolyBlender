import bpy, subprocess, os, mathutils

MAPPINGS_DICT = {
	'transform.position' : 'self.location',
	'transform.eulerAngles' : 'self.rotation_euler'
}

def Run (filePath : str, obj):
	fileText = open(filePath, 'rb').read().decode('utf-8')
	outputCode = 'self = bpy.data.objects[\'' + obj.name + '\']\n'

	command = [
		'dotnet',
		os.path.expanduser('~/Unity2Many/UnityInBlender/Unity2Many.dll'), 
		'includeFile=' + filePath,
		'output=/tmp/Unity2Many Data (UnityInBlender)'
	]
	print(command)

	subprocess.check_call(command)

	filePath = filePath.replace('.cs', '.py')
	if not filePath.endswith('.py'):
		filePath += '.py'
	outputCode += open(filePath, 'rb').read().decode('utf-8')
	for key in MAPPINGS_DICT:
		outputCode = outputCode.replace(key, MAPPINGS_DICT[key])
	print(outputCode)

	exec(outputCode)