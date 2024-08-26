import os, subprocess, bpy, sys, urllib.request, urllib.error, urllib.parse, atexit
from math import radians
from mathutils import *

'''
INSTALL NOTES:
	Fedora: 
		sudo dnf install blender rustup
		rustup-init
		~/.cargo/bin/rustup target add wasm32-unknown-unknown
'''

__thisdir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/local/lib/python3.12/dist-packages')
sys.path.append(os.path.expanduser('~/.local/lib/python3.12/site-packages'))
#sys.path.append(os.path.expanduser('~/HolyBlender'))
try:
	from PIL import Image
except:
	try:
		from wand.image import Image
	except:
		Image = None

from GetUnityProjectInfo import *
from SystemExtensions import *
from MakeBlenderPlugin import MAX_SCRIPTS_PER_OBJECT

UNITY_PROJECT_PATH = ''
BEVY_PROJECT_PATH = ''
TEMPLATES_PATH = os.path.join( __thisdir,'Templates')
TEMPLATE_APP_PATH = TEMPLATES_PATH + '/BevyBlenderApp.rs'
TEMPLATE_REGISTRY_PATH = TEMPLATES_PATH + '/registry.json'
ASSETS_PATH = BEVY_PROJECT_PATH + '/assets'
CODE_PATH = BEVY_PROJECT_PATH + '/src'
OUTPUT_FILE_PATH = BEVY_PROJECT_PATH + '/main.rs'
REGISTRY_PATH = ASSETS_PATH + '/registry.json'
INPUT_PATH_INDICATOR = 'input='
OUTPUT_PATH_INDICATOR = 'output='
WEBGL_INDICATOR = 'webgl'
YAML_ELEMENT_ID_INDICATOR = '--- !u!'
PARENT_INDICATOR = '  m_Father: {fileID: '
ACTIVE_INDICATOR = '  m_IsActive: '
MESH_INDICATOR = '  m_Mesh: '
SPRITE_INDICATOR = '  m_Sprite: '
SCRIPT_INDICATOR = '  m_Script: '
NAME_INDICATOR = '  m_Name: '
LIGHT_TYPE_INDICATOR = '  m_Type: '
LIGHT_INTENSITY_INDICATOR = '  m_Intensity: '
LOCAL_POSITION_INDICATOR = '  m_LocalPosition: {'
LOCAL_ROTATION_INDICATOR = '  m_LocalRotation: {'
LOCAL_SCALE_INDICATOR = '  m_LocalScale: {'
PIXELS_PER_UNIT_INDICATOR = '  spritePixelsToUnits: '
FOV_AXIS_INDICATOR = '  m_FOVAxisMode: '
FOV_INDICATOR = '  field of view: '
IS_ORTHOGRAPHIC_INDICATOR = '  orthographic: '
ORTHOGRAPHIC_SIZE_INDICATOR = '  orthographic size: '
NEAR_CLIP_PLANE_INDICATOR = '  near clip plane: '
FAR_CLIP_PLANE_INDICATOR = '  far clip plane: '
CLASS_MEMBER_INDICATOR = '#💠'
GAME_OBJECT_FIND_INDICATOR = 'GameObject.Find('
COMPONENT_TEMPLATE = '''    "HolyBlender::ꗈ": {
	  "additionalProperties": false,
	  "isComponent": true,
	  "isResource": false,
	  "properties": {},
	  "required": [],
	  "short_name": "ꗈ",
	  "title": "HolyBlender::ꗈ",
	  "type": "object",
	  "typeInfo": "Struct"
	}'''
CUSTOM_TYPE_TEMPLATE = '''#[derive(Component, Reflect, Default, Debug)]
#[reflect(Component)]
struct ꗈ;'''
REMOVE_COMPONENT_TEMPLATE = '''fn RemoveComponent (mut commands: Commands, query: Query<Entity, With<ꗈ>>, EventReader<RemoveComponentEvent>)
{
	for entity in query
	{
		if entity.name == entityName:
		{
			commands.entity(entity).remove::<ꗈ>();
			return;
		}
	}
}'''
SYSTEM_ARGUMENTS = '''mut commands: Commands,
assetServer: Res<AssetServer>,
mut meshes : ResMut<Assets<Mesh>>,
keys: Res<ButtonInput<KeyCode>>,
mouseButtons: Res<ButtonInput<MouseButton>>,
mut query: Query<&mut Transform, With<ꗈ>>,
time: Res<Time>,
mut cursorEvent: EventReader<CursorMoved>,
mut screenToWorldPointEvent: EventWriter<ScreenToWorldPointEvent>'''
SYSTEM_TEMPLATE = 'pub fn ꗈ0(' + SYSTEM_ARGUMENTS + ''')
{
	unsafe
	{
		for mut trs in &mut query
		{
			let right = trs.right();
			let up = trs.up();
			let forward = trs.forward();
			ꗈ1
		}
	}
}'''
PI = 3.141592653589793
outputFileText = ''
importStatementsText = ''
outputFileTextReplaceClauses = [ '', '', '', '' ]
addToOutputFileText = ''
mainClassName = ''
membersDict = {}
assetsPathsDict = {}

def ConvertCSFileToRust (filePath):
	global CODE_PATH
	global mainClassName
	mainClassName = filePath[filePath.rfind('/') + 1 : filePath.rfind('.')]
	assert os.path.isfile(filePath)
	command = [
		'dotnet',
		os.path.expanduser('~/HolyBlender/UnityToBevy/HolyBlender.dll'), 
		'includeFile=' + filePath,
		'bevy=true',
		'output=/tmp'
	]
	# for arg in sys.argv:
	# 	command.append(arg)
	print(command)

	subprocess.check_call(command)

	outputFilePath = CODE_PATH + '/main.py'
	print(outputFilePath)
	assert os.path.isfile(outputFilePath)

	os.system('cat ' + outputFilePath)

	ConvertPythonFileToRust (outputFilePath)

def ConvertPythonFileToRust (filePath):
	global UNITY_PROJECT_PATH
	global OUTPUT_FILE_PATH
	global mainClassName
	lines = []
	for line in open(filePath, 'rb').read().decode('utf-8').splitlines():
		if line.startswith('import ') or line.startswith('from '):
			print('Skipping line:', line)
			continue
		lines.append(line)
	data = '\n'.join(lines)
	open(filePath, 'wb').write(data.encode('utf-8'))
	command = [ 'python3', 'py2many/py2many.py', '--rust=1', '--force', filePath, '--outdir=' + CODE_PATH ]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(UNITY_PROJECT_PATH)
	print(command)
	
	subprocess.check_call(command)

	assert os.path.isfile(OUTPUT_FILE_PATH)
	print(OUTPUT_FILE_PATH)

	os.system('cat ' + OUTPUT_FILE_PATH)

