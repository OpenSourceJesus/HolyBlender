import bpy, subprocess, os, sys, webbrowser, hashlib#, blf
# from random import random

sys.path.append(os.path.expanduser('~/Unity2Many'))
from SystemExtensions import *
from StringExtensions import *
from CollectionExtensions import *

bl_info = {
	'name': 'Blender Plugin',
	'blender': (2, 80, 0),
	'category': 'System',
}
REPLACE_INDICATOR = 'ꗈ'
GAME_OBJECT_TEMPLATE = '''--- !u!1 &ꗈ0
GameObject:
	m_ObjectHideFlags: 0
	m_CorrespondingSourceObject: {fileID: 0}
	m_PrefabInstance: {fileID: 0}
	m_PrefabAsset: {fileID: 0}
	serializedVersion: 6
	m_Component:
	- component: {fileID: ꗈ1}
ꗈ2
	m_Layer: 0
	m_Name: ꗈ3
	m_TagString: Untagged
	m_Icon: {fileID: 0}
	m_NavMeshLayer: 0
	m_StaticEditorFlags: 0
	m_IsActive: 1'''
TRANSFORM_TEMPLATE = '''--- !u!4 &ꗈ0
Transform:
	m_ObjectHideFlags: 0
	m_CorrespondingSourceObject: {fileID: 0}
	m_PrefabInstance: {fileID: 0}
	m_PrefabAsset: {fileID: 0}
	m_GameObject: {fileID: ꗈ1}
	serializedVersion: 2
	m_LocalRotation: {x: ꗈ2, y: ꗈ3, z: ꗈ4, w: ꗈ5}
	m_LocalPosition: {x: ꗈ6, y: ꗈ7, z: ꗈ8}
	m_LocalScale: {x: ꗈ9, y: ꗈ10, z: ꗈ11}
	m_ConstrainProportionsScale: 0
	m_Children: []
	m_Father: {fileID: 0}
	m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}'''
LIGHT_TEMPLATE = '''--- !u!108 &ꗈ0
Light:
	m_ObjectHideFlags: 0
	m_CorrespondingSourceObject: {fileID: 0}
	m_PrefabInstance: {fileID: 0}
	m_PrefabAsset: {fileID: 0}
	m_GameObject: {fileID: ꗈ1}
	m_Enabled: 1
	serializedVersion: 11
	m_Type: ꗈ2
	m_Color: {r: ꗈ3, g: ꗈ4, b: ꗈ5, a: 1}
	m_Intensity: ꗈ6
	m_Range: ꗈ7
	m_SpotAngle: ꗈ8
	m_InnerSpotAngle: ꗈ9
	m_CookieSize: 10
	m_Shadows:
	m_Type: 0
	m_Resolution: -1
	m_CustomResolution: -1
	m_Strength: 1
	m_Bias: 0.05
	m_NormalBias: 0.4
	m_NearPlane: 0.2
	m_CullingMatrixOverride:
		e00: 1
		e01: 0
		e02: 0
		e03: 0
		e10: 0
		e11: 1
		e12: 0
		e13: 0
		e20: 0
		e21: 0
		e22: 1
		e23: 0
		e30: 0
		e31: 0
		e32: 0
		e33: 1
	m_UseCullingMatrixOverride: 0
	m_Cookie: {fileID: 0}
	m_DrawHalo: 0
	m_Flare: {fileID: 0}
	m_RenderMode: 0
	m_CullingMask:
	serializedVersion: 2
	m_Bits: 4294967295
	m_RenderingLayerMask: 1
	m_Lightmapping: 4
	m_LightShadowCasterMode: 0
	m_AreaSize: {x: 1, y: 1}
	m_BounceIntensity: 1
	m_ColorTemperature: 6570
	m_UseColorTemperature: 0
	m_BoundingSphereOverride: {x: 0, y: 0, z: 0, w: 0}
	m_UseBoundingSphereOverride: 0
	m_UseViewFrustumForShadowCasterCull: 1
	m_ShadowRadius: 0
	m_ShadowAngle: 0'''
SCRIPT_TEMPLATE = '''--- !u!114 &ꗈ0
MonoBehaviour:
	m_ObjectHideFlags: 0
	m_CorrespondingSourceObject: {fileID: 0}
	m_PrefabInstance: {fileID: 0}
	m_PrefabAsset: {fileID: 0}
	m_GameObject: {fileID: ꗈ1}
	m_Enabled: 1
	m_EditorHideFlags: 0
	m_Script: {fileID: 11500000, guid: ꗈ2, type: 3}
	m_Name: 
	m_EditorClassIdentifier: 
	m_Version: 3
	m_UsePipelineSettings: 1
	m_AdditionalLightsShadowResolutionTier: 2
	m_LightLayerMask: 1
	m_RenderingLayers: 1
	m_CustomShadowLayers: 0
	m_ShadowLayerMask: 1
	m_ShadowRenderingLayers: 1
	m_LightCookieSize: {x: 1, y: 1}
	m_LightCookieOffset: {x: 0, y: 0}
	m_SoftShadowQuality: 0'''
SCRIPT_META_TEMPLATE = '''fileFormatVersion: 2
guid: '''
MATERIAL_META_TEMPLATE = '''fileFormatVersion: 2
guid: ꗈ
NativeFormatImporter:
	externalObjects: {}
	mainObjectFileID: 2100000
	userData: 
	assetBundleName: 
	assetBundleVariant: '''
MESH_META_TEMPLATE = '''fileFormatVersion: 2
guid: ꗈ
ModelImporter:
	serializedVersion: 22200
	internalIDToNameTable: []
	externalObjects: {}
	materials:
		materialImportMode: 2
		materialName: 0
		materialSearch: 1
		materialLocation: 1
	animations:
		legacyGenerateAnimations: 4
		bakeSimulation: 0
		resampleCurves: 1
		optimizeGameObjects: 0
		removeConstantScaleCurves: 0
		motionNodeName: 
		animationImportErrors: 
		animationImportWarnings: 
		animationRetargetingWarnings: 
		animationDoRetargetingWarnings: 0
		importAnimatedCustomProperties: 0
		importConstraints: 0
		animationCompression: 1
		animationRotationError: 0.5
		animationPositionError: 0.5
		animationScaleError: 0.5
		animationWrapMode: 0
		extraExposedTransformPaths: []
		extraUserProperties: []
		clipAnimations: []
		isReadable: 0
	meshes:
		lODScreenPercentages: []
		globalScale: 1
		meshCompression: 0
		addColliders: 0
		useSRGBMaterialColor: 1
		sortHierarchyByName: 1
		importPhysicalCameras: 1
		importVisibility: 1
		importBlendShapes: 1
		importCameras: 1
		importLights: 1
		nodeNameCollisionStrategy: 1
		fileIdsGeneration: 2
		swapUVChannels: 0
		generateSecondaryUV: 0
		useFileUnits: 1
		keepQuads: 0
		weldVertices: 1
		bakeAxisConversion: 0
		preserveHierarchy: 0
		skinWeightsMode: 0
		maxBonesPerVertex: 4
		minBoneWeight: 0.001
		optimizeBones: 1
		meshOptimizationFlags: -1
		indexFormat: 0
		secondaryUVAngleDistortion: 8
		secondaryUVAreaDistortion: 15.000001
		secondaryUVHardAngle: 88
		secondaryUVMarginMethod: 1
		secondaryUVMinLightmapResolution: 40
		secondaryUVMinObjectScale: 1
		secondaryUVPackMargin: 4
		useFileScale: 1
		strictVertexDataChecks: 0
	tangentSpace:
		normalSmoothAngle: 60
		normalImportMode: 0
		tangentImportMode: 3
		normalCalculationMode: 4
		legacyComputeAllNormalsFromSmoothingGroupsWhenMeshHasBlendShapes: 0
		blendShapeNormalImportMode: 1
		normalSmoothingSource: 0
	referencedClips: []
	importAnimation: 1
	humanDescription:
		serializedVersion: 3
		human: []
		skeleton: []
		armTwist: 0.5
		foreArmTwist: 0.5
		upperLegTwist: 0.5
		legTwist: 0.5
		armStretch: 0.05
		legStretch: 0.05
		feetSpacing: 0
		globalScale: 1
		rootMotionBoneName: 
		hasTranslationDoF: 0
		hasExtraRoot: 0
		skeletonHasParents: 1
	lastHumanDescriptionAvatarSource: {instanceID: 0}
	autoGenerateAvatarMappingIfUnspecified: 1
	animationType: 2
	humanoidOversampling: 1
	avatarSetup: 0
	addHumanoidExtraRootOnlyWhenUsingAvatar: 1
	importBlendShapeDeformPercent: 1
	remapMaterialsIfMaterialImportModeIsNone: 0
	additionalBone: 0
	userData: 
	assetBundleName: 
	assetBundleVariant: '''
