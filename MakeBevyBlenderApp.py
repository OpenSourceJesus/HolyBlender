import os, subprocess, bpy, sys
from math import radians
from mathutils import *

sys.path.append('/usr/lib/python3/dist-packages')
from PIL import Image

sys.path.append(os.path.expanduser('~/Unity2Many'))
from GetUnityProjectInfo import *

UNITY_PROJECT_PATH = ''
BEVY_PROJECT_PATH = ''
TEMPLATES_PATH = os.path.expanduser('~/Unity2Many/Templates')
TEMPLATE_APP_PATH = TEMPLATES_PATH + '/BevyBlenderApp.rs'
TEMPLATE_REGISTRY_PATH = TEMPLATES_PATH + '/registry.json'
ASSETS_PATH = BEVY_PROJECT_PATH + '/assets'
CODE_PATH = BEVY_PROJECT_PATH + '/src'
OUTPUT_FILE_PATH = BEVY_PROJECT_PATH + '/main.rs'
REGISTRY_PATH = ASSETS_PATH + '/registry.json'
INPUT_PATH_INDICATOR = 'input='
OUTPUT_PATH_INDICATOR = 'output='
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
COMPONENT_TEMPLATE = '''"TestBevyProject::ꗈ": {
	  "additionalProperties": false,
	  "isComponent": true,
	  "isResource": false,
	  "properties": {},
	  "required": [],
	  "short_name": "ꗈ",
	  "title": "TestBevyProject::ꗈ",
	  "type": "object",
	  "typeInfo": "Struct"
	}'''
# CAMERA_2D_TEMPLATE = '''commands.spawn(Camera2dBundle {
# 		transform: Transform::from_xyz(ꗈ0, ꗈ1, ꗈ2).with_rotation(Quat::from_xyzw(ꗈ3, ꗈ4, ꗈ5, ꗈ6)),
# 		projection: OrthographicProjection { near: ꗈ7, far: ꗈ8, scale: ꗈ9, ..default() },
# 		..default()
# 	});'''
# CAMERA_3D_TEMPLATE = '''commands.spawn(Camera3dBundle {
# 		transform: Transform::from_xyz(ꗈ0, ꗈ1, ꗈ2).with_rotation(Quat::from_xyzw(ꗈ3, ꗈ4, ꗈ5, ꗈ6)),
# 		projection: PerspectiveProjection { near: ꗈ7, far: ꗈ8, fov: ꗈ9.to_radians(), ..default() },
# 		..default()
# 	});'''
# MESH_TEMPLATE = '''commands.spawn((SceneBundle {
# 		scene: assetServer.load("ꗈ7"),
# 		transform: Transform::from_xyz(ꗈ0, ꗈ1, ꗈ2).with_rotation(Quat::from_xyzw(ꗈ3, ꗈ4, ꗈ5, ꗈ6)),
# 		..default()
# 		},
# 		Name::new("ꗈ7"),
# 	));'''
SYSTEM_METHOD_ARGUMENTS = '''mut commands: Commands,
	assetServer: Res<AssetServer>,
	mut meshes : ResMut<Assets<Mesh>>,
	keys: Res<ButtonInput<KeyCode>>,
	mouseButtons: Res<ButtonInput<MouseButton>>,
	mut query: Query<&mut Transform, With<ꗈ>>,
	mut nameQuery: Query<&mut Name>,
	time: Res<Time>,
	mut cursorEvent: EventReader<CursorMoved>'''
CUSTOM_TYPE_INDICATOR = '''#[derive(Component, Reflect, Default, Debug)]
#[reflect(Component)]
struct ꗈ;'''
PI = 3.141592653589793
outputFileText = ''
importStatementsText = ''
outputFileTextReplaceClauses = [ '', '', '' ]
addToOutputFileText = ''
mainClassName = ''
translatedFiles = []
mainClassNames = []

for arg in sys.argv:
	if arg.startswith(INPUT_PATH_INDICATOR):
		UNITY_PROJECT_PATH = os.path.expanduser(arg[len(INPUT_PATH_INDICATOR) :])
	elif arg.startswith(OUTPUT_PATH_INDICATOR):
		BEVY_PROJECT_PATH = os.path.expanduser(arg[len(OUTPUT_PATH_INDICATOR) :])
		ASSETS_PATH = BEVY_PROJECT_PATH + '/assets'
		CODE_PATH = BEVY_PROJECT_PATH + '/src'
		OUTPUT_FILE_PATH = CODE_PATH + '/main.rs'
		REGISTRY_PATH = ASSETS_PATH + '/registry.json'
codeFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.cs')
registryText = open(TEMPLATE_REGISTRY_PATH, 'rb').read().decode('utf-8')
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
	componentText = COMPONENT_TEMPLATE
	componentText = componentText.replace('ꗈ', mainClassName)
	if i < len(codeFilesPaths) - 1:
		componentText += ','
	registryText = registryText[: indexOfAddRegistryTextIndicator] + componentText + registryText[indexOfAddRegistryTextIndicator :]
registryText = registryText.replace('ꗈ', '')
open(REGISTRY_PATH, 'wb').write(registryText.encode('utf-8'))
registry = bpy.context.window_manager.components_registry
registry.schemaPath = REGISTRY_PATH
bpy.ops.object.reload_registry()
typeInfos = registry.type_infos
addComponentOperator = bpy.ops.object.add_bevy_component

def ConvertCSFileToRust (filePath):
	global mainClassName
	mainClassName = filePath[filePath.rfind('/') + 1 : filePath.rfind('.')]
	assert os.path.isfile(filePath)
	command = [
		'dotnet',
		os.path.expanduser('~/Unity2Many/UnityToBevy/Unity2Many.dll'), 
		'includeFile=' + filePath,
		'bevy=true',
		'output=/tmp',
		'outputFolder=/tmp'
	]
	# for arg in sys.argv:
	# 	command.append(arg)
	# command.append(UNITY_PROJECT_PATH)
	print(command)

	subprocess.check_call(command)

	outputFilePath = CODE_PATH + '/main.py'
	print(outputFilePath)
	assert os.path.isfile(outputFilePath)

	os.system('cat ' + outputFilePath)

	ConvertPythonFileToRust (outputFilePath)

def ConvertPythonFileToRust (filePath):
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
	cameraText = ''
	if isOrthographic:
		# cameraText = CAMERA_2D_TEMPLATE
		cameraData.type = 'ORTHO'
		cameraData.ortho_scale = orthographicSize * 4
		if not horizontalFov:
			cameraData.ortho_scale *= bpy.context.scene.render.resolution_x / bpy.context.scene.render.resolution_y
	# else:
	# 	cameraText = CAMERA_3D_TEMPLATE
	# cameraText = cameraText.replace('ꗈ0', str(cameraObject.location.x))
	# cameraText = cameraText.replace('ꗈ1', str(cameraObject.location.y))
	# cameraText = cameraText.replace('ꗈ2', str(-cameraObject.location.z))
	# cameraText = cameraText.replace('ꗈ3', str(localRotation.x))
	# cameraText = cameraText.replace('ꗈ4', str(localRotation.y))
	# cameraText = cameraText.replace('ꗈ5', str(localRotation.z))
	# cameraText = cameraText.replace('ꗈ6', str(localRotation.w))
	# cameraText = cameraText.replace('ꗈ7', str(nearClipPlane))
	# cameraText = cameraText.replace('ꗈ8', str(farClipPlane))
	# if isOrthographic:
	# 	cameraText = cameraText.replace('ꗈ9', str(orthographicSize))
	# else:
	# 	cameraText = cameraText.replace('ꗈ9', str(fov))
	outputFileTextReplaceClauses[2] += cameraText

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
	if lightType == 1:
		lightType = 'SUN'
	elif lightType == 2:
		lightType = 'POINT'
	lightData = bpy.data.lights.new(name='Light data', type=lightType)
	lightObject = bpy.data.objects.new('Light', lightData)
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
		image = Image.open(textureAssetPath)
		multiplySize = max(image.width, image.height) / pixelsPerUnit
		importedObject.scale = Vector((localSize[0], localSize[1], -localSize[2])) * multiplySize
	return importedObject

