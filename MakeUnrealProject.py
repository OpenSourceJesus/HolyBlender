import unreal, os, sys
sys.path.append(os.path.expanduser('~/Unity2Many'))
from StringExtensions import *
from SystemExtensions import *

INPUT_PATH_INDICATOR = 'input='
OUTPUT_PATH_INDICATOR = 'output='
YAML_ELEMENT_ID_INDICATOR = '--- !u!'
GUID_INDICATOR = 'guid: '
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
CODE_PATH = UNREAL_PROJECT_PATH + ''
LEVEL_EDITOR = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
ASSET_TOOLS = unreal.AssetToolsHelpers().get_asset_tools()
ASSET_REGISTRY = assetRegistry = unreal.AssetRegistryHelpers.get_asset_registry()
EDITOR_ASSET = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
INTERCHANGE_MANAGER = unreal.InterchangeManager.get_interchange_manager_scripted()
EDITOR = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
EDITOR_UTILITY = unreal.get_editor_subsystem(unreal.EditorUtilitySubsystem)
SUBOBJECT_DATA = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
EXCLUDE_ITEM_INDICATOR = 'exclude='
excludeItems = []
blueprintAsset = None

data = open('/tmp/Unity2Many Data (UnityToUnreal)', 'rb').read().decode('utf-8').split('\n')
for arg in data:
	if arg.startswith(INPUT_PATH_INDICATOR):
		UNITY_PROJECT_PATH = arg[len(INPUT_PATH_INDICATOR) :]
	elif arg.startswith(OUTPUT_PATH_INDICATOR):
		UNREAL_PROJECT_PATH = arg[len(OUTPUT_PATH_INDICATOR) :]
		CODE_PATH = UNREAL_PROJECT_PATH + '/Source/' + UNREAL_PROJECT_PATH[UNREAL_PROJECT_PATH.rfind('/') + 1 :]
	elif arg.startswith(EXCLUDE_ITEM_INDICATOR):
		excludeItems.append(arg[len(EXCLUDE_ITEM_INDICATOR) + 1 :])
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

def MakeStaticMeshActor (location : unreal.Vector, rotation : unreal.Rotator, size : unreal.Vector, meshAssetPath : str):
	projectFilePath = UNREAL_PROJECT_PATH + '/Content' + meshAssetPath[meshAssetPath.rfind('/') :]
	os.system('cp \'' + meshAssetPath + '\' \'' + projectFilePath + '\'')
	staticMesh = LoadObject(meshAssetPath)
	staticMeshActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor.static_class(), location, rotation)
	staticMeshActor.static_mesh_component.set_static_mesh(staticMesh)
	staticMeshActor.set_actor_scale3d(size)
	LEVEL_EDITOR.save_current_level()
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
	LEVEL_EDITOR.save_current_level()
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
	LEVEL_EDITOR.save_current_level()
	return cameraActor

def MakeLightActor (location : unreal.Vector, rotation : unreal.Rotator, size : unreal.Vector, type : int, intensity : float):
	lightActor = None
	if type == 1:
		lightActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.DirectionalLight.static_class(), unreal.Vector(), unreal.Rotator())
	lightActor.light_component.set_intensity(intensity)
	lightActor.set_actor_scale3d(size)
	LEVEL_EDITOR.save_current_level()
	return lightActor