MESH_FILTER_TEMPLATE = '''--- !u!33 &ꗈ0
MeshFilter:
	m_ObjectHideFlags: 0
	m_CorrespondingSourceObject: {fileID: 0}
	m_PrefabInstance: {fileID: 0}
	m_PrefabAsset: {fileID: 0}
	m_GameObject: {fileID: ꗈ1}
	m_Mesh: {fileID: ꗈ2, guid: ꗈ3, type: 3}'''
MESH_RENDERER_TEMPLATE = '''--- !u!23 &ꗈ0
MeshRenderer:
	m_ObjectHideFlags: 0
	m_CorrespondingSourceObject: {fileID: 0}
	m_PrefabInstance: {fileID: 0}
	m_PrefabAsset: {fileID: 0}
	m_GameObject: {fileID: ꗈ1}
	m_Enabled: 1
	m_CastShadows: 1
	m_ReceiveShadows: 1
	m_DynamicOccludee: 1
	m_StaticShadowCaster: 0
	m_MotionVectors: 1
	m_LightProbeUsage: 1
	m_ReflectionProbeUsage: 1
	m_RayTracingMode: 2
	m_RayTraceProcedural: 0
	m_RayTracingAccelStructBuildFlagsOverride: 0
	m_RayTracingAccelStructBuildFlags: 1
	m_RenderingLayerMask: 1
	m_RendererPriority: 0
	m_Materials:
ꗈ2
	m_StaticBatchInfo:
	firstSubMesh: 0
	subMeshCount: 0
	m_StaticBatchRoot: {fileID: 0}
	m_ProbeAnchor: {fileID: 0}
	m_LightProbeVolumeOverride: {fileID: 0}
	m_ScaleInLightmap: 1
	m_ReceiveGI: 1
	m_PreserveUVs: 0
	m_IgnoreNormalsForChartDetection: 0
	m_ImportantGI: 0
	m_StitchLightmapSeams: 1
	m_SelectedEditorRenderState: 3
	m_MinimumChartSize: 4
	m_AutoUVMaxDistance: 0.5
	m_AutoUVMaxAngle: 89
	m_LightmapParameters: {fileID: 0}
	m_SortingLayerID: 0
	m_SortingLayer: 0
	m_SortingOrder: 0
	m_AdditionalVertexStreams: {fileID: 0}'''
CAMERA_TEMPLATE = '''--- !u!20 &ꗈ0
Camera:
	m_ObjectHideFlags: 0
	m_CorrespondingSourceObject: {fileID: 0}
	m_PrefabInstance: {fileID: 0}
	m_PrefabAsset: {fileID: 0}
	m_GameObject: {fileID: ꗈ1}
	m_Enabled: 1
	serializedVersion: 2
	m_ClearFlags: 1
	m_BackGroundColor: {r: 0.19215687, g: 0.3019608, b: 0.4745098, a: 0}
	m_projectionMatrixMode: 1
	m_GateFitMode: 2
	m_FOVAxisMode: ꗈ2
	m_Iso: 200
	m_ShutterSpeed: 0.005
	m_Aperture: 16
	m_FocusDistance: 10
	m_FocalLength: 50
	m_BladeCount: 5
	m_Curvature: {x: 2, y: 11}
	m_BarrelClipping: 0.25
	m_Anamorphism: 0
	m_SensorSize: {x: 36, y: 24}
	m_LensShift: {x: 0, y: 0}
	m_NormalizedViewPortRect:
	serializedVersion: 2
	x: 0
	y: 0
	width: 1
	height: 1
	near clip plane: ꗈ3
	far clip plane: ꗈ4
	field of view: ꗈ5
	orthographic: ꗈ6
	orthographic size: ꗈ7
	m_Depth: 0
	m_CullingMask:
	serializedVersion: 2
	m_Bits: 4294967295
	m_RenderingPath: -1
	m_TargetTexture: {fileID: 0}
	m_TargetDisplay: 0
	m_TargetEye: 3
	m_HDR: 1
	m_AllowMSAA: 1
	m_AllowDynamicResolution: 0
	m_ForceIntoRT: 0
	m_OcclusionCulling: 1
	m_StereoConvergence: 10
	m_StereoSeparation: 0.022'''