def MakeCamera (localPosition : list, localRotation : list, localSize : list, objectName : str, horizontalFov : bool, fov : float, isOrthographic : bool, orthographicSize : float, nearClipPlane : float, farClipPlane : float):
	global outputFileTextReplaceClauses
	cameraData = bpy.data.cameras.new('Camera')
	cameraObject = bpy.data.objects.new('Camera', cameraData)
	bpy.context.scene.collection.objects.link(cameraObject)
	bpy.context.view_layer.objects.active = cameraObject
	cameraObject.location = Vector((localPosition[0], localPosition[1], -localPosition[2]))
	cameraObject.rotation_mode = 'QUATERNION'
	localRotation = Quaternion((localRotation[0], localRotation[1], -localRotation[2], localRotation[3])).to_euler()
	localRotation.z += PI
	localRotation = localRotation.to_quaternion()
	cameraObject.rotation_quaternion = localRotation
	if isOrthographic:
		cameraData.type = 'ORTHO'
		cameraData.ortho_scale = orthographicSize * 4
		if not horizontalFov:
			cameraData.ortho_scale *= bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y

def MakeMesh (localPosition : list, localRotation : list, localSize : list, objectName : str, meshAssetPath : str):
	oldObjects = set(bpy.context.scene.objects)
	bpy.ops.import_scene.fbx(filepath=meshAssetPath)
	importedObjects = set(bpy.context.scene.objects) - oldObjects
	for importedObject in importedObjects:
		importedObject.location += Vector((localPosition[0], localPosition[1], -localPosition[2]))
		localRotation = Quaternion((localRotation[0], localRotation[1], -localRotation[2], localRotation[3])).to_euler()
		localRotation.z += PI
		localRotation = localRotation.to_quaternion()
		importedObject.rotation_mode = 'QUATERNION'
		importedObject.rotation_quaternion += localRotation
		importedObject.scale = (localSize[0], localSize[1], -localSize[2])

def MakeLight (localPosition : list, localRotation : list, localSize : list, objectName : str, lightType : int, lightIntensity : float):
	if lightType == 0:
		lightType = 'SPOT'
	elif lightType == 1:
		lightType = 'SUN'
	elif lightType == 2:
		lightType = 'POINT'
	else:
		lightType = 'AREA'
	lightData = bpy.data.lights.new(name='Light data', type=lightType)
	lightObject = bpy.data.objects.new(objectName, lightData)
	bpy.context.collection.objects.link(lightObject)
	bpy.context.view_layer.objects.active = lightObject
	lightObject.location = Vector((localPosition[0], localPosition[1], -localPosition[2]))
	localRotation = Quaternion((localRotation[0], localRotation[1], -localRotation[2], localRotation[3])).to_euler()
	localRotation.z += PI
	localRotation = localRotation.to_quaternion()
	lightObject.rotation_mode = 'QUATERNION'
	lightObject.rotation_quaternion = localRotation
	lightObject.scale = (localSize[0], localSize[1], -localSize[2])

def MakeSprite (localPosition : list, localRotation : list, localSize : list, objectName : str, textureAssetPath : str):
	oldObjects = set(bpy.context.scene.objects)
	bpy.ops.import_image.to_plane(files=[{ 'name': textureAssetPath }])
	importedObjects = set(bpy.context.scene.objects) - oldObjects
	pixelsPerUnit = -1
	fileLines = open(textureAssetPath + '.meta', 'rb').read().decode('utf-8').splitlines()
	for line in fileLines:
		if line.startswith(PIXELS_PER_UNIT_INDICATOR):
			pixelsPerUnit = float(line[len(PIXELS_PER_UNIT_INDICATOR) :])
			break
	for importedObject in importedObjects:
		importedObject.location += Vector((localPosition[0], localPosition[1], -localPosition[2]))
		localRotation = Quaternion((localRotation[0], localRotation[1], -localRotation[2], localRotation[3])).to_euler()
		localRotation.z += PI
		localRotation = localRotation.to_quaternion()
		importedObject.rotation_mode = 'QUATERNION'
		importedObject.rotation_quaternion += localRotation
		try:
			image = Image.open(textureAssetPath)
		except:
			image = Image(filename=textureAssetPath)
		multiplySize = max(image.width, image.height) / pixelsPerUnit
		importedObject.scale = Vector((localSize[0], localSize[1], -localSize[2])) * multiplySize
		importedObject.name = objectName
	return importedObject