def MakeScriptActor (location : unreal.Vector, rotation : unreal.Rotator, size : unreal.Vector, scriptAssetPath : str, parent : unreal.Actor = None):
	global blueprintAsset
	scriptAssetPath = CODE_PATH + scriptAssetPath[scriptAssetPath.rfind('/') :]
	scriptAssetPath = scriptAssetPath.replace('.cs', '.cpp')
	script = LoadScript(scriptAssetPath)
	blueprintFactory = unreal.BlueprintFactory()
	assetName = scriptAssetPath[scriptAssetPath.rfind('/') + 1 :].replace('.cpp', '')
	blueprintFactory.set_editor_property('parent_class', unreal.load_class(None, '/Script/BareUEProject.' + assetName))
	assetName += '_Blueprint'
	destinationPath = '/Game/' + assetName
	unreal.EditorAssetLibrary.delete_asset(destinationPath + '/' + assetName)
	blueprintAsset = ASSET_TOOLS.create_asset(assetName, destinationPath, None, blueprintFactory)
	destinationPath += '/' + assetName
	ASSET_REGISTRY.scan_files_synchronous([destinationPath])
	unreal.EditorAssetSubsystem().save_asset(destinationPath)
	# rootData = SUBOBJECT_DATA.k2_gather_subobject_data_for_blueprint(blueprintAsset)[0]
	# classType = unreal.StaticMeshComponent
	# subHandle, failReason = SUBOBJECT_DATA.add_new_subobject(unreal.AddNewSubobjectParams(rootData, classType, blueprintAsset))
	# SUBOBJECT_DATA.rename_subobject(subHandle, unreal.Text('Test'))
	# blueprintLibrary = unreal.SubobjectDataBlueprintFunctionLibrary()
	# classType = unreal.StaticMeshComponent
	# params = unreal.AddNewSubobjectParams(rootData, classType, blueprintAsset)
	# subHandle, failReason = SUBOBJECT_DATA.add_new_subobject(params)
	# if not failReason.is_empty():
	# 	raise Exception('ERROR from SUBOBJECT_DATA.add_new_subobject: {failReason}')
	# SUBOBJECT_DATA.attach_subobject(rootData, subHandle)
	# subData = blueprintLibrary.get_data(subHandle)
	# subComponent = blueprintLibrary.get_object(subData)
	# assetPath = '/Game/'
	# asset = unreal.EditorAssetLibrary.load_asset(assetPath)
	# if asset is not None:
	# 	subComponent.set_editor_property('static_mesh', asset)
	# location, isValid = unreal.StringLibrary.conv_string_to_vector('(X=-208.000000,Y=-1877.000000,Z=662.000000)')
	# subComponent.set_editor_property('relative_location', location)
	blueprint = unreal.load_object(None, destinationPath)
	blueprintActor = unreal.EditorLevelLibrary.spawn_actor_from_object(blueprint, location, rotation)
	attachRule = unreal.AttachmentRule.KEEP_WORLD
	if parent != None:
		blueprintActor.attach_to_actor(parent, '', attachRule, attachRule, attachRule)
	else:
		staticMeshActor = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.StaticMeshActor.static_class(), location, rotation)
		blueprintActor.set_editor_property('root_component', staticMeshActor.static_mesh_component)
		staticMeshActor.set_actor_scale3d(size)
	LEVEL_EDITOR.save_current_level()
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
	destinationPath = '/Script/BareUEProject.' + assetName
	return unreal.load_object(None, destinationPath)

def MakeLevel (sceneFileText : str):
	sceneFileLines = sceneFileText.split('\n')
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
	for i in range(len(sceneFileLines)):
		line = sceneFileLines[i]
		if i == len(sceneFileLines) - 1 or line.endswith(':'):
			if i == len(sceneFileLines) - 1 or line.startswith('GameObject') or line.startswith('SceneRoots'):
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
		prefabName = '/Game/' + prefabName + '/' + prefabName
		unreal.EditorAssetLibrary.delete_asset(prefabName)
		LEVEL_EDITOR.new_level(prefabName)
		prefabFileText = open(prefabFilePath, 'rb').read().decode('utf-8')
		MakeLevel (prefabFileText)
sceneFilesPaths = GetAllFilePathsOfType(UNITY_PROJECT_PATH, '.unity')
for sceneFilePath in sceneFilesPaths:
	sceneName = sceneFilePath[sceneFilePath.rfind('/') + 1 :]
	sceneName = sceneName.replace('.unity', '')
	sceneName = '/Game/' + sceneName + '/' + sceneName
	unreal.EditorAssetLibrary.delete_asset(sceneName)
	LEVEL_EDITOR.new_level(sceneName)
	sceneFileText = open(sceneFilePath, 'rb').read().decode('utf-8')
	MakeLevel (sceneFileText)