GET_UNITY_PROJECT_INFO_SCRIPT = '''using System;
using System.IO;
using UnityEngine;
using UnityEditor;
using Object = UnityEngine.Object;

public class GetUnityProjectInfo : MonoBehaviour
{
	public static void Do ()
	{
		string[] args = Environment.GetCommandLineArgs();
		string outputText = "";
		string[] filePaths = SystemExtensions.GetAllFilePathsInFolder(args[args.Length - 1], ".fbx");
		foreach (string filePath in filePaths)
		{
			int indexOfAssets = filePath.IndexOf("Assets");
			string relativeFilePath = filePath.Substring(indexOfAssets);
			Object[] objects = AssetDatabase.LoadAllAssetsAtPath(relativeFilePath);
			foreach (Object obj in objects)
			{
				if (obj.GetType() == typeof(Mesh))
				{
					string guid;
					long fileId;
					if (AssetDatabase.TryGetGUIDAndLocalFileIdentifier(obj, out guid, out fileId))
						outputText += '-' + filePath + ' ' + fileId + ' ' + guid + ',';
				}
			}
		}
		filePaths = SystemExtensions.GetAllFilePathsInFolder(args[args.Length - 1], ".mat");
		foreach (string filePath in filePaths)
		{
			int indexOfAssets = filePath.IndexOf("Assets");
			string relativeFilePath = filePath.Substring(indexOfAssets);
			Object[] objects = AssetDatabase.LoadAllAssetsAtPath(relativeFilePath);
			foreach (Object obj in objects)
			{
				if (obj.GetType() == typeof(Material))
				{
					string guid;
					long fileId;
					if (AssetDatabase.TryGetGUIDAndLocalFileIdentifier(obj, out guid, out fileId))
						outputText += '-' + filePath + ' ' + fileId + ' ' + guid + ',';
				}
			}
		}
		File.WriteAllText("/tmp/Unity2Many Data (BlenderToUnity)", outputText);
	}
}'''
EXAMPLES_DICT = {
	'Hello World' : '''using UnityEngine;

public class HelloWorld : MonoBehaviour
{
	void Start ()
	{
		print("Hello World!");
	}
}''',
	'Rotate': '''using UnityEngine;

public class Rotate : MonoBehaviour
{
	public float rotateSpeed = 50.0f;

	void Update ()
	{
		transform.eulerAngles += Vector3.up * rotateSpeed * Time.deltaTime;
	}
}''',
	'Grow And Shrink': '''using UnityEngine;

public class GrowAndShrink : MonoBehaviour
{
	public float maxSize = 5.0f; 
	public float minSize = 0.2f;
	public float speed = 0.375f;

	void Update ()
	{
		transform.localScale = Vector3.one * (Mathf.Abs(Mathf.Sin(speed * Time.time)) * (maxSize - minSize) + minSize);
	}
}''',
	'Keyboard And Mouse Controls' : '''using UnityEngine;
using UnityEngine.InputSystem;

public class WASDAndMouseControls : MonoBehaviour
{
	public float moveSpeed = 5.0f;

	void Update ()
	{
		Vector3 move = Vector3.zero;
		if (Keyboard.current.aKey.isPressed)
			move.x -= 1.0f;
		if (Keyboard.current.dKey.isPressed)
			move.x += 1.0f;
		if (Keyboard.current.sKey.isPressed)
			move.y -= 1.0f;
		if (Keyboard.current.wKey.isPressed)
			move.y += 1.0f;
		move.Normalize();
		transform.position += move * moveSpeed * Time.deltaTime;
    	Vector3 mousePosition = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
		transform.up = mousePosition - transform.position;
	}
}''',
	'First Person Controls' : '''using UnityEngine;
using UnityEngine.InputSystem;

public class FirstPersonControls : MonoBehaviour
{
	public float moveSpeed = 5.0f;
	public float lookSpeed = 50.0f;
	Vector2 previousMousePosition;

	void Update ()
	{
		Vector3 move = Vector3.zero;
		if (Keyboard.current.aKey.isPressed)
			move.x -= 1.0f;
		if (Keyboard.current.dKey.isPressed)
			move.x += 1.0f;
		if (Keyboard.current.sKey.isPressed)
			move.y -= 1.0f;
		if (Keyboard.current.wKey.isPressed)
			move.y += 1.0f;
		move.Normalize();
		transform.position += move * moveSpeed * Time.deltaTime;
    	Vector2 mousePosition = Mouse.current.position.ReadValue();
    	Vector2 look = (mousePosition - previousMousePosition) * lookSpeed;
    	transform.Rotate(new Vector3(look.y, look.x));
    	previousMousePosition = mousePosition;
	}
}'''
}
MATERIAL_TEMPLATE = '    - {fileID: ꗈ0, guid: ꗈ1, type: 2}'
COMPONENT_TEMPLATE = '    - component: {fileID: ꗈ}'
SCENE_ROOT_TEMPLATE = '  - {fileID: ꗈ}'
WATTS_TO_CANDELAS = 0.001341022
PI = 3.141592653589793
TEMPLATES_PATH = os.path.expanduser('~/Unity2Many/Templates')
TEMPLATE_REGISTRY_PATH = TEMPLATES_PATH + '/registry.json'
REGISTRY_PATH = '/tmp/registry.json'
unrealCodePath = ''
unrealCodePathSuffix = '/Source/'
excludeItems = [ '/Library' ]
lastId = 5
operatorContext = None
currentTextBlock = None
mainClassNames = []
attachScriptDropdownOptions = []
attachedScriptsDict = {}
detachScriptDropdownOptions = []
previousRunningScripts = []
textBlocksTextsDict = {}
previousTextBlocksTextsDict = {}

class ExamplesOperator (bpy.types.Operator):
	bl_idname = 'u2m.show_template'
	bl_label = 'Add or Remove'
	template : bpy.props.StringProperty(default = '')

	def invoke (self, context, event):
		if context.edit_text != None:
			context.edit_text.from_string(EXAMPLES_DICT[self.template])
		return {'FINISHED'}

class ExamplesMenu (bpy.types.Menu):
	bl_idname = 'TEXT_MT_u2m_menu'
	bl_label = 'Unity2Many Templates'

	def draw (self, context):
		layout = self.layout
		for name in EXAMPLES_DICT:
			op = layout.operator('u2m.show_template', text=name)
			op.template = name

class AttachedObjectsMenu (bpy.types.Menu):
	bl_label = 'Unity2Many Attached Objects'
	bl_idname = 'TEXT_MT_u2m_menu_obj'

	def draw (self, context):
		layout = self.layout
		if not context.edit_text:
			layout.label(text='No text block')
			return
		objs = []
		for obj in bpy.data.objects:
			attachedScripts = attachedScriptsDict.get(obj, [])
			if context.edit_text.name in attachedScripts:
				objs.append(obj)
		if objs:
			for obj in objs:
				layout.label(text=obj.name)
		else:
			layout.label(text='Script not attached to any objects')

class TEXT_EDITOR_OT_UnrealExportButton (bpy.types.Operator):
	bl_idname = 'unreal.export'
	bl_label = 'Export To Unreal'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		global unrealCodePath
		global unrealCodePathSuffix
		BuildTool ('UnityToUnreal')
		unrealExportPath = os.path.expanduser(context.scene.world.unrealExportPath)
		importPath = os.path.expanduser(context.scene.world.unity_project_import_path)
		if importPath != '':
			command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToUnreal.py'), 'input=' + importPath, 'output=' + unrealExportPath, 'exclude=/Library' ]
			print(command)

			subprocess.check_call(command)

		else:
			unrealCodePath = unrealExportPath
			unrealProjectName = unrealExportPath[unrealExportPath.rfind('/') + 1 :]
			unrealCodePathSuffix = '/Source/' + unrealProjectName
			unrealCodePath += unrealCodePathSuffix
			data = unrealExportPath + '\n' + bpy.data.filepath + '\nCameras'
			for camera in bpy.data.cameras:
				data += '\n' + GetCameraData(camera)
				print('YA' + 'Y' + camera.name)
			data += '\nLights'
			for light in bpy.data.lights:
				data += '\n' + GetLightData(light)
				print('YA' + 'Y' + light.name)
			data += '\nMeshes'
			for obj in bpy.context.scene.objects:
				if obj.type == 'MESH':
					ExportMesh (obj)
					data += '\n' + GetBasicObjectData(obj)
					print('YA' + 'Y' + obj.name)
			MakeFolderForFile ('/tmp/Unity2Many (Unreal Scripts)/')
			data += '\nScripts'
			for obj in attachedScriptsDict:
				if len(attachedScriptsDict[obj]) > 0:
					data += '\n' + GetBasicObjectData(obj) + '☣️' + '☣️'.join(attachedScriptsDict[obj])
					for script in attachedScriptsDict[obj]:
						for textBlock in bpy.data.texts:
							if textBlock.name == script:
								if not script.endswith('.h') and not script.endswith('.cpp') and not script.endswith('.cs'):
									script += '.cs'
								open('/tmp/Unity2Many (Unreal Scripts)/' + script, 'wb').write(textBlock.as_string().encode('utf-8'))
								break
			data += '\nPrefabs'
			for scene in bpy.data.scenes:
				data += '\n' + scene.name + '\nCameras'
				for obj in scene.collection.objects:
					if obj.type == 'CAMERA':
						data += '\n' + GetCameraData(obj)
						print('YA' + 'Y' + obj.name)
				data += '\nLights'
				for obj in scene.collection.objects:
					if obj.type == 'LIGHT':
						data += '\n' + GetLightData(obj)
						print('YA' + 'Y' + obj.name)
				data += '\nMeshes'
				for obj in scene.collection.objects:
					if obj.type == 'MESH':
						ExportMesh (obj)
						data += '\n' + GetBasicObjectData(obj)
						print('YA' + 'Y' + obj.name)
			open('/tmp/Unity2Many Data (BlenderToUnreal)', 'wb').write(data.encode('utf-8'))
			projectFilePath = unrealExportPath + '/' + unrealProjectName + '.uproject'
			if not os.path.isdir(unrealExportPath):
				MakeFolderForFile (unrealExportPath + '/')
				bareProjectPath = os.path.expanduser('~/Unity2Many/BareUEProject')
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
				command = command.replace('dotnet', '/home/gilead/Downloads/dotnet-sdk-6.0.423-linux-x64/dotnet')
			print(command)

			os.system(command)

			data = ''
			open('/tmp/Unity2Many Data (UnityToUnreal)', 'wb').write(data.encode('utf-8'))
			UNREAL_COMMAND_PATH = os.path.expanduser('~/UnrealEngine/Engine/Binaries/Linux/UnrealEditor-Cmd')
			command = UNREAL_COMMAND_PATH + ' ' + projectFilePath + ' -nullrhi -ExecutePythonScript=' + os.path.expanduser('~/Unity2Many/MakeUnrealProject.py')
			print(command)

			os.system(command)

			command = UNREAL_COMMAND_PATH + ' ' + projectFilePath + ' -buildlighting'
			print(command)

			os.system(command)