def MakeScript (localPosition : list, localRotation : list, localSize : list, objectName : str, scriptPath : str):
	global membersDict
	global mainClassName
	global outputFileText
	global addToOutputFileText
	global importStatementsText
	global outputFileTextReplaceClauses
	# ConvertCSFileToRust (scriptPath)
	# MakeComponent (objectName, 'HolyBlender::' + mainClassName)
	# outputFileText = open(OUTPUT_FILE_PATH, 'rb').read().decode('utf-8')
	scriptText = open(scriptPath, 'rb').read().decode('utf-8')
	# if 'fn Update' in outputFileText:
	# 	# importStatementsText += 'use ' + mainClassName + '::*;\n'
	# 	outputFileTextReplaceClauses[1] += '\n\t\t.add_systems(Update, Update' + mainClassName + ')'
	# # outputFileText = 'pub mod ' + mainClassName + '\n{\n' + outputFileText + '\n}'
	# startMethodIndicator = 'fn Start'
	# indexOfStartMethod = outputFileText.find(startMethodIndicator)
	# if indexOfStartMethod != -1:
	# 	outputFileTextReplaceClauses[1] += '\n\t\t.add_systems(OnEnter(MyStates::Next), Start' + mainClassName + ')'
	# 	outputFileText = outputFileText[: indexOfStartMethod + len(startMethodIndicator)] + mainClassName + outputFileText[indexOfStartMethod + len(startMethodIndicator) :]
	# outputFileText = outputFileText.replace('Time.deltaTime', 'time.delta_seconds()')
	# outputFileText = outputFileText.replace('Vector2', 'Vec2')
	# outputFileText = outputFileText.replace('Vec2.zero', 'Vec2::ZERO')
	# outputFileText = outputFileText.replace('Vector3', 'Vec3')
	# outputFileText = outputFileText.replace('Vec3.zero', 'Vec3::ZERO')
	# outputFileText = outputFileText.replace('Vec3.forward', '-Vec3::Y')
	# outputFileText = outputFileText.replace('Vec3.up', '-Vec3::Z')
	# SetVariableTypeAndRemovePrimitiveCastsFromOutputFile ('Vec2')
	# SetVariableTypeAndRemovePrimitiveCastsFromOutputFile ('Vec3')
	# outputFileText = outputFileText.replace('.Normalize', '.normalize')
	# outputFileText = outputFileText.replace(', screenToWorldPointEvent', ', &mut screenToWorldPointEvent')
	# outputFileText = outputFileText.replace('pub const ', 'let mut ')
	# outputFileText = outputFileText.replace('pub static ', 'let mut ')
	# outputFileText = outputFileText.replace('transform.position', 'trs.translation')
	# outputFileText = outputFileText.replace('transform.rotation', 'trs.rotation')
	# outputFileText = outputFileText.replace('self, ', '')
	# outputFileText = outputFileText.replace('&self', '')
	# outputFileText = outputFileText.replace('self.', '')
	# outputFileText = outputFileText.replace('self', '')
	# indexOfTrsUp = 0
	# while indexOfTrsUp != -1:
	# 	trsUpIndicator = 'transform.up'
	# 	indexOfTrsUp = outputFileText.find(trsUpIndicator, indexOfTrsUp + 1)
	# 	if indexOfTrsUp != -1:
	# 		indexOfEquals = outputFileText.find('=', indexOfTrsUp)
	# 		setValue = False
	# 		if indexOfEquals != -1:
	# 			betweenTrsUpAndEquals = outputFileText[indexOfTrsUp + len(trsUpIndicator) : indexOfEquals]
	# 			if betweenTrsUpAndEquals.isspace() or betweenTrsUpAndEquals == '':
	# 				setValue = True
	# 				indexOfSemicolon = outputFileText.find(';', indexOfEquals)
	# 				value = outputFileText[indexOfEquals + 1 : indexOfSemicolon]
	# 				outputFileText = outputFileText.replace(trsUpIndicator + betweenTrsUpAndEquals + '=' + value, 'trs.look_to(' + value + '.mul(-1.0), Vec3::from(up))')
	# 		if not setValue:
	# 			outputFileText = Remove(outputFileText, indexOfTrsUp, len(trsUpIndicator))
	# 			outputFileText = outputFileText[: indexOfTrsUp] + 'Vec3::from(forward).mul(-1.0)' + outputFileText[indexOfTrsUp :]
	# indexOfTrsForward = 0
	# while indexOfTrsForward != -1:
	# 	trsForwardIndicator = 'transform.forward'
	# 	indexOfTrsForward = outputFileText.find(trsForwardIndicator, indexOfTrsForward + 1)
	# 	if indexOfTrsForward != -1:
	# 		indexOfEquals = outputFileText.find('=', indexOfTrsForward)
	# 		setValue = False
	# 		if indexOfEquals != -1:
	# 			betweenTrsForwardAndEquals = outputFileText[indexOfTrsForward + len(trsForwardIndicator) : indexOfEquals]
	# 			if betweenTrsForwardAndEquals.isspace() or betweenTrsForwardAndEquals == '':
	# 				setValue = True
	# 				indexOfSemicolon = outputFileText.find(';', indexOfEquals)
	# 				value = outputFileText[indexOfEquals + 1 : indexOfSemicolon]
	# 				outputFileText = outputFileText.replace(trsForwardIndicator + betweenTrsForwardAndEquals + '=' + value, 'trs.look_to(Vec3::from(forward), ' + value + '.mul(-1.0))')
	# 		if not setValue:
	# 			outputFileText = Remove(outputFileText, indexOfTrsForward, len(trsForwardIndicator))
	# 			outputFileText = outputFileText[: indexOfTrsUp] + 'Vec3::from(up).mul(-1.0)' + outputFileText[indexOfTrsUp :]
	# indexOfAtan2 = 0
	# while indexOfAtan2 != -1:
	# 	atan2Indicator = 'Mathf.Atan2('
	# 	indexOfAtan2 = outputFileText.find(atan2Indicator, indexOfAtan2 + len(atan2Indicator))
	# 	if indexOfAtan2 != -1:
	# 		indexOfComma = outputFileText.find(',', indexOfAtan2)
	# 		yClause = outputFileText[indexOfAtan2 + len(atan2Indicator) : indexOfComma]
	# 		indexOfRightParenthesis = IndexOfMatchingRightParenthesis(outputFileText, indexOfAtan2 + len(atan2Indicator))
	# 		xClause = outputFileText[indexOfComma + 1 : indexOfRightParenthesis]
	# 		outputFileText = outputFileText.replace(outputFileText[indexOfAtan2 : indexOfRightParenthesis + 1], yClause + '.atan2(' + xClause + ')')
	# outputFileText = outputFileText.replace('(, ', '(')
	# indexOfY = 0
	# while indexOfY != -1:
	# 	indexOfY = outputFileText.find('.y', indexOfY + 2)
	# 	if indexOfY != -1:
	# 		indexOfToken = IndexOfAny(outputFileText, ['=', ' ', '+', '-', '*', '/', ')', ']'], indexOfY + 2)
	# 		if indexOfToken == indexOfY + 2:
	# 			indexOfEquals = outputFileText.find('=', indexOfToken + 3)
	# 			if indexOfEquals == indexOfToken + 1:
	# 				indexOfToken += 1
	# 			outputFileText = outputFileText[: indexOfToken + 3] + '-' + outputFileText[indexOfToken + 3 :]
	# 		outputFileText = Remove(outputFileText, indexOfY + 1, 1)
	# 		outputFileText = outputFileText[: indexOfY + 1] + 'z' + outputFileText[indexOfY + 1 :]
	# indexOfTrsEulerAngles = 0
	# while indexOfTrsEulerAngles != -1:
	# 	trsEulerAnglesIndicator = 'transform.eulerAngles'
	# 	indexOfTrsEulerAngles = outputFileText.find(trsEulerAnglesIndicator, indexOfTrsEulerAngles + len(trsEulerAnglesIndicator))
	# 	if indexOfTrsEulerAngles != -1:
	# 		indexOfEquals = outputFileText.find('=', indexOfTrsEulerAngles + len(trsEulerAnglesIndicator))
	# 		textBetweenTrsEulerAnglesAndEquals = outputFileText[indexOfTrsEulerAngles + len(trsEulerAnglesIndicator) : indexOfEquals]
	# 		if textBetweenTrsEulerAnglesAndEquals == '' or textBetweenTrsEulerAnglesAndEquals.isspace():
	# 			indexOfSemicolon = outputFileText.find(';', indexOfEquals)
	# 			valueAfterEquals = outputFileText[indexOfEquals + 1 : indexOfSemicolon]
	# 			outputFileText = outputFileText.replace(trsEulerAnglesIndicator + textBetweenTrsEulerAnglesAndEquals + '=' + valueAfterEquals, 'let _rotation = ' + valueAfterEquals + ' * ' + str(PI) + ' / 180.0;\ntrs.rotation = Quat::from_euler(EulerRot::ZYX, _rotation.x, _rotation.y, _rotation.z)')
	# 		elif textBetweenTrsEulerAnglesAndEquals.strip() == '+':
	# 			indexOfSemicolon = outputFileText.find(';', indexOfEquals)
	# 			valueAfterEquals = outputFileText[indexOfEquals + 1 : indexOfSemicolon]
	# 			outputFileText = outputFileText.replace(trsEulerAnglesIndicator + textBetweenTrsEulerAnglesAndEquals + '=' + valueAfterEquals, 'let _rotation = ' + valueAfterEquals + ' * ' + str(PI) + ' / 180.0;\ntrs.rotate(Quat::from_euler(EulerRot::ZYX, _rotation.x, _rotation.y, _rotation.z))')
	# 		elif textBetweenTrsEulerAnglesAndEquals.strip() == '-':
	# 			indexOfSemicolon = outputFileText.find(';', indexOfEquals)
	# 			valueAfterEquals = outputFileText[indexOfEquals + 1 : indexOfSemicolon]
	# 			outputFileText = outputFileText.replace(trsEulerAnglesIndicator + textBetweenTrsEulerAnglesAndEquals + '=' + valueAfterEquals, 'let _rotation = ' + valueAfterEquals + ' * ' + str(PI) + ' / 180.0;\ntrs.rotate(Quat::from_euler(EulerRot::ZYX, -_rotation.x, -_rotation.y, -_rotation.z))')
	# 		else:
	# 			outputFileText = Remove(outputFileText, indexOfTrsEulerAngles, len(trsEulerAnglesIndicator))
	# 			outputFileText = outputFileText[: indexOfTrsEulerAngles] + 'Vec3::from(trs.rotation.to_euler(EulerRot::ZYX))' + outputFileText[indexOfTrsEulerAngles :]
	# outputFileText = outputFileText.replace(mainClassName + '::', '')
	# outputFileText = outputFileText.replace('&' + mainClassName + ' {}', '')
	# indexOfMacro = 0
	# while indexOfMacro != -1:
	# 	indexOfMacro = outputFileText.find('#![')
	# 	if indexOfMacro != -1:
	# 		indexOfNewLine = outputFileText.find('\n', indexOfMacro)
	# 		outputFileText = RemoveStartEnd(outputFileText, indexOfMacro, indexOfNewLine)
	# indexOfDefaultComment = 0
	# while indexOfDefaultComment != -1:
	# 	indexOfDefaultComment = outputFileText.find('//! ')
	# 	if indexOfDefaultComment != -1:
	# 		indexOfNewLine = outputFileText.find('\n', indexOfDefaultComment)
	# 		outputFileText = RemoveStartEnd(outputFileText, indexOfDefaultComment, indexOfNewLine)
	# mainClassIndicator = 'impl ' + mainClassName + ' {'
	# indexOfMainClass = outputFileText.find(mainClassIndicator)
	# if indexOfMainClass != -1:
	# 	indexOfMainClassEnd = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfMainClass + len(mainClassIndicator))
	# 	outputFileText = Remove(outputFileText, indexOfMainClassEnd, 1)
	# 	outputFileText = Remove(outputFileText, indexOfMainClass, len(mainClassIndicator))
	# mainClassIndicator = 'pub struct ' + mainClassName + ' {'
	# indexOfMainClass = outputFileText.find(mainClassIndicator)
	# if indexOfMainClass != -1:
	# 	indexOfMainClassEnd = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfMainClass + len(mainClassIndicator))
	# 	mainClassContents = outputFileText[indexOfMainClass + len(mainClassIndicator) : indexOfMainClassEnd]
	# 	outputFileText = Remove(outputFileText, indexOfMainClassEnd, 1)
	# 	outputFileText = Remove(outputFileText, indexOfMainClass, len(mainClassIndicator))
	# 	newMainClassContents = mainClassContents.replace('pub ', 'static mut ')
	# 	newMainClassContents = newMainClassContents.replace(',', ';')
	# 	pythonFileText = open(OUTPUT_FILE_PATH.replace('.rs', '.py'), 'rb').read().decode('utf-8')
	# 	pythonFileLines = pythonFileText.split('\n')
	# 	pythonFileLines.pop(0)
	# 	for line in pythonFileLines:
	# 		if line.startswith(CLASS_MEMBER_INDICATOR):
	# 			indexOfColon = line.find(':')
	# 			memberName = line[len(CLASS_MEMBER_INDICATOR) : indexOfColon]
	# 			memberValue = membersDict.get(memberName + '_' + mainClassName, None)
	# 			if memberValue == None:
	# 				memberValue = line[indexOfColon + 1 :]
	# 			if IsNumber(memberValue) and '.' not in memberValue:
	# 				memberValue += '.0'
	# 				membersDict[memberName + '_' + mainClassName] = memberValue
	# 			indexOfMemberName = 0
	# 			while indexOfMemberName != -1:
	# 				indexOfMemberName = newMainClassContents.find(memberName, indexOfMemberName + 1)
	# 				if indexOfMemberName != -1:
	# 					indexOfSemicolon = newMainClassContents.find(';', indexOfMemberName)
	# 					newMainClassContents = newMainClassContents[: indexOfSemicolon] + ' = ' + memberValue + newMainClassContents[indexOfSemicolon :]
	# 		else:
	# 			break
	# 	outputFileText = outputFileText.replace(mainClassContents, newMainClassContents)
	# mainMethodIndicator = 'pub fn main() {'
	# indexOfMainMethod = outputFileText.find(mainMethodIndicator)
	# if indexOfMainMethod != -1:
	# 	indexOfMainMethodEnd = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfMainClass + len(mainClassIndicator))
	# 	outputFileText = RemoveStartEnd(outputFileText, indexOfMainMethod, indexOfMainMethodEnd)
	# publicMethodIndicator = 'pub fn '
	# indexOfPublicMethodIndicator = 0
	# while indexOfPublicMethodIndicator != -1:
	# 	indexOfPublicMethodIndicator = outputFileText.find(publicMethodIndicator, indexOfPublicMethodIndicator + len(publicMethodIndicator))
	# 	if indexOfPublicMethodIndicator != -1:
	# 		indexOfLeftParenthesis = outputFileText.find('(', indexOfPublicMethodIndicator)
	# 		outputFileText = outputFileText[: indexOfLeftParenthesis + 1] + SYSTEM_ARGUMENTS.replace('ꗈ', mainClassName) + outputFileText[indexOfLeftParenthesis + 1 :]
	# 		indexOfLeftCurlyBrace = outputFileText.find('{', indexOfLeftParenthesis + 1 + len(SYSTEM_ARGUMENTS))
	# 		indexOfRightCurlyBrace = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfLeftCurlyBrace)
	# 		query = '\nunsafe\n{\nfor mut trs in &mut query\n{\nlet right = trs.right();\nlet up = trs.up();\nlet forward = trs.forward();\n'
	# 		outputFileText = outputFileText[: indexOfLeftCurlyBrace + 1] + query + outputFileText[indexOfLeftCurlyBrace + 1 :]
	# 		outputFileText = outputFileText[: indexOfRightCurlyBrace + len(query)] + '}\n}\n' + outputFileText[indexOfRightCurlyBrace + len(query) :]
	# indexOfStaticVariableIndicator = 0
	# while indexOfStaticVariableIndicator != -1:
	# 	staticVariableIndicator = 'static mut '
	# 	indexOfStaticVariableIndicator = outputFileText.find(staticVariableIndicator, indexOfStaticVariableIndicator + 1)
	# 	if indexOfStaticVariableIndicator != -1:
	# 		indexOfColon = outputFileText.find(':', indexOfStaticVariableIndicator + len(staticVariableIndicator))
	# 		variableName = outputFileText[indexOfStaticVariableIndicator + len(staticVariableIndicator) : indexOfColon]
	# 		newValue = membersDict.get(variableName, None)
	# 		if newValue != None:
	# 			if newValue.startswith('"'):
	# 				indexOfVariableType = indexOfColon + 2
	# 				indexOfEndOfVariableType = outputFileText.find(' ', indexOfColon + 1)
	# 				variableType = outputFileText[indexOfVariableType : indexOfEndOfVariableType]
	# 				outputFileText = Remove(outputFileText, indexOfVariableType, len(variableType))
	# 				outputFileText = outputFileText[: indexOfVariableType] + '&str' + outputFileText[indexOfVariableType :]
	# 			indexOfEquals = outputFileText.find('=', indexOfColon)
	# 			indexOfSemicolon = outputFileText.find(';', indexOfEquals)
	# 			value = outputFileText[indexOfEquals + 1 : indexOfSemicolon]
	# 			outputFileText = Remove(outputFileText, indexOfEquals + 1, len(value))
	# 			outputFileText = outputFileText[: indexOfEquals + 1] + newValue + outputFileText[indexOfEquals + 1 :]
	# 		else:
	# 			indexOfEquals = outputFileText.find('=', indexOfColon)
	# 			indexOfSemicolon = outputFileText.find(';', indexOfEquals)
	# 			value = outputFileText[indexOfEquals + 2 : indexOfSemicolon]
	# 			if value.startswith('"'):
	# 				indexOfVariableType = indexOfColon + 2
	# 				indexOfEndOfVariableType = outputFileText.find(' ', indexOfVariableType)
	# 				variableType = outputFileText[indexOfVariableType : indexOfEndOfVariableType]
	# 				outputFileText = Remove(outputFileText, indexOfVariableType, len(variableType))
	# 				outputFileText = outputFileText[: indexOfVariableType] + '&str' + outputFileText[indexOfVariableType :]
	# 		outputFileText = outputFileText.replace(variableName, variableName + '_' + mainClassName)
	# indexOfInstantiate = 0
	# while indexOfInstantiate != -1:
	# 	instantiateIndicator = 'Instantiate('
	# 	indexOfInstantiate = outputFileText.find(instantiateIndicator)
	# 	if indexOfInstantiate != -1:
	# 		indexOfSemicolon = outputFileText.find(';', indexOfInstantiate)
	# 		instantiateCommand = outputFileText[indexOfInstantiate : indexOfSemicolon]
	# 		indexOfEndOfWhatToInstantiate = outputFileText.find(',', indexOfInstantiate)
	# 		position = ''
	# 		rotation = ''
	# 		if indexOfEndOfWhatToInstantiate > indexOfSemicolon:
	# 			indexOfEndOfWhatToInstantiate = indexOfSemicolon
	# 		elif indexOfEndOfWhatToInstantiate != -1:
	# 			indexOfPosition = outputFileText.find(',', indexOfEndOfWhatToInstantiate) + 1
	# 			indexOfRotation = outputFileText.find(',', indexOfPosition) + 1
	# 			position = outputFileText[indexOfPosition : indexOfRotation - 1]
	# 			rotation = outputFileText[indexOfRotation : indexOfSemicolon]
	# 			rotation = Remove(rotation, len(rotation) - 1, 1)
	# 		whatToInstantiate = outputFileText[indexOfInstantiate + len(instantiateIndicator) : indexOfEndOfWhatToInstantiate]
	# 		assetName = assetsPathsDict[whatToInstantiate]
	# 		assetName = assetName[assetName.rfind('/') + 1 :]
	# 		assetName = assetName.replace('.prefab', '_Prefab')
	# 		assetPath = assetName + '.glb#Scene0'
	# 		if position == '':
	# 			position = 'Vec3::ZERO'
	# 			rotation = 'Quat::IDENTITY'
	# 		indexOfEquals = outputFileText.rfind('=', indexOfInstantiate)
	# 		newInstantiateCommand = 'SpawnEntity(&mut commands, &assetServer, &"' + assetPath + '", ' + position + ', ' + rotation + ')'
	# 		if indexOfEquals != -1:
	# 			betweenEqualsAndInstantiate = outputFileText[indexOfEquals : indexOfInstantiate]
	# 			if not betweenEqualsAndInstantiate.isspace() and betweenEqualsAndInstantiate != '':
	# 				newInstantiateCommand = 'let entity_' + assetName + ' = ' + newInstantiateCommand
	# 		outputFileText = outputFileText.replace(instantiateCommand, newInstantiateCommand)
	# indexOfGameObjectFind = 0
	# while indexOfGameObjectFind != -1:
	# 	indexOfGameObjectFind = outputFileText.find(GAME_OBJECT_FIND_INDICATOR)
	# 	if indexOfGameObjectFind != -1:
	# 		indexOfRightParenthesis = IndexOfMatchingRightParenthesis(outputFileText, indexOfGameObjectFind + len(GAME_OBJECT_FIND_INDICATOR))
	# 		gameObjectFind = outputFileText.SubstringStartEnd(indexOfGameObjectFind, indexOfRightParenthesis)
	# 		print('YAY' + gameObjectFind)
	# 		whatToFind = gameObjectFind.SubstringStartEnd(len(GAME_OBJECT_FIND_INDICATOR), len(gameObjectFind) - 2)
	# 		entitytFind = '\nunsafe\n{\nfor mut enitty in &mut nameQuery\n{if enitty == ' + whatToFind + '\n{'
	# 		outputLine = outputLine.replace(gameObjectFind, entitytFind)
	# indexOfUpdateMethod = outputFileText.find('fn Update')
	# if indexOfUpdateMethod != -1:
	# 	outputFileText = outputFileText.replace('fn Update', 'fn Update' + mainClassName)
	addToOutputFileText += CUSTOM_TYPE_TEMPLATE.replace('ꗈ', mainClassName)
	if mainClassName not in bpy.data.texts:
		if mainClassName+'.py' in bpy.data.texts: mainClassName += '.py'
		elif mainClassName+'.rs' in bpy.data.texts: mainClassName += '.rs'
		elif mainClassName+'.cs' in bpy.data.texts: mainClassName += '.cs'
	textBlock = bpy.data.texts[mainClassName]
	methodNamePrefix = 'Start'
	if textBlock.is_init_script:
		outputFileTextReplaceClauses[1] += '\n\t\t.add_systems(OnEnter(MyStates::Next), Start' + mainClassName + ')'
	else:
		outputFileTextReplaceClauses[1] += '\n\t\t.add_systems(Update, Update' + mainClassName + ')'
		methodNamePrefix = 'Update'
	addToOutputFileText += SYSTEM_TEMPLATE.replace('ꗈ0', methodNamePrefix + mainClassName).replace('ꗈ1', scriptText).replace('ꗈ', mainClassName)
	outputFileTextReplaceClauses[0] += '\n\t\t.register_type::<' + mainClassName + '>()'
	# addToOutputFileText += '\n\n' + outputFileText

