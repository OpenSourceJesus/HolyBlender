import bpy, subprocess, os, mathutils

MAPPINGS_DICT = {
	'transform.position' : 'self.location',
	'transform.eulerAngles' : 'self.rotation_euler'
}

def Run (filePath : str, obj):
	outputCode = 'self = bpy.data.objects[\'' + obj.name + '\']\n'
	outputCode += open(filePath, 'rb').read().decode('utf-8')
	for key in MAPPINGS_DICT:
		outputCode = outputCode.replace(key, MAPPINGS_DICT[key])
	print(outputCode)

	exec(outputCode)