class TEXT_EDITOR_OT_BevyExportButton (bpy.types.Operator):
	bl_idname = 'bevy.export'
	bl_label = 'Export To Bevy'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		BuildTool ('UnityToBevy')
		bevyExportPath = os.path.expanduser(context.scene.world.bevy_project_path)
		if not os.path.isdir(bevyExportPath):
			MakeFolderForFile (bevyExportPath + '/')
		importPath = os.path.expanduser(context.scene.world.unity_project_import_path)
		if importPath != '':
			command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToBevy.py'), 'input=' + importPath, 'output=' + bevyExportPath, 'exclude=/Library', 'webgl' ]
			print(command)

			subprocess.check_call(command)

		else:
			data = bevyExportPath
			for obj in attachedScriptsDict:
				data += '\n' + obj.name + '☢️' + '☣️'.join(attachedScriptsDict[obj])
			open('/tmp/Unity2Many Data (BlenderToBevy)', 'wb').write(data.encode('utf-8'))
			import MakeBevyBlenderApp as makeBevyBlenderApp
			makeBevyBlenderApp.Do ()
			# webbrowser.open('http://localhost:1334')

class TEXT_EDITOR_OT_UnityExportButton (bpy.types.Operator):
	bl_idname = 'unity.export'
	bl_label = 'Export To Unity'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		global lastId
		projectExportPath = os.path.expanduser(context.scene.world.unity_project_export_path)
		if not os.path.isdir(projectExportPath):
			os.mkdir(projectExportPath)
		for textBlock in bpy.data.texts:
			script = textBlock.name
			if not textBlock.name.endswith('.cs'):
				script += '.cs'
			text = textBlock.as_string()
			fileExportPath = projectExportPath + '/Assets/Standard Assets/Scripts/' + script
			MakeFolderForFile (fileExportPath)
			open(fileExportPath, 'wb').write(text.encode('utf-8'))
		meshesDict = {}
		for mesh in bpy.data.meshes:
			meshesDict[mesh.name] = []
		for obj in bpy.context.scene.objects:
			if obj.type == 'MESH' and obj.data.name in meshesDict:
				meshesDict[obj.data.name].append(obj.name)
				fileExportPath = projectExportPath + '/Assets/Art/Models/' + obj.data.name + '.fbx'
				MakeFolderForFile (fileExportPath)
				bpy.ops.object.select_all(action='DESELECT')
				bpy.context.view_layer.objects.active = obj
				obj.select_set(True)
				previousObjectScale = obj.scale
				obj.scale *= 100
				bpy.ops.export_scene.fbx(filepath=fileExportPath, use_selection=True, use_custom_props=True, mesh_smooth_type='FACE')
				obj.scale = previousObjectScale
				for materialSlot in obj.material_slots:
					fileExportPath = projectExportPath + '/Assets/Art/Materials/' + materialSlot.material.name + '.mat'
					MakeFolderForFile (fileExportPath)
					material = open(os.path.expanduser('~/Unity2Many/Templates/Material.mat'), 'rb').read().decode('utf-8')
					material = material.replace(REPLACE_INDICATOR + '0', materialSlot.material.name)
					materialColor = materialSlot.material.diffuse_color
					material = material.replace(REPLACE_INDICATOR + '1', str(materialColor[0]))
					material = material.replace(REPLACE_INDICATOR + '2', str(materialColor[1]))
					material = material.replace(REPLACE_INDICATOR + '3', str(materialColor[2]))
					material = material.replace(REPLACE_INDICATOR + '4', str(materialColor[3]))
					open(fileExportPath, 'wb').write(material.encode('utf-8'))
		unityVersionsPath = os.path.expanduser('~/Unity/Hub/Editor')
		unityVersionPath = ''
		if os.path.isdir(unityVersionsPath):
			unityVersions = os.listdir(unityVersionsPath)
			for unityVersion in unityVersions:
				_unityVersionPath = unityVersionsPath + '/' + unityVersion + '/Editor/Unity'
				if os.path.isfile(_unityVersionPath):
					unityVersionPath = _unityVersionPath
					break
		if unityVersionPath != '':
			MakeFolderForFile (projectExportPath + '/Assets/Editor/GetUnityProjectInfo.cs')
			open(projectExportPath + '/Assets/Editor/GetUnityProjectInfo.cs', 'wb').write(GET_UNITY_PROJECT_INFO_SCRIPT.encode('utf-8'))

			os.system('cp ' + os.path.expanduser('~/Unity2Many/SystemExtensions.cs') + ' ' + projectExportPath + '/Assets/Editor/SystemExtensions.cs')

			command = [ unityVersionPath, '-quit', '-createProject', projectExportPath, '-executeMethod', 'GetUnityProjectInfo.Do', projectExportPath ]
			print(command)
			
			subprocess.check_call(command)

		scenePath = bpy.data.filepath.replace('.blend', '.unity')
		scenePath = scenePath[scenePath.rfind('/') + 1 :]
		scenesFolderPath = projectExportPath + '/Assets/Scenes'
		if not os.path.isdir(scenesFolderPath):
			os.mkdir(scenesFolderPath)
		if scenePath == '':
			scenePath = 'Test.unity'
		scenePath = scenesFolderPath + '/' + scenePath
		sceneTemplateText = open(os.path.expanduser('~/Unity2Many/Templates/Scene.unity'), 'rb').read().decode('utf-8')
		gameObjectsAndComponentsText = ''
		transformIds = []
		for obj in bpy.data.objects:
			componentIds = []
			gameObject = GAME_OBJECT_TEMPLATE
			gameObject = gameObject.replace(REPLACE_INDICATOR + '0', str(lastId))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '1', str(lastId + 1))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '3', obj.name)
			gameObjectsAndComponentsText += gameObject + '\n'
			gameObjectId = lastId
			lastId += 1
			transform = TRANSFORM_TEMPLATE
			transform = transform.replace(REPLACE_INDICATOR + '10', str(obj.scale.z))
			transform = transform.replace(REPLACE_INDICATOR + '11', str(obj.scale.y))
			transform = transform.replace(REPLACE_INDICATOR + '0', str(lastId))
			transform = transform.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			previousObjectRotationMode = obj.rotation_mode
			obj.rotation_mode = 'XYZ'
			eulerAngles = obj.rotation_euler
			previousYEulerAngles = eulerAngles.y
			eulerAngles.y = eulerAngles.z
			eulerAngles.z = previousYEulerAngles + PI
			rotation = eulerAngles.to_quaternion()
			transform = transform.replace(REPLACE_INDICATOR + '2', str(rotation.x))
			transform = transform.replace(REPLACE_INDICATOR + '3', str(rotation.y))
			transform = transform.replace(REPLACE_INDICATOR + '4', str(rotation.z))
			transform = transform.replace(REPLACE_INDICATOR + '5', str(rotation.w))
			obj.rotation_mode = previousObjectRotationMode
			transform = transform.replace(REPLACE_INDICATOR + '6', str(obj.location.x))
			transform = transform.replace(REPLACE_INDICATOR + '7', str(obj.location.z))
			transform = transform.replace(REPLACE_INDICATOR + '8', str(obj.location.y))
			transform = transform.replace(REPLACE_INDICATOR + '9', str(obj.scale.x))
			gameObjectsAndComponentsText += transform + '\n'
			transformIds.append(lastId)
			lastId += 1
			guidIndicator = 'guid: '
			if obj.type == 'LIGHT':
				light = LIGHT_TEMPLATE
				light = light.replace(REPLACE_INDICATOR + '0', str(lastId))
				light = light.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				lightObject = bpy.data.lights[obj.name]
				lightType = 2
				if lightObject.type == 'SUN':
					lightType = 1
				elif lightObject.type == 'SPOT':
					lightType = 0
				elif lightObject.type == 'AREA':
					lightType = 3
				light = light.replace(REPLACE_INDICATOR + '2', str(lightType))
				light = light.replace(REPLACE_INDICATOR + '3', str(lightObject.color[0]))
				light = light.replace(REPLACE_INDICATOR + '4', str(lightObject.color[1]))
				light = light.replace(REPLACE_INDICATOR + '5', str(lightObject.color[2]))
				light = light.replace(REPLACE_INDICATOR + '6', str(lightObject.energy * WATTS_TO_CANDELAS))
				light = light.replace(REPLACE_INDICATOR + '7', str(10))
				spotSize = 0
				innerSpotAngle = 0
				if lightType == 0:
					spotSize = lightObject.spot_size
					innerSpotAngle = spotSize * (1.0 - lightObject.spot_blend)
				light = light.replace(REPLACE_INDICATOR + '8', str(spotSize))
				light = light.replace(REPLACE_INDICATOR + '9', str(innerSpotAngle))
				gameObjectsAndComponentsText += light + '\n'
				componentIds.append(lastId)
				lastId += 1
			elif obj.type == 'MESH':
				meshFilter = MESH_FILTER_TEMPLATE
				meshFilter = meshFilter.replace(REPLACE_INDICATOR + '0', str(lastId))
				meshFilter = meshFilter.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				filePath = projectExportPath + '/Assets/Art/Models/' + obj.data.name + '.fbx.meta'
				meshGuid = GetGuid(filePath)
				open(filePath, 'wb').write(MESH_META_TEMPLATE.replace(REPLACE_INDICATOR, meshGuid).encode('utf-8'))
				if unityVersionPath != '':
					dataText = open('/tmp/Unity2Many Data (BlenderToUnity)', 'rb').read().decode('utf-8')
					fileIdIndicator = '-' + projectExportPath + '/Assets/Art/Models/' + obj.data.name + '.fbx'
					indexOfFile = dataText.find(fileIdIndicator)
					indexOfFileId = indexOfFile + len(fileIdIndicator) + 1
					indexOfEndOfFileId = dataText.find(' ', indexOfFileId)
					fileId = dataText[indexOfFileId : indexOfEndOfFileId]
				else:
					fileId = '10202'
				meshFilter = meshFilter.replace(REPLACE_INDICATOR + '2', fileId)
				meshFilter = meshFilter.replace(REPLACE_INDICATOR + '3', meshGuid)
				gameObjectsAndComponentsText += meshFilter + '\n'
				componentIds.append(lastId)
				lastId += 1
				meshRenderer = MESH_RENDERER_TEMPLATE
				meshRenderer = meshRenderer.replace(REPLACE_INDICATOR + '0', str(lastId))
				meshRenderer = meshRenderer.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				materials = ''
				for materialSlot in obj.material_slots:
					filePath = projectExportPath + '/Assets/Art/Materials/' + materialSlot.material.name + '.mat.meta'
					materialGuid = GetGuid(filePath)
					open(filePath, 'wb').write(MATERIAL_META_TEMPLATE.replace(REPLACE_INDICATOR, materialGuid).encode('utf-8'))
					if unityVersionPath != '':
						dataText = open('/tmp/Unity2Many Data (BlenderToUnity)', 'rb').read().decode('utf-8')
						fileIdIndicator = '-' + projectExportPath + '/Assets/Art/Materials/' + materialSlot.material.name + '.mat'
						indexOfFile = dataText.find(fileIdIndicator)
						indexOfFileId = indexOfFile + len(fileIdIndicator) + 1
						indexOfEndOfFileId = dataText.find(' ', indexOfFileId)
						fileId = dataText[indexOfFileId : indexOfEndOfFileId]
					else:
						fileId = '10303'
					material = MATERIAL_TEMPLATE
					material = material.replace(REPLACE_INDICATOR + '0', fileId)
					material = material.replace(REPLACE_INDICATOR + '1', materialGuid)
					materials += material + '\n'
				materials = materials[: -1]
				meshRenderer = meshRenderer.replace(REPLACE_INDICATOR + '2', materials)
				gameObjectsAndComponentsText += meshRenderer + '\n'
				componentIds.append(lastId)
				lastId += 1
			elif obj.type == 'CAMERA':
				camera = CAMERA_TEMPLATE
				camera = camera.replace(REPLACE_INDICATOR + '0', str(lastId))
				camera = camera.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				cameraObject = bpy.data.cameras[obj.name]
				fovAxisMode = 0
				if cameraObject.sensor_fit == 'HORIZONTAL':
					fovAxisMode = 1
				camera = camera.replace(REPLACE_INDICATOR + '2', str(fovAxisMode))
				camera = camera.replace(REPLACE_INDICATOR + '3', str(cameraObject.clip_start))
				camera = camera.replace(REPLACE_INDICATOR + '4', str(cameraObject.clip_end))
				camera = camera.replace(REPLACE_INDICATOR + '5', str(cameraObject.angle * (180.0 / PI)))
				isOrthographic = 0
				if cameraObject.type == 'ORTHO':
					isOrthographic = 1
				camera = camera.replace(REPLACE_INDICATOR + '6', str(isOrthographic))
				camera = camera.replace(REPLACE_INDICATOR + '7', str(cameraObject.ortho_scale))
				gameObjectsAndComponentsText += camera + '\n'
				componentIds.append(lastId)
				lastId += 1
			attachedScripts = attachedScriptsDict.get(obj, [])
			for scriptName in attachedScripts:
				script = SCRIPT_TEMPLATE
				script = script.replace(REPLACE_INDICATOR + '0', str(lastId))
				script = script.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				MakeFolderForFile (filePath)
				filePath = projectExportPath + '/Assets/Standard Assets/Scripts/' + scriptName
				for textBlock in bpy.data.texts:
					if textBlock.name == scriptName:
						if not scriptName.endswith('.cs'):
							filePath += '.cs'
						scriptText = textBlock.as_string()
						scriptText = scriptText.replace('Vector3.up', 'Vector3.forward')
						open(filePath, 'wb').write(scriptText.encode('utf-8'))
						break
				filePath += '.meta'
				scriptGuid = GetGuid(filePath)
				scriptMeta = SCRIPT_META_TEMPLATE
				scriptMeta += scriptGuid
				open(filePath, 'wb').write(scriptMeta.encode('utf-8'))
				script = script.replace(REPLACE_INDICATOR + '2', scriptGuid)
				gameObjectsAndComponentsText += script + '\n'
				componentIds.append(lastId)
				lastId += 1
				break
			indexOfComponentsList = gameObjectsAndComponentsText.find(REPLACE_INDICATOR + '2')
			for componentId in componentIds:
				component = COMPONENT_TEMPLATE
				component = component.replace(REPLACE_INDICATOR, str(componentId))
				gameObjectsAndComponentsText = gameObjectsAndComponentsText[: indexOfComponentsList] + component + '\n' + gameObjectsAndComponentsText[indexOfComponentsList :]
				gameObjectsAndComponentsText = gameObjectsAndComponentsText.replace(REPLACE_INDICATOR + '2', '')
		sceneText = sceneTemplateText.replace(REPLACE_INDICATOR + '0', gameObjectsAndComponentsText)
		sceneRootsText = ''
		for transformId in transformIds:
			sceneRoot = SCENE_ROOT_TEMPLATE
			sceneRoot = sceneRoot.replace(REPLACE_INDICATOR, str(transformId))
			sceneRootsText += sceneRoot + '\n'
		sceneText = sceneText.replace(REPLACE_INDICATOR + '1', sceneRootsText)
		open(scenePath, 'wb').write(sceneText.encode('utf-8'))
		if unityVersionPath != '':
			command = [ unityVersionPath, '-createProject', projectExportPath ]
			
			subprocess.check_call(command)

