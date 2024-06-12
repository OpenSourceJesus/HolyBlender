import unreal, os, sys, subprocess
sys.path.append(os.path.expanduser('~/Unity2Many'))
from StringExtensions import *
from SystemExtensions import *

INPUT_PATH_INDICATOR = 'input='
OUTPUT_PATH_INDICATOR = 'output='
EXCLUDE_ITEM_INDICATOR = 'exclude='
GAME_OBJECT_ID_INDICATOR = '--- !u!1 &'
GUID_INDICATOR = 'guid: '
GAME_OBJECT_INDICATOR = '  m_GameObject: {fileID: '
PARENT_INDICATOR = '  m_Father: {fileID: '
ACTIVE_INDICATOR = '  m_IsActive: '
MESH_INDICATOR = '  m_Mesh: '
SPRITE_INDICATOR = '  m_Sprite: '
SCRIPT_INDICATOR = '  m_Script: '
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
UNITY_2_MANY_PATH = os.path.expanduser('~/Unity2Many')
UNITY_PROJECT_PATH = ''
UNREAL_PROJECT_PATH = ''
UNREAL_PROJECT_NAME = ''
CODE_PATH = UNREAL_PROJECT_PATH + ''
LEVEL_EDITOR = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
ASSET_TOOLS = unreal.AssetToolsHelpers().get_asset_tools()
ASSET_REGISTRY = assetRegistry = unreal.AssetRegistryHelpers.get_asset_registry()
EDITOR_ASSET = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
INTERCHANGE_MANAGER = unreal.InterchangeManager.get_interchange_manager_scripted()
EDITOR = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
EDITOR_UTILITY = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
SUBOBJECT_DATA = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
PI = 3.141592653589793
excludeItems = []
blueprintAsset = None
CLASS_MEMBER_INDICATOR = '#💠'
mainClassNames = []
membersDict = {}
filePathMembersNamesDict = {}

def ConvertPythonFileToCpp (filePath):
	global fromUnity
	global membersDict
	global mainClassNames
	global filePathMembersNamesDict
	lines = []
	for line in open(filePath, 'rb').read().decode('utf-8').splitlines():
		if line.startswith('import ') or line.startswith('from '):
			print('Skipping line:', line)
			continue
		lines.append(line)
	text = '\n'.join(lines)
	open(filePath, 'wb').write(text.encode('utf-8'))
	outputFilePath = CODE_PATH + filePath[filePath.rfind('/') :]
	command = [ 'python3', os.path.expanduser('~/Unity2Many') + '/py2many/py2many.py', '--cpp=1', outputFilePath, '--unreal=1', '--outdir=' + CODE_PATH ]
	# for arg in sys.argv:
	# 	command.append(arg)
	if fromUnity:
		command.append(UNITY_PROJECT_PATH)
	else:
		command.append('/tmp/Unity2Many (Unreal Scripts)')
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
			value = membersDict.get(variableName, None)
			mainConstructor = '::A' + mainClassName + '() {'
			indexOfMainConstructor = outputFileText.find(mainConstructor)
			if indexOfEquals != -1:
				if value == None:
					value = line[indexOfEquals + 1 :]
				outputFileText = outputFileText[: indexOfMainConstructor + len(mainConstructor) + 1] + '\t' + variableName + ' = ' + value + ';\n' + outputFileText[indexOfMainConstructor + len(mainConstructor) + 1 :]
			else:
				for memberName in filePathMembersNamesDict:
					referenceString = filePathMembersNamesDict[variableName]
					if referenceString.endswith('.prefab"'):
						referenceString = referenceString.replace('.prefab"', '')
						referenceString = referenceString[referenceString.rfind('/') + 1 :] + '_Script'
						referenceString = '/Game/' + referenceString + '/' + referenceString + '.' + referenceString
						outputFileText = outputFileText[: indexOfMainConstructor + len(mainConstructor) + 1] + '\t' + variableName + ' = "' + referenceString + '";\n' + outputFileText[indexOfMainConstructor + len(mainConstructor) + 1 :]
		else:
			break
	outputFileLines = outputFileText.split('\n')
	for i in range(len(outputFileLines) - 2, -1, -1):
		line = outputFileLines[i]
		if line != '':
			for mainClassName in mainClassNames:
				if line.startswith('A' + mainClassName):
					line = line.replace('A' + mainClassName, 'FString')
					outputFileLines[i] = line
					break
			mainClassName = os.path.split(outputFilePath)[-1].split('.')[0]
			for memberName in membersDict:
				indexOfMemberName = 0
				while indexOfMemberName != -1:
					indexOfMemberName = line.find(memberName, indexOfMemberName + 1)
					if indexOfMemberName != -1:
						memberValue = membersDict[memberName]
						line = line.replace(line[indexOfMemberName :], memberName + '_' + mainClassName + ' = ' + memberValue + ';')
						line = line.replace('_' + mainClassName + '_' + mainClassName, '_' + mainClassName)
						outputFileLines[i] = line
		else:
			break
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
	indexOfUProperty = 0
	uPropertyIndicator = 'UPROPERTY('
	while indexOfUProperty != -1:
		indexOfUProperty = headerFileText.find(uPropertyIndicator, indexOfUProperty + len(uPropertyIndicator))
		indexOfNewLine = headerFileText.find('\n', indexOfUProperty)
		indexOfSpace = headerFileText.find(' ', indexOfNewLine + 1)
		variableType = headerFileText[indexOfNewLine + 1 : indexOfSpace]
		variableType = variableType.replace('\t', '')
		if variableType.startswith('A'):
			variableType = variableType[1 :]
			if variableType in mainClassNames:
				headerFileText = RemoveStartEnd(headerFileText, indexOfNewLine + 1, indexOfSpace)
				headerFileText = headerFileText[: indexOfNewLine + 1] + 'FString' + headerFileText[indexOfNewLine + 1 :]
	open(outputFilePath.replace('.py', '.cpp'), 'wb').write(outputFileText.encode('utf-8'))
	open(outputFilePath.replace('.py', '.h'), 'wb').write(headerFileText.encode('utf-8'))
	command = [ 'cat', outputFilePath.replace('.py', '.cpp') ]
	print(command)

	subprocess.check_call(command)

