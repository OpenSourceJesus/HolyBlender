#!/usr/bin/env python3
import bpy, subprocess, os, sys, hashlib, mathutils, math, base64, webbrowser

_thisdir = os.path.split(os.path.abspath(__file__))[0]
if _thisdir not in sys.path: sys.path.append(_thisdir)
from libholyblender import *

bpy.types.World.unrealExportPath = bpy.props.StringProperty(
	name = 'Unreal project path',
	description = '',
	default = '~/TestUnrealProject'
)

for i in range(MAX_SCRIPTS_PER_OBJECT):
	setattr(bpy.types.Object, 'unreal_script' + str(i), bpy.props.PointerProperty(name='Attach Unreal script', type=bpy.types.Text))

@bpy.utils.register_class
class WorldPanel (bpy.types.Panel):
	bl_idname = 'WORLD_PT_WorldUnreal_Panel'
	bl_label = 'HolyUnreal'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'
	def draw (self, context):
		self.layout.prop(context.world, 'unrealExportPath')
		self.layout.operator('unreal.export', icon='CONSOLE')

@bpy.utils.register_class
class UnrealTranslateButton (bpy.types.Operator):
	bl_idname = 'unreal.translate'
	bl_label = 'Translate To Unreal'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		global operatorContext
		global currentTextBlock
		BuildTool ('UnityToUnreal')
		operatorContext = context
		MakeFolderForFile ('/tmp/HolyBlender (Unreal Scripts)/')
		script = currentTextBlock.name
		if not currentTextBlock.name.endswith('.cs'):
			script += '.cs'
		filePath = '/tmp/HolyBlender (Unreal Scripts)/' + script
		open(filePath, 'wb').write(currentTextBlock.as_string().encode('utf-8'))
		ConvertCSFileToCPP (filePath)

@bpy.utils.register_class
class UnrealScriptsPanel (bpy.types.Panel):
	bl_idname = 'OBJECT_PT_Unreal_Scripts_Panel'
	bl_label = 'HolyBlender Unreal Scripts'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'

	def draw (self, context):
		self.layout.label(text='Attach Unreal scripts')
		foundUnassignedScript = False
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			hasScript = getattr(context.active_object, 'unreal_script' + str(i)) != None
			if hasScript or not foundUnassignedScript:
				self.layout.prop(context.active_object, 'unreal_script' + str(i))
			if not foundUnassignedScript:
				foundUnassignedScript = not hasScript