class TEXT_EDITOR_OT_PygameExportButton (bpy.types.Operator):
	bl_idname = 'pygame.export'
	bl_label = 'Export To Pygame'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		BuildTool ('UnityToPygame')
		pygameExportPath = os.path.expanduser(context.scene.world.pygame_project_path)
		if not os.path.isdir(pygameExportPath):
			MakeFolderForFile (pygameExportPath + '/')
		importPath = os.path.expanduser(context.scene.world.unity_project_import_path)
		if importPath != '':
			command = [ 'python3', os.path.expanduser('~/Unity2Many/UnityToPygame.py'), 'input=' + importPath, 'output=' + pygameExportPath, 'exclude=/Library' ]
			print(command)

			subprocess.check_call(command)

		else:
			data = pygameExportPath
			for obj in attachedScriptsDict:
				data += '\n' + obj.name + '☢️' + '☣️'.join(attachedScriptsDict[obj])
			open('/tmp/Unity2Many Data (BlenderToPygame)', 'wb').write(data.encode('utf-8'))
			

class TEXT_EDITOR_OT_UnrealTranslateButton (bpy.types.Operator):
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
		MakeFolderForFile ('/tmp/Unity2Many (Unreal Scripts)/')
		script = currentTextBlock.name
		if not currentTextBlock.name.endswith('.cs'):
			script += '.cs'
		filePath = '/tmp/Unity2Many (Unreal Scripts)/' + script
		open(filePath, 'wb').write(currentTextBlock.as_string().encode('utf-8'))
		ConvertCSFileToCPP (filePath)