def ConvertCSFileToCPP (filePath):
	global fromUnity
	assert os.path.isfile(filePath)
	command = [
		'dotnet',
		os.path.expanduser('~/Unity2Many/UnityToUnreal/Unity2Many.dll'),
		'includeFile=' + filePath,
		'unreal=true',
		'output=' + CODE_PATH,
	]
	# for arg in sys.argv:
	# 	command.append(arg)
	if fromUnity:
		command.append(UNITY_PROJECT_PATH)
	else:
		command.append('/tmp/Unity2Many (Unreal Scripts)')
	print(command)

	subprocess.check_call(command)

	outputFilePath = CODE_PATH + filePath[filePath.rfind('/') :]
	outputFilePath = outputFilePath.replace('.cs', '.py')
	print(outputFilePath)
	assert os.path.isfile(outputFilePath)

	os.system('cat ' + outputFilePath)

	ConvertPythonFileToCpp (outputFilePath)

def MakeStaticMeshActor (location : unreal.Vector, rotation : unreal.Rotator, size : unreal.Vector, meshAssetPath : str):
	projectFilePath = UNREAL_PROJECT_PATH + '/Content' + meshAssetPath[meshAssetPath.rfind('/') :]
	os.system('cp \'' + meshAssetPath + '\' \'' + projectFilePath + '\'')
	staticMesh = LoadObject(meshAssetPath)
	staticMeshActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor.static_class(), location, rotation)
	staticMeshActor.static_mesh_component.set_static_mesh(staticMesh)
	staticMeshActor.set_actor_scale3d(size)
	staticMeshActor.set_mobility(unreal.ComponentMobility.MOVABLE)
	return staticMeshActor