@bpy.utils.register_class
class UnrealExportButton (bpy.types.Operator):
	bl_idname = 'unreal.export'
	bl_label = 'Export To Unreal'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		global unrealCodePath
		global childrenDict
		global unrealCodePathSuffix
		BuildTool ('UnityToUnreal')
		unrealExportPath = os.path.expanduser(context.scene.world.unrealExportPath)
		importPath = os.path.expanduser(context.scene.world.unity_project_import_path)
		if importPath != '':
			command = [ 'python3', os.path.expanduser('~/HolyBlender/UnityToUnreal.py'), 'input=' + importPath, 'output=' + unrealExportPath, 'exclude=/Library' ]
			print(command)

			subprocess.check_call(command)

		else:
			unrealCodePath = unrealExportPath
			unrealProjectName = unrealExportPath[unrealExportPath.rfind('/') + 1 :]
			unrealCodePathSuffix = '/Source/' + unrealProjectName
			unrealCodePath += unrealCodePathSuffix
			MakeFolderForFile ('/tmp/HolyBlender (Unreal Scripts)/')
			data = unrealExportPath + '\n' + bpy.data.filepath + '\n'
			for collection in bpy.data.collections:
				for obj in collection.objects:
					if obj.instance_collection == None:
						data += self.GetObjectsData(collection.objects) + '\n'
			data += '\nScenes\n'
			for scene in bpy.data.scenes:
				data += self.GetObjectsData(scene.objects) + '\n'
			data += 'Children\n'
			data += self.GetObjectsData(childrenDict) + '\n'
			data += '\nScripts'
			attachedUnrealScriptsDict = get_user_scripts('unreal')
			for obj in attachedUnrealScriptsDict:
				if len(attachedUnrealScriptsDict[obj]) > 0:
					data += '\n' + self.GetBasicObjectData(obj) + '☣️' + '☣️'.join(attachedUnrealScriptsDict[obj]) + '\n'
					for property in obj.keys():
						data += property + '☣️' + str(type(obj[property])) + '☣️' + str(obj[property]) + '☣️'
					data = data[: len(data) - 2]
					for script in attachedUnrealScriptsDict[obj]:
						for textBlock in bpy.data.texts:
							if textBlock.name == script:
								if not script.endswith('.h') and not script.endswith('.cpp') and not script.endswith('.cs'):
									script += '.cs'
								open('/tmp/HolyBlender (Unreal Scripts)/' + script, 'wb').write(textBlock.as_string().encode('utf-8'))
								break
			open('/tmp/HolyBlender Data (BlenderToUnreal)', 'wb').write(data.encode('utf-8'))
			projectFilePath = unrealExportPath + '/' + unrealProjectName + '.uproject'
			if not os.path.isdir(unrealExportPath):
				MakeFolderForFile (unrealExportPath + '/')
				bareProjectPath = os.path.expanduser('~/HolyBlender/BareUEProject')
				filesAndFolders = os.listdir(bareProjectPath)
				for fileOrFolder in filesAndFolders:
					command = 'cp -r ''' + bareProjectPath + '/' + fileOrFolder + ' ' + unrealExportPath
					print(command)

					os.system(command)

				os.rename(unrealExportPath + '/Source/BareUEProject', unrealCodePath)
				os.rename(unrealExportPath + '/BareUEProject.uproject', projectFilePath)
				command = 'cp -r ' + TEMPLATES_PATH + '/Utils.h' + ' ' + unrealCodePath + '''/Utils.h
					cp -r ''' + TEMPLATES_PATH + '/Utils.cpp' + ' ' + unrealCodePath + '/Utils.cpp'
				print(command)

				os.system(command)
				projectFileText = open(projectFilePath, 'rb').read().decode('utf-8')
				projectFileText = projectFileText.replace('BareUEProject', unrealProjectName)
				open(projectFilePath, 'wb').write(projectFileText.encode('utf-8'))
				defaultActorFilePath = unrealCodePath + '/MyActor.h'
				defaultActorFileText = open(defaultActorFilePath, 'rb').read().decode('utf-8')
				defaultActorFileText = defaultActorFileText.replace('BAREUEPROJECT', unrealProjectName.upper())
				open(defaultActorFilePath, 'wb').write(defaultActorFileText.encode('utf-8'))
				utilsFilePath = unrealCodePath + '/Utils.h'
				utilsFileText = open(utilsFilePath, 'rb').read().decode('utf-8')
				utilsFileText = utilsFileText.replace('BAREUEPROJECT', unrealProjectName.upper())
				open(utilsFilePath, 'wb').write(utilsFileText.encode('utf-8'))
				codeFilesPaths = GetAllFilePathsOfType(unrealExportPath, '.cs')
				codeFilesPaths.append(unrealCodePath + '/BareUEProject.h')
				codeFilesPaths.append(unrealCodePath + '/BareUEProject.cpp')
				for codeFilePath in codeFilesPaths:
					codeFileText = open(codeFilePath, 'rb').read().decode('utf-8')
					codeFileText = codeFileText.replace('BareUEProject', unrealProjectName)
					open(codeFilePath, 'wb').write(codeFileText.encode('utf-8'))
					os.rename(codeFilePath, codeFilePath.replace('BareUEProject', unrealProjectName))
			command = 'dotnet ' + os.path.expanduser('~/UnrealEngine/Engine/Binaries/DotNET/UnrealBuildTool/UnrealBuildTool.dll ') + unrealProjectName + ' Development Linux -Project="' + projectFilePath + '" -TargetType=Editor -Progress'
			if os.path.expanduser('~') == '/home/gilead':
				command = command.replace('dotnet', '/home/gilead/Downloads/dotnet-sdk-6.0.302-linux-x64/dotnet')
				command = command.replace(os.path.expanduser('~/UnrealEngine'), os.path.expanduser('~/Downloads/Linux_Unreal_Engine_5.4.3'))
			print(command)

			os.system(command)

			open('/tmp/HolyBlender Data (UnityToUnreal)', 'wb').write(''.encode('utf-8'))
			unrealEditorPath = os.path.expanduser('~/UnrealEngine/Engine/Binaries/Linux/UnrealEditor-Cmd')
			if os.path.expanduser('~') == '/home/gilead':
				unrealEditorPath = '/home/gilead/Downloads/Linux_Unreal_Engine_5.4.3/Engine/Binaries/Linux/UnrealEditor-Cmd'
			command = unrealEditorPath + ' ' + projectFilePath + ' -nullrhi -ExecutePythonScript=' + os.path.expanduser('~/HolyBlender/MakeUnrealProject.py')
			print(command)

			os.system(command)

			command = unrealEditorPath + ' ' + projectFilePath + ' -buildlighting'
			print(command)

			os.system(command)

	def GetObjectsData (self, objectGroup):
		data = 'Cameras'
		for camera in bpy.data.cameras:
			if camera.name in objectGroup.keys():
				data += '\n' + GetCameraData(camera)
		data += '\nLights'
		for light in bpy.data.lights:
			if light.name in objectGroup.keys():
				data += '\n' + GetLightData(light)
		data += '\nMeshes'
		for obj in objectGroup:
			if obj.type == 'MESH':
				ExportObject (obj, '/tmp')
				data += '\n' + self.GetBasicObjectData(obj)
				if obj.rigid_body != None:
					data += '☣️' + str(obj.rigid_body.mass) + '☣️' + str(obj.rigid_body.linear_damping) + '☣️' + str(obj.rigid_body.angular_damping) + '☣️' + str(obj.rigid_body.enabled)
				for modifier in obj.modifiers:
					if modifier.type == 'COLLISION':
						data += '☣️True'
						break
		return data

	def GetBasicObjectData (self, obj):
		global childrenDict
		for _obj in bpy.data.objects:
			if _obj.name == obj.name:
				obj = _obj
				break
		previousObjectRotationMode = obj.rotation_mode
		obj.rotation_mode = 'QUATERNION'
		output = obj.name + '☣️' + str(obj.location * 100) + '☣️' + str(obj.rotation_quaternion) + '☣️' + str(obj.scale)
		if len(obj.children) > 0:
			for child in obj.children:
				childrenDict[child.name] = child
		obj.rotation_mode = previousObjectRotationMode
		return output

	def GetCameraData (self, camera):
		horizontalFov = False
		if camera.sensor_fit == 'HORIZONTAL':
			horizontalFov = True
		isOrthographic = False
		if camera.type == 'ORTHO':
			isOrthographic = True
		return self.GetBasicObjectData(camera) + '☣️' + str(horizontalFov) + '☣️' + str(camera.angle * (180.0 / PI)) + '☣️' + str(isOrthographic) + '☣️' + str(camera.ortho_scale) + '☣️' + str(camera.clip_start) + '☣️' + str(camera.clip_end)

	def GetLightData (self, light):
		lightType = 0
		if light.type == 'POINT':
			lightType = 1
		elif light.type == 'SPOT':
			lightType = 2
		elif lightObject.type == 'AREA':
			lightType = 3
		return self.GetBasicObjectData(light) + '☣️' + str(lightType) + '☣️' + str(light.energy * WATTS_TO_CANDELAS * 100) + '☣️' + str(light.color)


