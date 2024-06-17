import bpy, subprocess, os, mathutils

def Run (filePath : str, obj):
	outputCode = 'self = bpy.data.objects[\'' + obj.name + '\']\n'
	outputCode += open(filePath, 'rb').read().decode('utf-8')
	print(outputCode)

	exec(outputCode)