def MakeComponent (objectName : str, componentType : str):
	if objectName == '':
		print('WARN: bad objectName - MakeComponent')
		return
	klass = mainClassName
	if '.' in klass: klass = klass.split('.')[0]
	obj = bpy.data.objects[objectName]
	import bevy_components.registry.registry as registry
	typeInfo = {
		'additionalProperties': False,
		'isComponent': True,
		'isResource': False,
		'properties': {},
		'required': [],
		'short_name': klass,
		'title': 'HolyBlender::' + klass,
		'type': 'object',
		'typeInfo': 'Struct'
	}
	registry.ComponentsRegistry.type_infos[componentType] = typeInfo
	import bevy_components.components.metadata as metadata
	metadata.add_component_to_object(obj, typeInfo)
	print('YAY ' + objectName + ' ' + componentType)

def RemoveComponent (objectName : str, componentType : str):
	if objectName != '':
		obj = bpy.data.objects[objectName]
		sys.path.append(os.path.expanduser('~/HolyBlender/Blender_bevy_components_workflow/tools'))
		import bevy_components.components.metadata as metadata
		metadata.remove_component_to_object(obj, componentType.replace('Unit2Many::', ''))

def DeleteScene (scene = None):
	if scene is None:
		scene = bpy.context.scene
	for obj in scene.objects:
		bpy.data.objects.remove(obj, do_unlink=True)