def MakeScript (localPosition : list, localRotation : list, localSize : list, objectName : str, scriptPath : str):
	global mainClassName
	global outputFileText
	global addToOutputFileText
	global importStatementsText
	global outputFileTextReplaceClauses
	ConvertCSFileToRust (scriptPath)
	MakeComponent (objectName, 'TestBevyProject::' + mainClassName)
	outputFileText = open(OUTPUT_FILE_PATH, 'rb').read().decode('utf-8')
	if 'fn Update' in outputFileText:
		# importStatementsText += 'use ' + mainClassName + '::*;\n'
		# outputFileTextReplaceClauses[1] += '.add_systems(Update, ' + mainClassName + '::' + mainClassName + '::Update)'
		outputFileTextReplaceClauses[1] += '\n\t\t.add_systems(Update, Update' + mainClassName + ')'
	# open(BEVY_PROJECT_PATH + '/' + mainClassName + '.rs', 'wb').write(outputFileText.encode('utf-8'))
	# outputFileText = 'pub mod ' + mainClassName + '\n{\n' + outputFileText + '\n}'
	outputFileText = outputFileText.replace('fn Start', 'fn Start' + mainClassName)
	outputFileText = outputFileText.replace('Time.deltaTime', 'time.delta_seconds()')
	outputFileText = outputFileText.replace('Vector2', 'Vec2')
	outputFileText = outputFileText.replace('Vec2.zero', 'Vec2::ZERO')
	outputFileText = outputFileText.replace('Vector3', 'Vec3')
	outputFileText = outputFileText.replace('Vec3.zero', 'Vec3::ZERO')
	outputFileText = outputFileText.replace('Vec3.forward', '-Vec3::Y')
	SetVariableTypeAndRemovePrimitiveCastsFromOutputFile ('Vec2')
	SetVariableTypeAndRemovePrimitiveCastsFromOutputFile ('Vec3')
	outputFileText = outputFileText.replace('.Normalize', '.normalize')
	outputFileText = outputFileText.replace('pub const ', 'let mut ')
	outputFileText = outputFileText.replace('pub static ', 'let mut ')
	outputFileText = outputFileText.replace('transform.position', 'trs.translation')
	outputFileText = outputFileText.replace('transform.rotation', 'trs.rotation')
	outputFileText = outputFileText.replace('self, ', '')
	outputFileText = outputFileText.replace('&self', '')
	outputFileText = outputFileText.replace('self.', '')
	outputFileText = outputFileText.replace('self', '')
	indexOfAtan2 = 0
	while indexOfAtan2 != -1:
		atan2Indicator = 'Mathf.Atan2('
		indexOfAtan2 = outputFileText.find(atan2Indicator, indexOfAtan2 + len(atan2Indicator))
		if indexOfAtan2 != -1:
			indexOfComma = outputFileText.find(',', indexOfAtan2)
			yClause = outputFileText[indexOfAtan2 + len(atan2Indicator) : indexOfComma]
			indexOfRightParenthesis = IndexOfMatchingRightParenthesis(outputFileText, indexOfAtan2 + len(atan2Indicator))
			xClause = outputFileText[indexOfComma + 1 : indexOfRightParenthesis]
			outputFileText = outputFileText.replace(outputFileText[indexOfAtan2 : indexOfRightParenthesis + 1], yClause + '.atan2(' + xClause + ')')
	outputFileText = outputFileText.replace('(, ', '(')
	indexOfY = 0
	while indexOfY != -1:
		indexOfY = outputFileText.find('.y', indexOfY + 2)
		if indexOfY != -1:
			indexOfToken = IndexOfAny(outputFileText, ['=', ' ', '+', '-', '*', '/', ')', ']'], indexOfY + 2)
			if indexOfToken == indexOfY + 2:
				indexOfEquals = outputFileText.find('=', indexOfToken + 3)
				if indexOfEquals == indexOfToken + 1:
					indexOfToken += 1
				outputFileText = outputFileText[: indexOfToken + 3] + '-' + outputFileText[indexOfToken + 3 :]
			outputFileText = Remove(outputFileText, indexOfY + 1, 1)
			outputFileText = outputFileText[: indexOfY + 1] + 'z' + outputFileText[indexOfY + 1 :]
	indexOfTrsEulerAngles = 0
	while indexOfTrsEulerAngles != -1:
		trsEulerAnglesIndicator = 'transform.eulerAngles'
		indexOfTrsEulerAngles = outputFileText.find(trsEulerAnglesIndicator, indexOfTrsEulerAngles + len(trsEulerAnglesIndicator))
		if indexOfTrsEulerAngles != -1:
			indexOfEquals = outputFileText.find('=', indexOfTrsEulerAngles + len(trsEulerAnglesIndicator))
			textBetweenTrsEulerAnglesAndEquals = outputFileText[indexOfTrsEulerAngles + len(trsEulerAnglesIndicator) : indexOfEquals]
			if textBetweenTrsEulerAnglesAndEquals == '' or textBetweenTrsEulerAnglesAndEquals == ' ':
				indexOfSemicolon = outputFileText.find(';', indexOfEquals)
				valueAfterEquals = outputFileText[indexOfEquals + 1 : indexOfSemicolon]
				outputFileText = outputFileText.replace(trsEulerAnglesIndicator + textBetweenTrsEulerAnglesAndEquals + '=' + valueAfterEquals, 'let rotation = ' + valueAfterEquals + ' * ' + str(PI) + ' / 180.0;\ntrs.rotation = Quat::from_euler(EulerRot::ZYX, rotation.x, rotation.y + 90.0, rotation.z)')
	outputFileText = outputFileText.replace(mainClassName + '::', '')
	outputFileText = outputFileText.replace('&' + mainClassName + ' {}', '')
	indexOfMacro = 0
	while indexOfMacro != -1:
		indexOfMacro = outputFileText.find('#![')
		if indexOfMacro != -1:
			indexOfNewLine = outputFileText.find('\n', indexOfMacro)
			outputFileText = RemoveStartEnd(outputFileText, indexOfMacro, indexOfNewLine)
	indexOfDefaultComment = 0
	while indexOfDefaultComment != -1:
		indexOfDefaultComment = outputFileText.find('//! ')
		if indexOfDefaultComment != -1:
			indexOfNewLine = outputFileText.find('\n', indexOfDefaultComment)
			outputFileText = RemoveStartEnd(outputFileText, indexOfDefaultComment, indexOfNewLine)
	mainClassIndicator = 'impl ' + mainClassName + ' {'
	indexOfMainClass = outputFileText.find(mainClassIndicator)
	if indexOfMainClass != -1:
		indexOfMainClassEnd = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfMainClass + len(mainClassIndicator))
		outputFileText = Remove(outputFileText, indexOfMainClassEnd, 1)
		outputFileText = Remove(outputFileText, indexOfMainClass, len(mainClassIndicator))
	mainClassIndicator = 'pub struct ' + mainClassName + ' {'
	indexOfMainClass = outputFileText.find(mainClassIndicator)
	membersDict = {}
	if indexOfMainClass != -1:
		indexOfMainClassEnd = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfMainClass + len(mainClassIndicator))
		mainClassContents = outputFileText[indexOfMainClass + len(mainClassIndicator) : indexOfMainClassEnd]
		outputFileText = Remove(outputFileText, indexOfMainClassEnd, 1)
		outputFileText = Remove(outputFileText, indexOfMainClass, len(mainClassIndicator))
		newMainClassContents = mainClassContents.replace('pub ', 'static mut ')
		newMainClassContents = newMainClassContents.replace(',', ';')
		pythonFileText = open(OUTPUT_FILE_PATH.replace('.rs', '.py'), 'rb').read().decode('utf-8')
		pythonFileLines = pythonFileText.split('\n')
		pythonFileLines.pop(0)
		for line in pythonFileLines:
			if line.startswith(CLASS_MEMBER_INDICATOR):
				indexOfColon = line.find(':')
				memberName = line[len(CLASS_MEMBER_INDICATOR) : indexOfColon]
				memberValue = line[indexOfColon + 1 :]
				membersDict[memberName] = memberValue
				indexOfMemberName = 0
				while indexOfMemberName != -1:
					indexOfMemberName = newMainClassContents.find(memberName, indexOfMemberName + 1)
					if indexOfMemberName != -1:
						# newMainClassContents = newMainClassContents[: indexOfMemberName + len(memberName)] + mainClassName + newMainClassContents[indexOfMemberName + len(memberName) :]
						indexOfSemicolon = newMainClassContents.find(';', indexOfMemberName)
						newMainClassContents = newMainClassContents[: indexOfSemicolon] + ' = ' + memberValue + newMainClassContents[indexOfSemicolon :]
			else:
				break
		# mainClassMembersDeclarations = newMainClassContents.split(';')
		# for mainClassMembersDeclaration in mainClassMembersDeclarations:
		# 	mainClassMemberName = mainClassMembersDeclaration[len('static ') : mainClassMembersDeclaration.find(':')]
		# 	if mainClassMemberName != '':
		# 		newMainClassContents = newMainClassContents.replace(mainClassMemberName, mainClassMemberName + mainClassName)
		outputFileText = outputFileText.replace(mainClassContents, newMainClassContents)
	mainMethodIndicator = 'pub fn main() {'
	indexOfMainMethod = outputFileText.find(mainMethodIndicator)
	if indexOfMainMethod != -1:
		indexOfMainMethodEnd = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfMainClass + len(mainClassIndicator))
		outputFileText = RemoveStartEnd(outputFileText, indexOfMainMethod, indexOfMainMethodEnd)
	publicMethodIndicator = 'pub fn '
	indexOfPublicMethodIndicator = 0
	while indexOfPublicMethodIndicator != -1:
		indexOfPublicMethodIndicator = outputFileText.find(publicMethodIndicator, indexOfPublicMethodIndicator + len(publicMethodIndicator))
		if indexOfPublicMethodIndicator != -1:
			indexOfLeftParenthesis = outputFileText.find('(', indexOfPublicMethodIndicator)
			outputFileText = outputFileText[: indexOfLeftParenthesis + 1] + SYSTEM_METHOD_ARGUMENTS.replace('ꗈ', mainClassName) + outputFileText[indexOfLeftParenthesis + 1 :]
			# indexOfLeftCurlyBrace = outputFileText.find('{', indexOfLeftParenthesis + 1 + len(SYSTEM_METHOD_ARGUMENTS))
			# indexOfRightCurlyBrace = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfLeftCurlyBrace)
			# unsafeIndicator = '\nunsafe\n{'
			# outputFileText = outputFileText[: indexOfLeftCurlyBrace + 1] + unsafeIndicator + outputFileText[indexOfLeftCurlyBrace + 1 :]
			# outputFileText = outputFileText[: indexOfRightCurlyBrace + len(unsafeIndicator)] + '}\n' + outputFileText[indexOfRightCurlyBrace + len(unsafeIndicator) :]
			# if outputFileText[indexOfPublicMethodIndicator :].startswith('Update' + mainClassName):
			indexOfLeftCurlyBrace = outputFileText.find('{', indexOfLeftParenthesis + 1 + len(SYSTEM_METHOD_ARGUMENTS))
			indexOfRightCurlyBrace = IndexOfMatchingRightCurlyBrace(outputFileText, indexOfLeftCurlyBrace)
			query = '\nunsafe\n{\nfor mut trs in &mut query\n{'
			outputFileText = outputFileText[: indexOfLeftCurlyBrace + 1] + query + outputFileText[indexOfLeftCurlyBrace + 1 :]
			outputFileText = outputFileText[: indexOfRightCurlyBrace + len(query)] + '}\n}\n' + outputFileText[indexOfRightCurlyBrace + len(query) :]
			# else:
			# 	pass
	indexOfInstantiate = 0
	while indexOfInstantiate != -1:
		instantiateIndicator = 'Instantiate('
		indexOfInstantiate = outputFileText.find(instantiateIndicator)
		if indexOfInstantiate != -1:
			indexOfRightParenthesis = IndexOfMatchingRightParenthesis(outputFileText, indexOfInstantiate + len(instantiateIndicator))
			instantiateCommand = outputFileText[indexOfInstantiate : indexOfRightParenthesis + 1]
			if instantiateCommand == '':
				break
			indexOfEndOfWhatToInstantiate = outputFileText.find(',', indexOfInstantiate)
			position = ''
			rotation = ''
			if indexOfEndOfWhatToInstantiate > indexOfRightParenthesis:
				indexOfEndOfWhatToInstantiate = indexOfRightParenthesis
			elif indexOfEndOfWhatToInstantiate != -1:
				indexOfPosition = outputFileText.find(',', indexOfEndOfWhatToInstantiate + 1)
				indexOfRotation = outputFileText.find(',', indexOfPosition + 1)
				position = outputFileText[indexOfPosition + 1 : indexOfRotation]
				rotation = outputFileText[indexOfRotation + 1 : indexOfRightParenthesis]
			whatToInstantiate = outputFileText[indexOfInstantiate + len(instantiateIndicator) : indexOfEndOfWhatToInstantiate]
			whatToInstantiate = '''Camera2dBundle {
					..default()
				}'''
			newInstantiateCommand = 'let mut spawned = commands.spawn(' + whatToInstantiate + ').id();'
			print('YAY' + position + 'YAY2')
			print('YAY' + rotation + 'YAY2')
			if position != '':
				# newInstantiateCommand += ', ' + position + ', ' + rotation
				newInstantiateCommand += 'spawned.translation = ' + position + ';'
				newInstantiateCommand += 'spawned.rotation = ' + rotation + ';'
			# newInstantiateCommand += ')'
			outputFileText = outputFileText.replace(instantiateCommand, newInstantiateCommand)
	indexOfGameObjectFind = 0
	while indexOfGameObjectFind != -1:
		indexOfGameObjectFind = outputFileText.find(GAME_OBJECT_FIND_INDICATOR)
		if indexOfGameObjectFind != -1:
			indexOfRightParenthesis = outputFileText.IndexOfMatchingRightParenthesis(indexOfGameObjectFind + GAME_OBJECT_FIND_INDICATOR.Length)
			gameObjectFind = outputFileText.SubstringStartEnd(indexOfGameObjectFind, indexOfRightParenthesis)
			print('YAY' + gameObjectFind)
			whatToFind = gameObjectFind.SubstringStartEnd(GAME_OBJECT_FIND_INDICATOR.Length, gameObjectFind.Length - 2)
			entitytFind = '\nunsafe\n{\nfor mut enitty in &mut nameQuery\n{if enitty == ' + whatToFind + '\n{'
			outputLine = outputLine.Replace(gameObjectFind, entitytFind)
	indexOfUpdateMethod = outputFileText.find('fn Update')
	if indexOfUpdateMethod != -1:
		outputFileText = outputFileText.replace('fn Update', 'fn Update' + mainClassName)
		outputFileText += CUSTOM_TYPE_INDICATOR.replace('ꗈ', mainClassName)
		outputFileTextReplaceClauses[0] += '\n\t\t.register_type::<' + mainClassName + '>()'
	for memberName in membersDict:
		outputFileText = outputFileText.replace(memberName, memberName + mainClassName)
	addToOutputFileText += '\n\n' + outputFileText