def MakePaperSpriteActor (location : unreal.Vector, rotation : unreal.Rotator, size : unreal.Vector, textureAssetPath : str):
	texture = LoadObject(textureAssetPath)
	paperSpriteActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PaperSpriteActor.static_class(), location, rotation)
	lastIndexOfPeriod = textureAssetPath.rfind('.')
	assetName = textureAssetPath[textureAssetPath.rfind('/') + 1 : lastIndexOfPeriod] + '_PaperSprite'
	destinationPath = '/Game/' + assetName
	paperSpriteFactory = unreal.PaperSpriteFactory()
	paperSpriteFactory.create_new = True
	importData = unreal.AutomatedAssetImportData()
	importData.filenames = [textureAssetPath]
	importData.destination_path = destinationPath
	importData.replace_existing = True
	paperSpriteFactory.automated_import_data = importData
	paperSprite = ASSET_TOOLS.create_asset(assetName, destinationPath, unreal.PaperSprite.static_class(), paperSpriteFactory)
	destinationPath += '/' + assetName
	ASSET_REGISTRY.scan_files_synchronous([destinationPath])
	unreal.EditorAssetSubsystem().save_asset(destinationPath)
	paperSprite = unreal.load_object(None, destinationPath)
	paperSprite.set_editor_property('source_texture', texture)
	pixelsPerUnit = -1
	fileLines = open(textureAssetPath + '.meta', 'rb').read().decode('utf-8').splitlines()
	for line in fileLines:
		if line.startswith(PIXELS_PER_UNIT_INDICATOR):
			pixelsPerUnit = float(line[len(PIXELS_PER_UNIT_INDICATOR) :])
			break
	paperSprite.set_editor_property('pixels_per_unreal_unit', pixelsPerUnit)
	ASSET_REGISTRY.scan_files_synchronous([destinationPath])
	unreal.EditorAssetSubsystem().save_asset(destinationPath)
	paperSprite = unreal.load_object(None, destinationPath)
	paperSpriteActor.set_actor_scale3d(size)
	paperSpriteActor.render_component.set_editor_property('source_sprite', paperSprite)
	paperSpriteActor.set_mobility(unreal.ComponentMobility.MOVABLE)
	return paperSpriteActor

def MakeCameraActor (location : unreal.Vector, rotation : unreal.Rotator, size : unreal.Vector, horizontalFov : bool, fov : float, isOrthographic : bool, orthographicSize : float, nearClipPlane : float, farClipPlane : float):
	rotation.yaw = 90
	cameraActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.CameraActor.static_class(), location, rotation)
	if isOrthographic:
		cameraActor.camera_component.projection_mode = unreal.CameraProjectionMode.ORTHOGRAPHIC
	if not horizontalFov:
		cameraActor.camera_component.aspect_ratio_axis_constraint = unreal.AspectRatioAxisConstraint.ASPECT_RATIO_MAINTAIN_YFOV
	cameraActor.camera_component.field_of_view = fov
	cameraActor.camera_component.ortho_width = orthographicSize * 4
	cameraActor.camera_component.ortho_near_clip_plane = nearClipPlane
	cameraActor.camera_component.ortho_far_clip_plane = farClipPlane
	cameraActor.set_actor_scale3d(size)
	cameraActor.set_editor_property('auto_activate_for_player', unreal.AutoReceiveInput.PLAYER0)
	cameraActor.camera_component.set_mobility(unreal.ComponentMobility.MOVABLE)
	return cameraActor

def MakeLightActor (location : unreal.Vector, rotation : unreal.Rotator, size : unreal.Vector, type : int, intensity : float, color : unreal.LinearColor):
	lightActor = None
	if type == 0:
		lightActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight.static_class(), location, rotation)
	elif type == 1:
		lightActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight.static_class(), location, rotation)
	lightActor.light_component.set_intensity(intensity)
	lightActor.set_light_color(color)
	lightActor.set_actor_scale3d(size)
	lightActor.light_component.set_mobility(unreal.ComponentMobility.MOVABLE)
	return lightActor