class TEXT_EDITOR_OT_BevyTranslateButton (bpy.types.Operator):
	bl_idname = 'bevy.translate'
	bl_label = 'Translate To Bevy'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		global operatorContext
		global currentTextBlock
		BuildTool ('UnityToBevy')
		operatorContext = context
		script = currentTextBlock.name
		if not currentTextBlock.name.endswith('.cs'):
			script += '.cs'
		filePath = '/tmp/' + script
		open(filePath, 'wb').write(currentTextBlock.as_string().encode('utf-8'))
		ConvertCSFileToRust (filePath)

timer = None
@bpy.utils.register_class
class Loop (bpy.types.Operator):
	bl_idname = 'blender_plugin.start'
	bl_label = 'blender_plugin_start'
	bl_options = { 'REGISTER' }

	def modal (self, context, event):
		for area in bpy.data.screens['Layout'].areas:
			if area.type == 'VIEW_3D':
				for region in area.regions:
					if region.type == 'WINDOW':
						region.tag_redraw()
		return {'PASS_THROUGH'} # will not supress event bubbles

	def invoke (self, context, event):
		global timer
		if timer is None:
			timer = self._timer = context.window_manager.event_timer_add(
				time_step=0.016666667,
				window=context.window)
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {'FINISHED'}

	def execute (self, context):
		return self.invoke(context, None)

classes = [
	TEXT_EDITOR_OT_UnrealExportButton,
	TEXT_EDITOR_OT_BevyExportButton,
	TEXT_EDITOR_OT_UnityExportButton,
	TEXT_EDITOR_OT_PygameExportButton,
	TEXT_EDITOR_OT_UnrealTranslateButton,
	TEXT_EDITOR_OT_BevyTranslateButton,
	ExamplesOperator,
	ExamplesMenu,
	AttachedObjectsMenu
]

def BuildTool (toolName : str):
	command = [ 'make', 'build_' + toolName ]
	print(command)

	subprocess.check_call(command)

def ExportMesh (obj):
	meshAssetPath = '/tmp/' + obj.name + '.fbx'
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.export_scene.fbx(filepath=meshAssetPath, use_selection=True, use_custom_props=True, mesh_smooth_type='FACE')

def GetBasicObjectData (obj):
	for _obj in bpy.data.objects:
		if _obj.name == obj.name:
			obj = _obj
			break
	previousObjectRotationMode = obj.rotation_mode
	obj.rotation_mode = 'QUATERNION'
	output = obj.name + '☣️' + str(obj.location * 100) + '☣️' + str(obj.rotation_quaternion) + '☣️' + str(obj.scale)
	obj.rotation_mode = previousObjectRotationMode
	return output

def GetCameraData (camera):
	horizontalFov = False
	if camera.sensor_fit == 'HORIZONTAL':
		horizontalFov = True
	isOrthographic = False
	if camera.type == 'ORTHO':
		isOrthographic = True
	return GetBasicObjectData(camera) + '☣️' + str(horizontalFov) + '☣️' + str(camera.angle * (180.0 / PI)) + '☣️' + str(isOrthographic) + '☣️' + str(camera.ortho_scale) + '☣️' + str(camera.clip_start) + '☣️' + str(camera.clip_end)

def GetLightData (light):
	lightType = 0
	if light.type == 'POINT':
		lightType = 1
	elif light.type == 'SPOT':
		lightType = 2
	elif lightObject.type == 'AREA':
		lightType = 3
	return GetBasicObjectData(light) + '☣️' + str(lightType) + '☣️' + str(light.energy * WATTS_TO_CANDELAS * 100) + '☣️' + str(light.color)

def GetGuid (filePath : str):
	return hashlib.md5(filePath.encode('utf-8')).hexdigest()

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
		os.path.expanduser('~/Unity2Many/UnityToUnreal/Unity2Many.dll'),
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
	command = [ 'python3', os.path.expanduser('~/Unity2Many') + '/py2many/py2many.py', '--cpp=1', outputFilePath, '--unreal=1', '--outdir=' + unrealCodePath ]
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