def MakeComponent (objectName : str, componentType : str):
	global mainClassName
	definition = typeInfos[componentType]
	componentType = definition['title']
	isComponent = definition['isComponent'] if 'isComponent' in definition else False
	if isComponent:
		addComponentOperator(component_type=componentType)
		if objectName != '':
			bpy.data.objects[objectName][mainClassName] = ''
		# if 'SomeProp' in bpy.context.object:
		# 	print('Property found')
		# value = bpy.data.scenes['Scene'].get('test_prop', 'fallback value')
		# group = bpy.data.groups.new('MyTestGroup')
		# group['GameSettings'] = {'foo': 10, 'bar': 'spam', 'baz': {}}
		# del group['GameSettings']

# for typeInfo in typeInfos:
# 	MakeComponent (typeInfo)

def DeleteScene (scene = None):
	if scene is None:
		scene = bpy.context.scene
	elif isinstance(scene, str):
		scene = bpy.data.scenes[scene]
	for object in scene.objects:
		bpy.data.objects.remove(object, do_unlink=True)

os.system('''cd Blender_bevy_components_workflow/tools
python3 internal_generate_release_zips.py
unzip bevy_components.zip -d ''' + os.path.expanduser('~/.config/blender/4.1/scripts/addons') + '''
unzip gltf_auto_export.zip -d ''' + os.path.expanduser('~/.config/blender/4.1/scripts/addons'))