def MakeScriptActor (location : unreal.Vector, rotation : unreal.Rotator, size : unreal.Vector, scriptAssetPath : str, parent : unreal.Actor = None):
	global blueprintAsset
	scriptAssetPath = CODE_PATH + scriptAssetPath[scriptAssetPath.rfind('/') :]
	scriptAssetPath = scriptAssetPath.replace('.cs', '.cpp')
	script = LoadScript(scriptAssetPath)
	blueprintFactory = unreal.BlueprintFactory()
	assetName = scriptAssetPath[scriptAssetPath.rfind('/') + 1 :].replace('.cpp', '')
	blueprintFactory.set_editor_property('parent_class', unreal.load_class(None, '/Script/' + UNREAL_PROJECT_NAME + '.' + assetName))
	assetName += '_Script'
	destinationPath = '/Game/' + assetName
	unreal.EditorAssetLibrary.delete_asset(destinationPath + '/' + assetName)
	scriptBlueprintAsset = ASSET_TOOLS.create_asset(assetName, destinationPath, None, blueprintFactory)
	destinationPath += '/' + assetName
	ASSET_REGISTRY.scan_files_synchronous([destinationPath])
	unreal.EditorAssetSubsystem().save_asset(destinationPath)
	blueprintActor = unreal.EditorLevelLibrary.spawn_actor_from_object(scriptBlueprintAsset, location, rotation)
	attachRule = unreal.AttachmentRule.KEEP_WORLD
	if parent != None:
		blueprintActor.attach_to_actor(parent, '', attachRule, attachRule, attachRule)
	if blueprintAsset != None:
		rootData = SUBOBJECT_DATA.k2_gather_subobject_data_for_blueprint(blueprintAsset)[0]
		assetName = assetName.replace('_Script', '')
		classType = unreal.load_class(None, '/Script/' + UNREAL_PROJECT_NAME + '.' + assetName)
		blueprintLibrary = unreal.SubobjectDataBlueprintFunctionLibrary()
		addSubobjectParameters = unreal.AddNewSubobjectParams(rootData, classType, blueprintAsset)
		subHandle, failReason = SUBOBJECT_DATA.add_new_subobject(addSubobjectParameters)
		if not failReason.is_empty():
			raise Exception('ERROR from SUBOBJECT_DATA.add_new_subobject: {failReason}')
		didAttach = SUBOBJECT_DATA.attach_subobject(rootData, subHandle)
		subData = blueprintLibrary.get_data(subHandle)
		subComponent = blueprintLibrary.get_object(subData)
		subComponent.set_editor_property('relative_location', location)
		unreal.EditorAssetSubsystem().save_asset(destinationPath)
	return blueprintActor

def LoadObject (assetPath : str) -> unreal.Object:
	lastIndexOfPeriod = assetPath.rfind('.')
	assetName = assetPath[assetPath.rfind('/') + 1 : lastIndexOfPeriod]
	destinationPath = '/Game/' + assetName
	importData = unreal.AutomatedAssetImportData()
	importData.filenames = [assetPath]
	importData.destination_path = destinationPath
	importData.replace_existing = True
	asset = ASSET_TOOLS.import_assets_automated(importData)[0]
	destinationPath += '/' + assetName
	ASSET_REGISTRY.scan_files_synchronous([destinationPath])
	unreal.EditorAssetSubsystem().save_asset(destinationPath)
	return asset

def LoadScript (assetPath : str) -> unreal.Object:
	lastIndexOfPeriod = assetPath.rfind('.')
	assetName = assetPath[assetPath.rfind('/') + 1 : lastIndexOfPeriod]
	destinationPath = '/Script/' + UNREAL_PROJECT_NAME + '.' + assetName
	return unreal.load_object(None, destinationPath)