def ConvertCSFileToRust (filePath):
	global mainClassName
	mainClassName = filePath[filePath.rfind('/') + 1 : filePath.rfind('.')]
	assert os.path.isfile(filePath)
	MakeFolderForFile ('/tmp/src/main.rs')
	MakeFolderForFile ('/tmp/assets/registry.json')
	data = 'output=/tmp\n' + filePath
	open('/tmp/Unity2Many Data (UnityToBevy)', 'wb').write(data.encode('utf-8'))
	command = [
		'dotnet',
		os.path.expanduser('~/Unity2Many/UnityToBevy/Unity2Many.dll'), 
		'includeFile=' + filePath,
		'bevy=true',
		'output=/tmp'
	]
	# for arg in sys.argv:
	# 	command.append(arg)
	print(command)

	subprocess.check_call(command)

	outputFilePath = '/tmp/main.py'
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
	command = [ 'python3', 'py2many/py2many.py', '--rust=1', '--force', filePath, '--outdir=/tmp/src' ]
	# for arg in sys.argv:
	# 	command.append(arg)
	command.append(os.path.expanduser(operatorContext.scene.world.unity_project_import_path))
	print(command)
	
	subprocess.check_call(command)

	outputFilePath = '/tmp/src/main.rs'
	assert os.path.isfile(outputFilePath)
	print(outputFilePath)

	os.system('cat ' + outputFilePath)
	
	data = open('/tmp/Unity2Many Data (UnityToBevy)', 'rb').read().decode('utf-8')
	filePath = data[data.find('\n') + 1 :]
	for textBlock in bpy.data.texts:
		if textBlock.name == filePath[filePath.rfind('/') + 1 :].replace('.rs', '.cs'):
			textBlock.name = textBlock.name.replace('.cs', '.rs')
			textBlock.clear()
			outputFileText = open('/tmp/src/main.rs', 'rb').read().decode('utf-8')
			textBlock.write(outputFileText)

def DrawExamplesMenu (self, context):
	self.layout.menu(ExamplesMenu.bl_idname)

def DrawAttachedObjectsMenu (self, context):
	self.layout.menu(AttachedObjectsMenu.bl_idname)

def DrawUnityImportField (self, context):
	self.layout.prop(context.world, 'unity_project_import_path')

def DrawUnityExportField (self, context):
	self.layout.prop(context.world, 'unity_project_export_path')

# def DrawUnityExportVersionField (self, context):
# 	self.layout.prop(context.world, 'unity_export_version')

def DrawUnrealExportField (self, context):
	self.layout.prop(context.world, 'unrealExportPath')

def DrawBevyExportField (self, context):
	self.layout.prop(context.world, 'bevy_project_path')

def DrawPygameExportField (self, context):
	self.layout.prop(context.world, 'pygame_project_path')

def DrawUnrealExportButton (self, context):
	self.layout.operator(TEXT_EDITOR_OT_UnrealExportButton.bl_idname, icon='CONSOLE')

def DrawBevyExportButton (self, context):
	self.layout.operator(TEXT_EDITOR_OT_BevyExportButton.bl_idname, icon='CONSOLE')

def DrawUnityExportButton (self, context):
	self.layout.operator(TEXT_EDITOR_OT_UnityExportButton.bl_idname, icon='CONSOLE')

def DrawPygameExportButton (self, context):
	self.layout.operator(TEXT_EDITOR_OT_PygameExportButton.bl_idname, icon='CONSOLE')

def DrawUnrealTranslateButton (self, context):
	self.layout.operator(TEXT_EDITOR_OT_UnrealTranslateButton.bl_idname, icon='CONSOLE')

def DrawBevyTranslateButton (self, context):
	self.layout.operator(TEXT_EDITOR_OT_BevyTranslateButton.bl_idname, icon='CONSOLE')

def DrawAttachScriptDropdown (self, context):
	self.layout.prop(context.object, 'attach_script_dropdown')

def SetupObjectContext (self, context):
	global attachedScriptsDict
	global detachScriptDropdownOptions
	detachScriptDropdownOptions.clear()
	attachedScripts = attachedScriptsDict.get(context.object, [])
	i = 0
	for attachedScript in attachedScripts:
		detachScriptDropdownOptions.append((attachedScript, attachedScript, '', '', i))
		i += 1

def DrawDetachScriptDropdown (self, context):
	self.layout.prop(context.object, 'detach_script_dropdown')

def SetupTextEditorFooterContext (self, context):
	global currentTextBlock
	global previousRunningScripts
	currentTextBlock = context.edit_text
	previousRunningScripts = []
	for textBlock in bpy.data.texts:
		if textBlock.name == '.gltf_auto_export_gltf_settings':
			continue
		if textBlock.run_cs:
			previousRunningScripts.append(textBlock.name)

def DrawRunCSToggle (self, context):
	self.layout.prop(context.edit_text, 'run_cs')

def AttachScript (self, context):
	global attachedScriptsDict
	if bpy.context.object.attach_script_dropdown == 'No scripts exist':
		return
	attachedScripts = attachedScriptsDict.get(self, [])
	attachedScripts.append(bpy.context.object.attach_script_dropdown)
	attachedScriptsDict[self] = attachedScripts
	if bpy.context.object.attach_script_dropdown + ' attach count' in self.keys():
		self[bpy.context.object.attach_script_dropdown + ' attach count'] += 1
	else:
		self[bpy.context.object.attach_script_dropdown + ' attach count'] = 1

def DetachScript (self, context):
	global attachedScriptsDict
	if bpy.context.object.detach_script_dropdown == 'No scripts attached':
		return
	attachedScripts = attachedScriptsDict.get(self, [])
	if bpy.context.object.detach_script_dropdown in attachedScripts:
		attachedScripts.remove(bpy.context.object.detach_script_dropdown)
	attachedScriptsDict[self] = attachedScripts
	self[bpy.context.object.attach_script_dropdown + ' attach count'] -= 1

def UpdateInspectorFields (textBlock):
	text = textBlock.as_string()
	publicIndicator = 'public '
	indexOfPublicIndicator = text.find(publicIndicator)
	while indexOfPublicIndicator != -1:
		indexOfVariable = IndexOfAny(text, [ ' ', ';' , '=' ], indexOfPublicIndicator + len(publicIndicator))
		indexOfLastSpaceAfterPublicIndicator = indexOfPublicIndicator + len(publicIndicator)
		while True:
			indexOfLastSpaceAfterPublicIndicator += 1
			if text[indexOfLastSpaceAfterPublicIndicator] != ' ':
				break
		indexOfLastSpaceAfterPublicIndicator -= 1
		indexOfParenthesis = text.find('(', indexOfLastSpaceAfterPublicIndicator + 1)
		if indexOfParenthesis == indexOfLastSpaceAfterPublicIndicator + 1:
			continue
		
		indexOfPublicIndicator = text.find(publicIndicator, indexOfPublicIndicator + len(publicIndicator))