def ConvertCSFileToCPP (filePath):
	global mainClassNames
	global unrealCodePath
	global unrealCodePathSuffix
	assert os.path.isfile(filePath)
	unrealCodePath = os.path.expanduser(operatorContext.scene.world.unrealExportPath)
	unrealProjectName = unrealCodePath[unrealCodePath.rfind('/') + 1 :]
	unrealCodePathSuffix = '/Source/' + unrealProjectName
	unrealCodePath += unrealCodePathSuffix
	mainClassNames = [ os.path.split(filePath)[-1].split('.')[0] ]
	command = [
		'dotnet',
		os.path.expanduser('~/HolyBlender/UnityToUnreal/HolyBlender.dll'),
		'includeFile=' + filePath,
		'unreal=true',
		'output=' + unrealCodePath,
	]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(os.path.expanduser(operatorContext.scene.world.unity_project_import_path))
	print(command)

	subprocess.check_call(command)

	outputFilePath = unrealCodePath + filePath[filePath.rfind('/') :]
	outputFilePath = outputFilePath.replace('.cs', '.py')
	print(outputFilePath)
	assert os.path.isfile(outputFilePath)

	os.system('cat ' + outputFilePath)

	ConvertPythonFileToCPP (outputFilePath)

def ConvertPythonFileToCPP (filePath):
	global mainClassNames
	lines = []
	for line in open(filePath, 'rb').read().decode('utf-8').splitlines():
		if line.startswith('import ') or line.startswith('from '):
			print('Skipping line:', line)
			continue
		lines.append(line)
	text = '\n'.join(lines)
	open(filePath, 'wb').write(text.encode('utf-8'))
	hasCorrectTextBlock = False
	textBlockName = filePath[filePath.rfind('/') + 1 :]
	for textBlock in bpy.data.texts:
		if textBlock.name == textBlockName:
			hasCorrectTextBlock = True
			break
	if not hasCorrectTextBlock:
		bpy.data.texts.new(textBlockName)
	textBlock = bpy.data.texts[textBlockName]
	textBlock.clear()
	textBlock.write(text)
	outputFilePath = unrealCodePath + '/' + textBlockName
	command = [ 'python3', os.path.expanduser('~/HolyBlender') + '/py2many/py2many.py', '--cpp=1', outputFilePath, '--unreal=1', '--outdir=' + unrealCodePath ]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(os.path.expanduser(operatorContext.scene.world.unrealExportPath))
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
			variableName += '_' + mainClassName
			mainConstructor = '::A' + mainClassName + '() {'
			indexOfMainConstructor = outputFileText.find(mainConstructor)
			if indexOfEquals != -1:
				value = line[indexOfEquals + 1 :]
				outputFileText = outputFileText[: indexOfMainConstructor + len(mainConstructor) + 1] + '\t' + variableName + ' = ' + value + ';\n' + outputFileText[indexOfMainConstructor + len(mainConstructor) + 1 :]
		else:
			break
	outputFileLines = outputFileText.split('\n')
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
	cppFilePath = outputFilePath.replace('.py', '.cpp')
	open(cppFilePath, 'wb').write(outputFileText.encode('utf-8'))
	open(outputFilePath.replace('.py', '.h'), 'wb').write(headerFileText.encode('utf-8'))
	command = [ 'cat', cppFilePath ]
	print(command)

	subprocess.check_call(command)
	
	for textBlock in bpy.data.texts:
		textBlockName = cppFilePath[cppFilePath.rfind('/') + 1 :].replace('.cpp', '')
		if textBlock.name == textBlockName:
			textBlockName += '.cpp+.h'
			hasCorrectTextBlock = False
			for textBlock in bpy.data.texts:
				if textBlock.name == textBlockName:
					hasCorrectTextBlock = True
					break
			if not hasCorrectTextBlock:
				bpy.data.texts.new(textBlockName)
			textBlock = bpy.data.texts[textBlockName]
			textBlock.clear()
			textBlock.write(outputFileText)
			textBlock.write(headerFileText)