sceneName = ''
bpy.ops.preferences.addon_enable(module='bevy_components')
bpy.ops.preferences.addon_enable(module='gltf_auto_export')
bpy.ops.preferences.addon_enable(module='io_import_images_as_planes')

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

sceneFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.unity')
scriptsPaths = []
for sceneFilePath in sceneFilesPaths:
	isExcluded = False
	for excludeItem in excludeItems:
		if excludeItem in sceneFilePath:
			isExcluded = True
			break
	if isExcluded:
		continue
	sceneFileText = open(sceneFilePath, 'rb').read().decode('utf-8')
	sceneFileLines = sceneFileText.split('\n')
	for line in sceneFileLines:
		if line.startswith(SCRIPT_INDICATOR):
			indexOfGuid = line.find(GUID_INDICATOR)
			scriptPath = fileGuidsDict.get(line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')], None)
			if scriptPath != None:
				scriptsPaths.append(scriptPath)
codeFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.cs')
for codeFilePath in codeFilesPaths:
	isExcluded = False
	for excludeItem in excludeItems:
		if excludeItem in codeFilePath:
			isExcluded = True
			break
	if not isExcluded and codeFilePath not in scriptsPaths:
		MakeScript ([], [], [1, 1, 1], '', codeFilePath)
		mainClassName = codeFilePath[codeFilePath.rfind('/') + 1 : codeFilePath.rfind('.')]
sceneFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.unity')
for sceneFilePath in sceneFilesPaths:
	isExcluded = False
	for excludeItem in excludeItems:
		if excludeItem in sceneFilePath:
			isExcluded = True
			break
	if isExcluded:
		continue
	sceneName = sceneFilePath[sceneFilePath.rfind('/') + 1 :]
	sceneName = sceneName.replace('.unity', '.glb')
	DeleteScene ()
	sceneFileText = open(sceneFilePath, 'rb').read().decode('utf-8')
	sceneFileLines = sceneFileText.split('\n')
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
	for line in sceneFileLines:
		if line.endswith(':'):
			if line.startswith('GameObject') or line.startswith('SceneRoots'):
				components = []
				if 'Camera' in currentTypes:
					components.append(MakeCamera(localPosition, localRotation, localSize, '', horizontalFov, fov, isOrthographic, orthographicSize, nearClipPlane, farClipPlane))
				if 'MeshRenderer' in currentTypes:
					components.append(MakeMesh(localPosition, localRotation, localSize, '', meshAssetPath))
				if 'Light' in currentTypes:
					components.append(MakeLight(localPosition, localRotation, localSize, '', lightType, lightIntensity))
				if 'SpriteRenderer' in currentTypes:
					components.append(MakeSprite(localPosition, localRotation, localSize, '', textureAssetPath))
				if 'MonoBehaviour' in currentTypes:
					for scriptPath in currentScriptsPaths:
						if not scriptPath.endswith('/UniversalAdditionalCameraData.cs') and not scriptPath.endswith('/UniversalAdditionalLightData.cs'):
							scriptComponent = MakeScript([], [], [1, 1, 1], objectName, scriptPath)
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
			elif currentType == 'GameObject':
				if line.startswith(ACTIVE_INDICATOR):
					pass
				elif line.startswith(NAME_INDICATOR):
					objectName = line[len(NAME_INDICATOR) :]
			elif currentType == 'Transform':
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
					lightIntensity = int(line[len(LIGHT_INTENSITY_INDICATOR) :])
			# elif currentType == 'Camera':
			if line.startswith(FOV_AXIS_INDICATOR):
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
			if line.startswith(SPRITE_INDICATOR):
				indexOfGuid = line.find(GUID_INDICATOR)
				textureAssetPath = fileGuidsDict[line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')]]
outputFileText = open(TEMPLATE_APP_PATH, 'rb').read().decode('utf-8')
outputFileText = importStatementsText + outputFileText
outputFileText = outputFileText.replace('ꗈ0', outputFileTextReplaceClauses[0])
outputFileText = outputFileText.replace('ꗈ1', outputFileTextReplaceClauses[1])
outputFileText = outputFileText.replace('ꗈ2', outputFileTextReplaceClauses[2])
outputFileText += addToOutputFileText
open(OUTPUT_FILE_PATH, 'wb').write(outputFileText.encode('utf-8'))
bpy.ops.export_scene.gltf(filepath=ASSETS_PATH + '/' + sceneName, export_extras=True, export_cameras=True)
command = [ 'cargo', 'run', '--features', 'bevy/dynamic_linking' ]
print(command)

os.environ['WGPU_BACKEND'] = 'gl'
subprocess.check_call(command)