def OnRedrawView ():
	global currentTextBlock
	global textBlocksTextsDict
	global attachedScriptsDict
	global previousRunningScripts
	global previousTextBlocksTextsDict
	global attachScriptDropdownOptions
	global detachScriptDropdownOptions
	attachScriptDropdownOptions.clear()
	i = 0
	defaultScript = None
	defaultAttachedScript = None
	textBlocksTextsDict = {}
	for textBlock in bpy.data.texts:
		if textBlock.name == '.gltf_auto_export_gltf_settings':
			continue
		textBlocksTextsDict[textBlock.name] = textBlock.as_string()
		if i == 0:
			defaultScript = textBlock.name
		attachedScripts = attachedScriptsDict.get(bpy.context.object, [])
		defaultAttachedScript = None
		for attachedScript in attachedScripts:
			defaultAttachedScript = attachedScript
			break
		attachScriptDropdownOptions.append((textBlock.name, textBlock.name, '', '', i))
		if textBlock.name not in previousTextBlocksTextsDict or previousTextBlocksTextsDict[textBlock.name] != textBlock.as_string():
			UpdateInspectorFields (textBlock)
		i += 1
	if defaultScript == None:
		attachScriptDropdownOptions.append(('No scripts exist', 'No scripts exist', '', '', i))
	previousTextBlocksTextsDict = textBlocksTextsDict.copy()
	bpy.types.Object.attach_script_dropdown = bpy.props.EnumProperty(
		items = attachScriptDropdownOptions,
		name = 'Attach script',
		description = '',
		default = defaultScript if defaultScript != None else 'No scripts exist',
		update = AttachScript
	)
	bpy.types.OBJECT_PT_context_object.remove(SetupObjectContext)
	bpy.types.OBJECT_PT_context_object.append(SetupObjectContext)
	if len(detachScriptDropdownOptions) == 0:
		detachScriptDropdownOptions.append(('No scripts attached', 'No scripts attached', '', '', 0))
	bpy.types.Object.detach_script_dropdown = bpy.props.EnumProperty(
		items = detachScriptDropdownOptions,
		name = 'Detach script',
		description = '',
		default = defaultAttachedScript if defaultAttachedScript != None else 'No scripts attached',
		update = DetachScript
	)
	bpy.types.TEXT_HT_footer.remove(SetupTextEditorFooterContext)
	bpy.types.TEXT_HT_footer.append(SetupTextEditorFooterContext)
	bpy.types.OBJECT_PT_context_object.remove(DrawAttachScriptDropdown)
	bpy.types.OBJECT_PT_context_object.append(DrawAttachScriptDropdown)
	bpy.types.OBJECT_PT_context_object.remove(DrawDetachScriptDropdown)
	bpy.types.OBJECT_PT_context_object.append(DrawDetachScriptDropdown)
	if currentTextBlock != None:
		if currentTextBlock.run_cs:
			import RunCSInBlender as runCSInBlender
			for obj in attachedScriptsDict:
				if currentTextBlock.name in attachedScriptsDict[obj]:
					filePath = os.path.expanduser('/tmp/Unity2Many Data (UnityInBlender)/' + currentTextBlock.name)
					filePath = filePath.replace('.cs', '.py')
					if not filePath.endswith('.py'):
						filePath += '.py'
					if currentTextBlock.name not in previousRunningScripts:
						MakeFolderForFile (filePath)
						open(filePath, 'wb').write(currentTextBlock.as_string().encode('utf-8'))
						BuildTool ('UnityInBlender')
						command = [
							'dotnet',
							os.path.expanduser('~/Unity2Many/UnityInBlender/Unity2Many.dll'), 
							'includeFile=' + filePath,
							'output=/tmp/Unity2Many Data (UnityInBlender)'
						]
						print(command)

						subprocess.check_call(command)
					runCSInBlender.Run (filePath, obj)
	# id = 0
	# size = 32
	# blf.size(id, size)
	# blf.color(id, 0, 1, 0, 0.8)
	# x = 0
	# y = 0
	# blf.draw(id, str(random()))

def register ():
	global attachedScriptsDict
	registryText = open(TEMPLATE_REGISTRY_PATH, 'rb').read().decode('utf-8')
	registryText = registryText.replace('ꗈ', '')
	open(REGISTRY_PATH, 'wb').write(registryText.encode('utf-8'))
	toolsPath = os.path.expanduser('~/Unity2Many/Blender_bevy_components_workflow/tools')
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

	# componentsAddonPath = os.path.expanduser('~/Unity2Many/Blender_bevy_components_workflow/tools/bevy_components')
	# if os.path.isdir(componentsAddonPath):
	# 	sys.path.append(componentsAddonPath)
	bpy.ops.preferences.addon_enable(module='io_import_images_as_planes')
	registry = bpy.context.window_manager.components_registry
	registry.schemaPath = REGISTRY_PATH
	bpy.ops.object.reload_registry()
	for obj in bpy.data.objects:
		attachedScripts = []
		for key in obj.keys():
			attachCountIndicator = ' attach count'
			if key.endswith(attachCountIndicator):
				for i in range(obj[key]):
					attachedScripts.append(key.replace(attachCountIndicator, ''))
		attachedScriptsDict[obj] = attachedScripts

	# bpy.types.View3DShading.color_type = 'OBJECT'
	for cls in classes:
		bpy.utils.register_class(cls)
	bpy.types.World.unity_project_import_path = bpy.props.StringProperty(
		name = 'Unity project import path',
		description = '',
		default = ''
	)
	bpy.types.World.unity_project_export_path = bpy.props.StringProperty(
		name = 'Unity project export path',
		description = '',
		default = '/tmp/TestUnityProject'
	)
	# bpy.types.World.unity_export_version = bpy.props.StringProperty(
	# 	name = 'Unity export version',
	# 	description = '',
	# 	default = ''
	# )
	bpy.types.World.unrealExportPath = bpy.props.StringProperty(
		name = 'Unreal project path',
		description = '',
		default = ''
	)
	bpy.types.World.bevy_project_path = bpy.props.StringProperty(
		name = 'Bevy project path',
		description = '',
		default = ''
	)
	bpy.types.World.pygame_project_path = bpy.props.StringProperty(
		name = 'Pygame project path',
		description = '',
		default = ''
	)
	bpy.types.Text.run_cs = bpy.props.BoolProperty(
		name = 'Run C# Script',
		description = ''
	)
	bpy.types.TEXT_HT_header.append(DrawExamplesMenu)
	bpy.types.TEXT_HT_header.append(DrawAttachedObjectsMenu)
	bpy.types.TEXT_HT_footer.append(DrawUnrealTranslateButton)
	bpy.types.TEXT_HT_footer.append(DrawBevyTranslateButton)
	bpy.types.TEXT_HT_footer.append(DrawRunCSToggle)
	bpy.types.WORLD_PT_context_world.append(DrawUnityImportField)
	bpy.types.WORLD_PT_context_world.append(DrawUnityExportField)
	# bpy.types.WORLD_PT_context_world.append(DrawUnityExportVersionField)
	bpy.types.WORLD_PT_context_world.append(DrawUnrealExportField)
	bpy.types.WORLD_PT_context_world.append(DrawBevyExportField)
	# bpy.types.WORLD_PT_context_world.append(DrawPygameExportField)
	bpy.types.WORLD_PT_context_world.append(DrawUnrealExportButton)
	bpy.types.WORLD_PT_context_world.append(DrawBevyExportButton)
	bpy.types.WORLD_PT_context_world.append(DrawUnityExportButton)
	# bpy.types.WORLD_PT_context_world.append(DrawPygameExportButton)
	handle = bpy.types.SpaceView3D.draw_handler_add(
		OnRedrawView,
		tuple([]),
		'WINDOW', 'POST_PIXEL')
	bpy.ops.blender_plugin.start()

def unregister ():
	bpy.types.TEXT_HT_header.remove(DrawExamplesMenu)
	bpy.types.TEXT_HT_header.append(DrawAttachedObjectsMenu)
	bpy.types.TEXT_HT_footer.remove(DrawUnrealTranslateButton)
	bpy.types.TEXT_HT_footer.remove(DrawBevyTranslateButton)
	bpy.types.TEXT_HT_footer.remove(DrawRunCSToggle)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityImportField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityExportField)
	# bpy.types.WORLD_PT_context_world.remove(DrawUnityExportVersionField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnrealExportField)
	bpy.types.WORLD_PT_context_world.remove(DrawBevyExportField)
	# bpy.types.WORLD_PT_context_world.remove(DrawPygameExportField)
	bpy.types.WORLD_PT_context_world.remove(DrawUnrealExportButton)
	bpy.types.WORLD_PT_context_world.remove(DrawBevyExportButton)
	bpy.types.WORLD_PT_context_world.remove(DrawUnityExportButton)
	# bpy.types.WORLD_PT_context_world.remove(DrawPygameExportButton)
	for cls in classes:
		bpy.utils.unregister_class(cls)

if __name__ == '__main__':
	register ()