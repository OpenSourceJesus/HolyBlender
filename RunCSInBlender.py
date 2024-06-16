import bpy

MAPPINGS_DICT = {
	'transform.position' : 'self.location',
	'transform.eulerAngles' : 'self.rotation_euler'
}

def Run (code : str, obj):
	outputCode = 'self = bpy.data.objects[' + obj.name + ']'
	outputCode += code 
	for key in MAPPINGS_DICT:
		outputCode = outputCode.replace(key, MAPPINGS_DICT[key])
	exec(outputCode)