def MakeLevelOrPrefab (sceneOrPrefabFileText : str):
	sceneOrPrefabFileLines = sceneOrPrefabFileText.split('\n')
	currentTypes = []
	currentType = ''
	transformsIdsDict = {}
	elementId = ''
	parent = ''
	localPosition = unreal.Vector()
	localRotation = unreal.Rotator()
	localSize = unreal.Vector()
	meshAssetPath = ''
	textureAssetPath = ''
	scriptsPaths = []
	prefabsPaths = []
	lightType = -1
	lightIntensity = -1
	horizontalFov = False
	fov = -1
	isOrthographic = False
	orthographicSize = -1
	nearClipPlane = -1
	farClipPlane = -1
	for i in range(len(sceneOrPrefabFileLines)):
		line = sceneOrPrefabFileLines[i]
		if i == len(sceneOrPrefabFileLines) - 1 or line.endswith(':'):
			if i == len(sceneOrPrefabFileLines) - 1 or line.startswith('GameObject') or line.startswith('SceneRoots'):
				actors = []
				components = []
				if 'Camera' in currentTypes:
					actors.append(MakeCameraActor(localPosition, localRotation, localSize, horizontalFov, fov, isOrthographic, orthographicSize, nearClipPlane, farClipPlane))
				if 'MeshRenderer' in currentTypes:
					actors.append(MakeStaticMeshActor(localPosition, localRotation, localSize, meshAssetPath))
				if 'Light' in currentTypes:
					actors.append(MakeLightActor(localPosition, localRotation, localSize, lightType, lightIntensity))
				if 'SpriteRenderer' in currentTypes:
					actors.append(MakePaperSpriteActor(localPosition, localRotation, localSize, textureAssetPath))
				if 'MonoBehaviour' in currentTypes:
					for scriptPath in scriptsPaths:
						if not scriptPath.endswith('/UniversalAdditionalCameraData.cs') and not scriptPath.endswith('/UniversalAdditionalLightData.cs'):
							scriptActor = MakeScriptActor(unreal.Vector(), unreal.Rotator(), unreal.Vector(1, 1, 1), scriptPath)
							attachRule = unreal.AttachmentRule.KEEP_WORLD
							for actor in actors:
								actor.attach_to_actor(scriptActor, '', attachRule, attachRule, attachRule)
							for component in components:
								component.attach_to(scriptActor.root_component, '', attachRule, attachRule, attachRule)
							actors = [ scriptActor ]
				if parent != '' and parent != '0' and parent in transformsIdsDict:
					attachRule = unreal.AttachmentRule.KEEP_WORLD
					for actor in actors:
						actor.attach_to_actor(transformsIdsDict[parent], '', attachRule, attachRule, attachRule)
				if len(actors) > 0:
					transformsIdsDict[elementId] = actors[-1]
				parent = ''
				currentTypes.clear()
				scriptsPaths.clear()
				prefabsPaths.clear()
			currentType = line[: len(line) - 1]
			currentTypes.append(currentType)
		elif line.startswith(GAME_OBJECT_ID_INDICATOR):
			elementId = line[len(GAME_OBJECT_ID_INDICATOR) + 1 :]
		elif line.startswith('  '):
			if currentType == 'MeshFilter':
				if line.startswith(MESH_INDICATOR):
					indexOfGuid = line.find(GUID_INDICATOR)
					meshAssetPath = fileGuidsDict[line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')]]
			elif currentType == 'GameObject':
				if line.startswith(ACTIVE_INDICATOR):
					pass
			elif currentType == 'Transform':
				if line.startswith(PARENT_INDICATOR):
					parent = line[len(PARENT_INDICATOR) : -1]
				elif line.startswith(LOCAL_POSITION_INDICATOR):
					indexOfComma = line.find(',')
					x = line[len(LOCAL_POSITION_INDICATOR) + 3 : indexOfComma]
					localPosition.x = -float(x)
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfY = line.find('y: ')
					y = line[indexOfY + 3 : indexOfComma]
					localPosition.z = float(y)
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfZ = line.find('z: ')
					z = line[indexOfZ + 3 : indexOfComma]
					localPosition.y = float(z)
				elif line.startswith(LOCAL_ROTATION_INDICATOR):
					localRotation = unreal.Quat()
					indexOfComma = line.find(',')
					x = line[len(LOCAL_ROTATION_INDICATOR) + 3 : indexOfComma]
					localRotation.x = -float(x)
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfY = line.find('y: ')
					y = line[indexOfY + 3 : indexOfComma]
					localRotation.z = float(y)
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfZ = line.find('z: ')
					z = line[indexOfZ + 3 : indexOfComma]
					localRotation.y = float(z)
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfW = line.find('w: ')
					w = line[indexOfW + 3 : indexOfComma]
					localRotation.w = float(w)
					localRotation = localRotation.rotator()
					localRotation.yaw += 180
				elif line.startswith(LOCAL_SCALE_INDICATOR):
					indexOfComma = line.find(',')
					x = line[len(LOCAL_SCALE_INDICATOR) + 3 : indexOfComma]
					localSize.x = -float(x)
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfY = line.find('y: ')
					y = line[indexOfY + 3 : indexOfComma]
					localSize.z = float(y)
					indexOfComma = line.find(',', indexOfComma + 1)
					indexOfZ = line.find('z: ')
					z = line[indexOfZ + 3 : indexOfComma]
					localSize.y = float(z)
			elif currentType == 'MonoBehaviour':
				if line.startswith(SCRIPT_INDICATOR):
					indexOfGuid = line.find(GUID_INDICATOR)
					scriptPath = fileGuidsDict.get(line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')], None)
					if scriptPath != None:
						scriptsPaths.append(scriptPath)
				# elif not line[2 :].startswith('m_'):
				# 	indexOfGuid = line.find(GUID_INDICATOR)
				# 	prefabPath = fileGuidsDict[line[indexOfGuid + len(GUID_INDICATOR) : line.rfind(',')]]
				# 	prefabsPaths.append(prefabPath)
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

data = open('/tmp/Unity2Many Data (UnityToUnreal)', 'rb').read().decode('utf-8').split('\n')
fromUnity = False
for arg in data:
	if arg.startswith(INPUT_PATH_INDICATOR):
		UNITY_PROJECT_PATH = arg[len(INPUT_PATH_INDICATOR) :]
		fromUnity = True
	elif arg.startswith(OUTPUT_PATH_INDICATOR):
		UNREAL_PROJECT_PATH = arg[len(OUTPUT_PATH_INDICATOR) :]
		UNREAL_PROJECT_NAME = UNREAL_PROJECT_PATH[UNREAL_PROJECT_PATH.rfind('/') + 1 :]
		CODE_PATH = UNREAL_PROJECT_PATH + '/Source/' + UNREAL_PROJECT_NAME
	elif arg.startswith(EXCLUDE_ITEM_INDICATOR):
		excludeItems.append(arg[len(EXCLUDE_ITEM_INDICATOR) + 1 :])

if fromUnity:
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
	prefabFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.prefab')
	for prefabFilePath in prefabFilesPaths:
		isExcluded = False
		for excludeItem in excludeItems:
			if excludeItem in prefabFilePath:
				isExcluded = True
				break
		if not isExcluded:
			prefabName = prefabFilePath[prefabFilePath.rfind('/') + 1 :]
			prefabName = prefabName.replace('.prefab', '')
			prefabName += '_Prefab'
			destinationPath = '/Game/' + prefabName
			unreal.EditorAssetLibrary.delete_asset(destinationPath)
			destinationPath += '/' + prefabName + '.' + prefabName
			blueprintFactory = unreal.BlueprintFactory()
			blueprintFactory.set_editor_property('parent_class', unreal.Actor)
			blueprintAsset = ASSET_TOOLS.create_asset(prefabName, destinationPath, None, blueprintFactory)
			ASSET_REGISTRY.scan_files_synchronous([destinationPath])
			unreal.EditorAssetSubsystem().save_asset(destinationPath)
			prefabFileText = open(prefabFilePath, 'rb').read().decode('utf-8')
			MakeLevelOrPrefab (prefabFileText)
	blueprintAsset = None
	sceneFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.unity')
	for sceneFilePath in sceneFilesPaths:
		isExcluded = False
		for excludeItem in excludeItems:
			if excludeItem in sceneFilePath:
				isExcluded = True
				break
		if not isExcluded:
			sceneName = sceneFilePath[sceneFilePath.rfind('/') + 1 :]
			sceneName = sceneName.replace('.unity', '')
			sceneName = '/Game/' + sceneName + '/' + sceneName
			unreal.EditorAssetLibrary.delete_asset(sceneName)
			LEVEL_EDITOR.new_level(sceneName)
			sceneFileText = open(sceneFilePath, 'rb').read().decode('utf-8')
			MakeLevelOrPrefab (sceneFileText)
else:
	data = open('/tmp/Unity2Many Data (BlenderToUnreal)', 'rb').read().decode('utf-8')
	lines = data.split('\n')
	UNREAL_PROJECT_PATH = lines[0]
	UNREAL_PROJECT_NAME = UNREAL_PROJECT_PATH[UNREAL_PROJECT_PATH.rfind('/') + 1 :]
	CODE_PATH = UNREAL_PROJECT_PATH + '/Source/' + UNREAL_PROJECT_NAME
	sceneName = lines[1].replace('.blend', '')
	sceneName = sceneName[sceneName.rfind('/') + 1 :]
	if sceneName == '':
		sceneName = 'Game'
	sceneName = '/Game/' + sceneName + '/' + sceneName
	unreal.EditorAssetLibrary.delete_asset(sceneName)
	LEVEL_EDITOR.new_level(sceneName)
	EDITOR.get_editor_world().get_world_settings().lightmass_settings.environment_color = unreal.Color(75, 75, 75, 0)
	stage = 0
	actorsDict = {}
	for line in lines:
		name = ''
		localPosition = unreal.Vector()
		localRotation = unreal.Quat()
		localSize = unreal.Vector()
		if line == 'Cameras' or line == 'Lights' or line == 'Meshes' or line == 'Scripts':
			stage += 1
		elif stage > 0:
			objectInfo = line.split('☣️')
			name = objectInfo[0]
			actors = actorsDict.get(name, [])
			localPositionInfo = objectInfo[1]
			indexOfComma = localPositionInfo.find(',')
			localPosition.x = -float(localPositionInfo[localPositionInfo.find('(') + 1 : indexOfComma])
			indexOfComma2 = localPositionInfo.find(',', indexOfComma + 1)
			localPosition.z = float(localPositionInfo[indexOfComma + 1 : indexOfComma2])
			localPosition.y = float(localPositionInfo[indexOfComma2 + 1 : localPositionInfo.find(')')])
			localRotationInfo = objectInfo[2]
			indexOfEquals = localRotationInfo.find('=')
			indexOfComma = localRotationInfo.find(',')
			localRotation.w = float(localRotationInfo[indexOfEquals + 1 : indexOfComma])
			indexOfEquals = localRotationInfo.find('=', indexOfEquals + 1)
			indexOfComma = localRotationInfo.find(',', indexOfComma + 1)
			localRotation.x = -float(localRotationInfo[indexOfEquals + 1 : indexOfComma])
			indexOfEquals = localRotationInfo.find('=', indexOfEquals + 1)
			indexOfComma = localRotationInfo.find(',', indexOfComma + 1)
			localRotation.z = float(localRotationInfo[indexOfEquals + 1 : indexOfComma])
			indexOfEquals = localRotationInfo.find('=', indexOfEquals + 1)
			localRotation.y = float(localRotationInfo[indexOfEquals + 1 : localRotationInfo.find(')')])
			localRotation = localRotation.rotator()
			localRotation.yaw += 180
			localSizeInfo = objectInfo[3]
			indexOfComma = localSizeInfo.find(',')
			localSize.x = -float(localSizeInfo[localSizeInfo.find('(') + 1 : indexOfComma])
			indexOfComma2 = localSizeInfo.find(',', indexOfComma + 1)
			localSize.z = float(localSizeInfo[indexOfComma + 1 : indexOfComma2])
			localSize.y = float(localSizeInfo[indexOfComma2 + 1 : localSizeInfo.find(')')])
			if stage == 1:
				horizontalFov = bool(objectInfo[4])
				fov = float(objectInfo[5])
				isOrthographic = bool(objectInfo[6])
				orthographicSize = float(objectInfo[7])
				nearClipPlane = float(objectInfo[8])
				farClipPlane = float(objectInfo[9])
				actors.append(MakeCameraActor(localPosition, localRotation, localSize, horizontalFov, fov, isOrthographic, orthographicSize, nearClipPlane, farClipPlane))
				actorsDict[name] = actors
			elif stage == 2:
				lightType = int(objectInfo[4])
				intensity = float(objectInfo[5])
				colorInfo = objectInfo[6]
				indexOfEquals = colorInfo.find('=')
				indexOfComma = colorInfo.find(',')
				color = unreal.LinearColor()
				color.r = float(colorInfo[indexOfEquals + 1 : indexOfComma])
				indexOfEquals = colorInfo.find('=', indexOfEquals + 1)
				indexOfComma = colorInfo.find(',', indexOfComma + 1)
				color.g = float(colorInfo[indexOfEquals + 1 : indexOfComma])
				indexOfEquals = colorInfo.find('=', indexOfEquals + 1)
				color.b = float(colorInfo[indexOfEquals + 1 : colorInfo.find(')')])
				actors.append(MakeLightActor(localPosition, localRotation, localSize, lightType, intensity, color))
				actorsDict[name] = actors
			elif stage == 3:
				actors.append(MakeStaticMeshActor(localPosition, localRotation, localSize, '/tmp/' + name + '.fbx'))
				actorsDict[name] = actors
			elif stage == 4:
				scripts = objectInfo[4 :]
				for script in scripts:
					if not script.endswith('.cs'):
						script += '.cs'
					codeFilePath = '/tmp/Unity2Many (Unreal Scripts)/' + script
					ConvertCSFileToCPP (codeFilePath)
					scriptActor = MakeScriptActor(unreal.Vector(), unreal.Rotator(), unreal.Vector(1, 1, 1), codeFilePath)
					for actor in actorsDict[name]:
						scriptActor.set_editor_property('root_component', actor.get_editor_property('root_component'))
LEVEL_EDITOR.save_current_level()