def SetVariableTypeAndRemovePrimitiveCastsFromOutputFile (variableType : str):
	global outputFileText
	castIndicator = ' as f32)'
	indexOfCast = 0
	while indexOfCast != -1:
		indexOfCast = outputFileText.find(castIndicator, indexOfCast + len(castIndicator))
		if indexOfCast != -1:
			indexOfCasted = IndexOfMatchingLeftParenthesis(outputFileText, indexOfCast + len(castIndicator)) + 1
			casted = outputFileText[indexOfCasted : indexOfCast]
			indexOfAssignment = outputFileText.find(casted + ' = ' + variableType)
			if indexOfAssignment:
				outputFileText = outputFileText.replace('(' + casted + ' as f32)', casted)

def MakeSceneOrPrefab (sceneOrPrefabFilePath : str):
	global mainClassName
	global membersDict
	DeleteScene ()
	sceneOrPrefabFileText = open(sceneOrPrefabFilePath, 'rb').read().decode('utf-8')
	sceneOrPrefabFileLines = sceneOrPrefabFileText.split('\n')
	currentTypes = []
	currentType = ''
	# transformsIdsDict = {}
	# elementId = ''
	# parent = ''
	localPosition = []
	localRotation = []
	localSize = []
	meshAssetPath = ''
	textureAssetPath = ''
	currentScriptsPaths = []
	lightType = -1
	lightIntensity = -1
	horizontalFov = False
	fov = -1
	isOrthographic = False
	orthographicSize = -1
	nearClipPlane = -1
	farClipPlane = -1
	objectName = ''
	for line in sceneOrPrefabFileLines:
		if line.endswith(':') or line == '':
			if line.startswith('GameObject') or line.startswith('SceneRoots') or line == '':
				components = []
				if 'Camera' in currentTypes:
					components.append(MakeCamera(localPosition, localRotation, localSize, objectName, horizontalFov, fov, isOrthographic, orthographicSize, nearClipPlane, farClipPlane))
				if 'MeshRenderer' in currentTypes:
					components.append(MakeMesh(localPosition, localRotation, localSize, objectName, meshAssetPath))
				if 'Light' in currentTypes:
					components.append(MakeLight(localPosition, localRotation, localSize, objectName, lightType, lightIntensity))
				if 'SpriteRenderer' in currentTypes:
					components.append(MakeSprite(localPosition, localRotation, localSize, objectName, textureAssetPath))
				if 'MonoBehaviour' in currentTypes:
					for scriptPath in currentScriptsPaths:
						if not scriptPath.endswith('/UniversalAdditionalCameraData.cs') and not scriptPath.endswith('/UniversalAdditionalLightData.cs'):
							mainClassName = scriptPath[scriptPath.rfind('/') + 1 : scriptPath.rfind('.')]
							MakeComponent (objectName, 'HolyBlender::' + mainClassName)
							# scriptComponent = MakeScript([], [], [1, 1, 1], objectName, scriptPath)
				# 			for component in components:
				# 				component.attach_to(scriptComponent.root_component)
				# 			components = [ scriptComponent ]
				# if parent != '' and parent != '0' and parent in transformsIdsDict:
				# 	for component in components:
				# 		component.attach_to_component(transformsIdsDict[parent])
				# if len(components) > 0:
				# 	transformsIdsDict[elementId] = components[-1]
				# parent = ''
				currentTypes.clear()
				currentScriptsPaths.clear()
				membersDict.clear()
			currentType = line[: len(line) - 1]
			currentTypes.append(currentType)
		elif line.startswith(YAML_ELEMENT_ID_INDICATOR):
			indexOfAmpersand = line.find('&', len(YAML_ELEMENT_ID_INDICATOR))
			elementId = line[indexOfAmpersand + 1 :]
		elif line.startswith('  '):
			if currentType == 'MeshFilter':
				if line.startswith(MESH_INDICATOR):
					indexOfGuid = line.find(GUID_INDICATOR)
					meshAssetPath = fileGuidsDict[line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')]]
			if currentType == 'Transform':
				if line.startswith(PARENT_INDICATOR):
					parent = line[len(PARENT_INDICATOR) : -1]
				elif line.startswith(LOCAL_POSITION_INDICATOR):
					localPosition = []
					indexOfComma = line.find(',')
					x = line[len(LOCAL_POSITION_INDICATOR) + 3 : indexOfComma]
					localPosition.append(float(x))
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfY = line.find('y: ')
					y = line[indexOfY + 3 : indexOfComma]
					localPosition.append(float(y))
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfZ = line.find('z: ')
					z = line[indexOfZ + 3 : indexOfComma]
					localPosition.append(float(z))
				elif line.startswith(LOCAL_ROTATION_INDICATOR):
					localRotation = []
					indexOfComma = line.find(',')
					x = line[len(LOCAL_ROTATION_INDICATOR) + 3 : indexOfComma]
					localRotation.append(float(x))
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfY = line.find('y: ')
					y = line[indexOfY + 3 : indexOfComma]
					localRotation.append(float(y))
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfZ = line.find('z: ')
					z = line[indexOfZ + 3 : indexOfComma]
					localRotation.append(float(z))
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfW = line.find('w: ')
					w = line[indexOfW + 3 : indexOfComma]
					localRotation.append(float(w))
				elif line.startswith(LOCAL_SCALE_INDICATOR):
					indexOfComma = line.find(',')
					localSize = []
					x = line[len(LOCAL_SCALE_INDICATOR) + 3 : indexOfComma]
					localSize.append(float(x))
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfY = line.find('y: ')
					y = line[indexOfY + 3 : indexOfComma]
					localSize.append(float(y))
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfZ = line.find('z: ')
					z = line[indexOfZ + 3 : indexOfComma]
					localSize.append(float(z))
			elif currentType == 'MonoBehaviour':
				if line.startswith(SCRIPT_INDICATOR):
					indexOfGuid = line.find(GUID_INDICATOR)
					scriptPath = fileGuidsDict.get(line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')], None)
					if scriptPath != None:
						currentScriptsPaths.append(scriptPath)
			elif currentType == 'Light':
				if line.startswith(LIGHT_TYPE_INDICATOR):
					lightType = int(line[len(LIGHT_TYPE_INDICATOR) :])
				elif line.startswith(LIGHT_INTENSITY_INDICATOR):
					lightIntensity = float(line[len(LIGHT_INTENSITY_INDICATOR) :])
			# elif currentType == 'GameObject':
			elif line.startswith(ACTIVE_INDICATOR):
				pass
			elif line.startswith(NAME_INDICATOR):
				objectName = line[len(NAME_INDICATOR) :]
			# elif currentType == 'Camera':
			elif line.startswith(FOV_AXIS_INDICATOR):
				horizontalFov = line[len(FOV_AXIS_INDICATOR) :] == '1'
			elif line.startswith(FOV_INDICATOR):
				fov = float(line[len(FOV_INDICATOR) :])
			elif line.startswith(IS_ORTHOGRAPHIC_INDICATOR):
				isOrthographic = line[len(IS_ORTHOGRAPHIC_INDICATOR) :] == '1'
			elif line.startswith(ORTHOGRAPHIC_SIZE_INDICATOR):
				orthographicSize = float(line[len(ORTHOGRAPHIC_SIZE_INDICATOR) :])
			elif line.startswith(NEAR_CLIP_PLANE_INDICATOR):
				nearClipPlane = float(line[len(NEAR_CLIP_PLANE_INDICATOR) :])
			elif line.startswith(FAR_CLIP_PLANE_INDICATOR):
				farClipPlane = float(line[len(FAR_CLIP_PLANE_INDICATOR) :])
			# elif currentType == 'SpriteRenderer':
			elif line.startswith(SPRITE_INDICATOR):
				indexOfGuid = line.find(GUID_INDICATOR)
				textureAssetPath = fileGuidsDict[line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')]]

def AddToMembersDictAndAssetsPathsDict (sceneOrPrefabFilePath : str):
	global membersDict
	global assetsPathsDict
	sceneFileLines = sceneFileText.split('\n')
	currentType = ''
	for line in sceneFileLines:
		if line.endswith(':'):
			currentType = line[: len(line) - 1]
		elif line.startswith('  ') and currentType == 'MonoBehaviour':
			if line.startswith(SCRIPT_INDICATOR):
				indexOfGuid = line.find(GUID_INDICATOR)
				scriptPath = fileGuidsDict.get(line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')], None)
				if scriptPath != None:
					mainClassName = scriptPath[scriptPath.rfind('/') + 1 : scriptPath.rfind('.')]	
			elif not line.startswith('  m_'):
				indexOfColon = line.find(': ')
				memberName = line[2 : indexOfColon] + '_' + mainClassName
				value = line[indexOfColon + 2 :]
				if value.startswith('{'):
					indexOfGuid = line.find(GUID_INDICATOR)
					assetPath = fileGuidsDict.get(line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')], None)
					if assetPath != None:
						value = assetPath
						assetsPathsDict[memberName] = assetPath
					value = '"' + value  + '"'
				membersDict[memberName] = value

data = ''
fromUnity = False
for arg in sys.argv:
	if arg.startswith(INPUT_PATH_INDICATOR):
		UNITY_PROJECT_PATH = os.path.expanduser(arg[len(INPUT_PATH_INDICATOR) :])
		fromUnity = True
	elif arg.startswith(OUTPUT_PATH_INDICATOR):
		BEVY_PROJECT_PATH = os.path.expanduser(arg[len(OUTPUT_PATH_INDICATOR) :])
		ASSETS_PATH = BEVY_PROJECT_PATH + '/assets'
		CODE_PATH = BEVY_PROJECT_PATH + '/src'
		OUTPUT_FILE_PATH = CODE_PATH + '/main.rs'
		REGISTRY_PATH = ASSETS_PATH + '/registry.json'
		data += arg + '\n'
open('/tmp/HolyBlender Data (UnityToBevy)', 'wb').write(data.encode('utf-8'))

def Do (attachedScriptsDict = {}):
	global CODE_PATH
	global mainClassName
	global OUTPUT_FILE_PATH
	global UNITY_PROJECT_PATH
	attachedScripts = []
	for scripts in attachedScriptsDict.values():
		for script in scripts:
			attachedScripts.append(script)
	toolsPath = os.path.expanduser('~/HolyBlender/Blender_bevy_components_workflow/tools')
	if os.path.isdir(toolsPath):
		addonsPath = os.path.expanduser('~/.config/blender/4.1/scripts/addons')
		if not os.path.isdir(addonsPath):
			MakeFolderForFile (addonsPath + '/')

		os.system('cd ' + toolsPath + '''
			python3 internal_generate_release_zips.py''')
		if not os.path.isdir(addonsPath + '/bevy_components'):
			os.system('unzip ' + toolsPath + '/bevy_components.zip -d ' + addonsPath)
		if not os.path.isdir(addonsPath + '/gltf_auto_export'):
			os.system('unzip ' + toolsPath + '/gltf_auto_export.zip -d ' + addonsPath)

		bpy.ops.preferences.addon_enable(module='bevy_components')
		bpy.ops.preferences.addon_enable(module='gltf_auto_export')
	# sys.path.append('~/HolyBlender/Blender_bevy_components_workflow/tools/bevy_components')
	# bpy.ops.preferences.addon_enable(module='io_import_images_as_planes')
	registryText = open(TEMPLATE_REGISTRY_PATH, 'rb').read().decode('utf-8')
	if fromUnity:
		codeFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.cs')
		i = 0
		while i < len(codeFilesPaths):
			codeFilePath = codeFilesPaths[i]
			isExcluded = False
			for excludeItem in excludeItems:
				if excludeItem in codeFilePath:
					isExcluded = True
					break
			if isExcluded:
				codeFilesPaths.pop(i)
				i -= 1
			i += 1
		for i in range(len(codeFilesPaths)):
			codeFilePath = codeFilesPaths[i]
			mainClassName = codeFilePath[codeFilePath.rfind('/') + 1 : codeFilePath.rfind('.')]
			indexOfAddRegistryTextIndicator = registryText.find('ꗈ')
			componentText = ',\n' + COMPONENT_TEMPLATE
			componentText = componentText.replace('ꗈ', mainClassName)
			registryText = registryText[: indexOfAddRegistryTextIndicator] + componentText + registryText[indexOfAddRegistryTextIndicator :]
	else:
		data = open('/tmp/HolyBlender Data (BlenderToBevy)', 'rb').read().decode('utf-8')
		BEVY_PROJECT_PATH = data.split('\n')[0]
		if not BEVY_PROJECT_PATH.strip() or BEVY_PROJECT_PATH.strip()=='/':
			BEVY_PROJECT_PATH = '/tmp'
		ASSETS_PATH = BEVY_PROJECT_PATH + '/assets'
		CODE_PATH = BEVY_PROJECT_PATH + '/src'
		OUTPUT_FILE_PATH = CODE_PATH + '/main.rs'
		REGISTRY_PATH = ASSETS_PATH + '/registry.json'
		MakeFolderForFile (ASSETS_PATH + '/')
		MakeFolderForFile (CODE_PATH + '/')
		open('/tmp/HolyBlender Data (UnityToBevy)', 'wb').write(('output=' + BEVY_PROJECT_PATH).encode('utf-8'))
		for script in attachedScripts:
			mainClassName = script.replace('.rs', '')
			indexOfAddRegistryTextIndicator = registryText.find('ꗈ')
			componentText = ',\n' + COMPONENT_TEMPLATE
			componentText = componentText.replace('ꗈ', mainClassName)
			registryText = registryText[: indexOfAddRegistryTextIndicator] + componentText + registryText[indexOfAddRegistryTextIndicator :]
	registryText = registryText.replace('ꗈ', '')
	if not os.path.isdir(ASSETS_PATH):
		os.mkdir(ASSETS_PATH)
	if not os.path.isdir(CODE_PATH):
		os.mkdir(CODE_PATH)
	open(REGISTRY_PATH, 'wb').write(registryText.encode('utf-8'))
	registry = bpy.context.window_manager.components_registry
	registry.schemaPath = REGISTRY_PATH
	bpy.ops.object.reload_registry()
	os.system('cd ' + BEVY_PROJECT_PATH + '''
		cargo init
		cargo add bevy
		cargo add bevy_asset_loader
		cargo add bevy_gltf_components
		cargo add bevy_gltf_blueprints
		rustup target install wasm32-unknown-unknown
		cargo install wasm-server-runner
		rustup target add wasm32-unknown-unknown
		cargo add serde --features derive
		cargo add wasm-bindgen --features serde-serialize''')
	if fromUnity:
		sceneFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.unity')
		for sceneFilePath in sceneFilesPaths:
			isExcluded = False
			for excludeItem in excludeItems:
				if excludeItem in sceneFilePath:
					isExcluded = True
					break
			if not isExcluded:
				sceneFileText = open(sceneFilePath, 'rb').read().decode('utf-8')
				AddToMembersDictAndAssetsPathsDict (sceneFileText)
		prefabFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.prefab')
		for prefabFilePath in prefabFilesPaths:
			isExcluded = False
			for excludeItem in excludeItems:
				if excludeItem in prefabFilePath:
					isExcluded = True
					break
			if not isExcluded:
				prefabFileText = open(prefabFilePath, 'rb').read().decode('utf-8')
				AddToMembersDictAndAssetsPathsDict (prefabFileText)
		codeFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.cs')
		for codeFilePath in codeFilesPaths:
			isExcluded = False
			for excludeItem in excludeItems:
				if excludeItem in codeFilePath:
					isExcluded = True
					break
			if not isExcluded:
				mainClassName = codeFilePath[codeFilePath.rfind('/') + 1 : codeFilePath.rfind('.')]
				MakeScript ([], [], [1, 1, 1], '', codeFilePath)
		prefabFilePaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.prefab')
		for prefabFilePath in prefabFilePaths:
			isExcluded = False
			for excludeItem in excludeItems:
				if excludeItem in prefabFilePath:
					isExcluded = True
					break
			if not isExcluded:
				prefabName = prefabFilePath[prefabFilePath.rfind('/') + 1 :]
				prefabName = prefabName.replace('.prefab', '_Prefab.glb')
				MakeSceneOrPrefab (prefabFilePath)
				bpy.ops.export_scene.gltf(filepath=ASSETS_PATH + '/' + prefabName, export_extras=True, export_cameras=True, export_lights=True)
		sceneFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.unity')
		for sceneFilePath in sceneFilesPaths:
			isExcluded = False
			for excludeItem in excludeItems:
				if excludeItem in sceneFilePath:
					isExcluded = True
					break
			if not isExcluded:
				sceneName = sceneFilePath[sceneFilePath.rfind('/') + 1 :]
				sceneName = sceneName.replace('.unity', '.glb')
				MakeSceneOrPrefab (sceneFilePath)
				bpy.ops.export_scene.gltf(filepath=ASSETS_PATH + '/' + sceneName, export_extras=True, export_cameras=True, export_lights=True)
				outputFileTextReplaceClauses[2] = sceneName
	else:
		for script in attachedScripts:
			textBlock = bpy.data.texts[script]
			mainClassName = script.replace('.rs', '')
			codeFilePath = '/tmp/' + mainClassName + '.rs'
			open(codeFilePath, 'wb').write(textBlock.as_string().encode('utf-8'))
			MakeScript ([], [], [1, 1, 1], '', codeFilePath)
		lines = data.split('\n')
		for line in lines:
			indexOfEndOfObjectName = line.find('☢️')
			if indexOfEndOfObjectName != -1:
				objectName = line[: indexOfEndOfObjectName]
				scripts = line[indexOfEndOfObjectName + 1 :].split('☣️')
				print(scripts)
				for script in scripts:
					if not script.strip(): continue
					if '.' in script: script = script.split('.')[0]
					MakeComponent (objectName, 'HolyBlender::' + script)
		sceneName = bpy.data.filepath.replace('.blend', '.glb')
		sceneName = sceneName[sceneName.rfind('/') + 1 :]
		if not sceneName: sceneName = '__holyblender__'
		bpy.ops.export_scene.gltf(filepath=ASSETS_PATH + '/' + sceneName, export_extras=True, export_cameras=True, export_lights=True)
		outputFileTextReplaceClauses[2] = sceneName
		sys.argv.append(WEBGL_INDICATOR)

	outputFileText = open(TEMPLATE_APP_PATH, 'rb').read().decode('utf-8')
	outputFileText = importStatementsText + outputFileText
	outputFileText = outputFileText.replace('ꗈ0', outputFileTextReplaceClauses[0])
	outputFileText = outputFileText.replace('ꗈ1', outputFileTextReplaceClauses[1])
	outputFileText = outputFileText.replace('ꗈ2', outputFileTextReplaceClauses[2])
	outputFileText = outputFileText.replace('ꗈ3', outputFileTextReplaceClauses[3])
	outputFileText += addToOutputFileText
	open(OUTPUT_FILE_PATH, 'wb').write(outputFileText.encode('utf-8'))
	htmlText = open(TEMPLATES_PATH + '/index.html', 'rb').read().decode('utf-8')
	if bpy.data.worlds[0].html_code != None:
		htmlText = htmlText.replace('ꗈ', bpy.data.worlds[0].html_code.as_string())
	else:
		htmlText = htmlText.replace('ꗈ', '')
	open(BEVY_PROJECT_PATH + '/index.html', 'wb').write(htmlText.encode('utf-8'))

	# os.system('cp ' + TEMPLATES_PATH + '/wasm.js' + ' ' + BEVY_PROJECT_PATH + '/api/wasm.js')
	subprocess.check_call(['cp', '-v', os.path.join(__thisdir, 'Server.py'), os.path.join(BEVY_PROJECT_PATH,'Server.py')])
	subprocess.check_call(['chmod', '+x', os.path.join(BEVY_PROJECT_PATH,'Server.py')])

	os.environ['WGPU_BACKEND'] = 'gl'
	os.environ['CARGO_TARGET_WASM32_UNKNOWN_UNKNOWN_RUNNER'] = 'wasm-server-runner'

	command = [ 'cargo', 'add', 'bevy_rapier3d' ]
	subprocess.check_call(command, cwd=BEVY_PROJECT_PATH)

	command = [ 'cargo', 'run' ]
	if WEBGL_INDICATOR in sys.argv:
		command.append('--target')
		command.append('wasm32-unknown-unknown')
	else:
		command.append('--features')
		command.append('bevy/dynamic_linking')
	print(command)
	# bpy.ops.wm.save_as_mainfile(filepath=BEVY_PROJECT_PATH + '/Test.blend')
	# projectName = BEVY_PROJECT_PATH[BEVY_PROJECT_PATH.rfind('/') + 1 :]

	process = subprocess.Popen(command, cwd=BEVY_PROJECT_PATH)
	atexit.register(lambda:process.kill())
	import time
	time.sleep(10)
	MakeFolderForFile (BEVY_PROJECT_PATH + '/api/')
	waiting = True
	while waiting:
		try:
			print('ping...')
			subprocess.check_call(['curl', 'http://127.0.0.1:1334/api/wasm.js', '-o', BEVY_PROJECT_PATH+'/api/wasm.js'])
			subprocess.check_call(['curl', 'http://127.0.0.1:1334/api/wasm.wasm','-o', BEVY_PROJECT_PATH+'/api/wasm.wasm'])
			waiting = False
		except subprocess.CalledProcessError:
			time.sleep(3)
			print('waiting for http://127.0.0.1:1334')
	try:
		process.kill()
	except:
		pass

	subprocess.check_call(['python3', 'Server.py'], cwd=BEVY_PROJECT_PATH)

if fromUnity:
	Do ()
