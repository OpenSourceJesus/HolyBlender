#!/usr/bin/env python3
import bpy, subprocess, os, sys, hashlib, mathutils, math, base64, webbrowser

_thisdir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append(_thisdir)
from libholyblender import *

sys.path.append(os.path.join(_thisdir, 'blender-to-unity-fbx-exporter'))
try:
	import blender_to_unity_fbx_exporter as fbxExporter
	print(fbxExporter)
except:
	fbxExporter = None
if fbxExporter:
	bpy.ops.preferences.addon_enable(module='blender_to_unity_fbx_exporter')

for i in range(MAX_SCRIPTS_PER_OBJECT):
	setattr(bpy.types.Object, 'unity_script' + str(i), bpy.props.PointerProperty(name='Attach Unity script', type=bpy.types.Text))


bpy.types.World.unity_project_import_path = bpy.props.StringProperty(
	name = 'Unity project import path',
	description = '',
	default = ''
)
bpy.types.World.unity_project_export_path = bpy.props.StringProperty(
	name = 'Unity project export path',
	description = '',
	default = '~/TestUnityProject'
)

bpy.types.Text.run_cs = bpy.props.BoolProperty(
	name = 'Run C# Script',
	description = ''
)

EXAMPLES_DICT = {
	'Hello World (Unity)' : '''using UnityEngine;

public class HelloWorld : MonoBehaviour
{
	void Start ()
	{
		print("Hello World!");
	}
}''',
	'Rotate (Unity)': '''using UnityEngine;

public class Rotate : MonoBehaviour
{
	public float rotateSpeed = 50.0f;

	void Update ()
	{
		transform.eulerAngles += Vector3.up * rotateSpeed * Time.deltaTime;
	}
}''',
	'Grow And Shrink (Unity)': '''using UnityEngine;

public class GrowAndShrink : MonoBehaviour
{
	public float maxSize = 5.0f; 
	public float minSize = 0.2f;
	public float speed = 0.375f;

	void Update ()
	{
		transform.localScale = Vector3.one * (((Mathf.Sin(speed * Time.time) + 1) / 2) * (maxSize - minSize) + minSize);
	}
}''',
	'Keyboard And Mouse Controls (Unity)' : '''using UnityEngine;

public class WASDAndMouseControls : MonoBehaviour
{
	public float moveSpeed = 5.0f;

	void Update ()
	{
		Vector3 move = Vector3.zero;
		if (Input.GetKey(KeyCode.A))
			move.x -= 1.0f;
		if (Input.GetKey(KeyCode.D))
			move.x += 1.0f;
		if (Input.GetKey(KeyCode.S))
			move.y -= 1.0f;
		if (Input.GetKey(KeyCode.W))
			move.y += 1.0f;
		move.Normalize();
		transform.position += move * moveSpeed * Time.deltaTime;
		Vector3 mousePosition = Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue());
		transform.up = mousePosition - transform.position;
	}
}''',
	'First Person Controls (Unity) (Unfinished)' : '''using UnityEngine;
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
}''',

}

@bpy.utils.register_class
class UnityExportButton (bpy.types.Operator):
	bl_idname = 'unity.export'
	bl_label = 'Export To Unity'
	INIT_YAML_TEXT = '''%YAML 1.1
%TAG !u! tag:unity3d.com,2011:'''
	MATERIAL_TEMPLATE = '    - {fileID: ꗈ0, guid: ꗈ1, type: 2}'
	COMPONENT_TEMPLATE = '    - component: {fileID: ꗈ}'
	CHILD_TRANSFORM_TEMPLATE = '    - {fileID: ꗈ}'
	SCENE_ROOT_TEMPLATE = CHILD_TRANSFORM_TEMPLATE
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
  m_Layer: ꗈ3
  m_Name: ꗈ4
  m_TagString: ꗈ5
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
  m_Children: ꗈ12
  m_Father: {fileID: ꗈ13}
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
  m_Script: {fileID: 11500000, guid: ꗈ2, type: 3}'''
	MESH_FILTER_TEMPLATE = '''--- !u!33 &ꗈ0
MeshFilter:
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Mesh: {fileID: ꗈ2, guid: ꗈ3, type: 3}'''
	MESH_RENDERER_TEMPLATE = '''--- !u!23 &ꗈ0
MeshRenderer:
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Materials:
ꗈ2'''
	MESH_COLLIDER_TEMPLATE = '''--- !u!64 &ꗈ0
MeshCollider:
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Material: {fileID: 0}
  m_IsTrigger: ꗈ2
  m_Convex: ꗈ3
  m_Mesh: {fileID: ꗈ4, guid: ꗈ5, type: 3}'''
	RIGIDBODY_TEMPLATE = '''--- !u!54 &ꗈ0
Rigidbody:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  serializedVersion: 4
  m_Mass: ꗈ2
  m_Drag: ꗈ3
  m_AngularDrag: ꗈ4
  m_CenterOfMass: {x: 0, y: 0, z: 0}
  m_InertiaTensor: {x: 1, y: 1, z: 1}
  m_InertiaRotation: {x: 0, y: 0, z: 0 w: 1}
  m_IncludeLayers:
    serializedVersion: 2
    m_Bits: 0
  m_ExcludeLayers:
    serializedVersion: 2
    m_Bits: 0
  m_ImplicitCom: 1
  m_ImplicitTensor: 1
  m_UseGravity: ꗈ5
  m_IsKinematic: ꗈ6
  m_Interpolate: ꗈ7
  m_Constraints: ꗈ8
  m_CollisionDetection: ꗈ9'''
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
	SPRITE_RENDERER_TEMPLATE = '''--- !u!212 &ꗈ0
SpriteRenderer:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Enabled: 1
  m_CastShadows: 0
  m_ReceiveShadows: 0
  m_DynamicOccludee: 1
  m_StaticShadowCaster: 0
  m_MotionVectors: 1
  m_LightProbeUsage: 1
  m_ReflectionProbeUsage: 1
  m_RayTracingMode: 0
  m_RayTraceProcedural: 0
  m_RayTracingAccelStructBuildFlagsOverride: 0
  m_RayTracingAccelStructBuildFlags: 1
  m_SmallMeshCulling: 1
  m_RenderingLayerMask: 1
  m_RendererPriority: 0
  m_Materials:
  - {fileID: 10754, guid: 0000000000000000f000000000000000, type: 0}
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
  m_SelectedEditorRenderState: 0
  m_MinimumChartSize: 4
  m_AutoUVMaxDistance: 0.5
  m_AutoUVMaxAngle: 89
  m_LightmapParameters: {fileID: 0}
  m_SortingLayerID: ꗈ2
  m_SortingLayer: ꗈ3
  m_SortingOrder: ꗈ4
  m_Sprite: {fileID: 0, guid: ꗈ5, type: 3}
  m_Color: {r: 1, g: 1, b: 1, a: 1}
  m_FlipX: 0
  m_FlipY: 0
  m_DrawMode: 0
  m_Size: {x: 0, y: 0}
  m_AdaptiveModeThreshold: 0.5
  m_SpriteTileMode: 0
  m_WasSpriteAssigned: 1
  m_MaskInteraction: 0
  m_SpriteSortPoint: 0'''
	SPRITE_META_TEMPLATE = '''fileFormatVersion: 2
guid: ꗈ0
TextureImporter:
  internalIDToNameTable:
  - first:
      213: 0
    second: ꗈ1_0
  externalObjects: {}
  serializedVersion: 13
  mipmaps:
    mipMapMode: 0
    enableMipMap: 0
    sRGBTexture: 1
    linearTexture: 0
    fadeOut: 0
    borderMipMap: 0
    mipMapsPreserveCoverage: 0
    alphaTestReferenceValue: 0.5
    mipMapFadeDistanceStart: 1
    mipMapFadeDistanceEnd: 3
  bumpmap:
    convertToNormalMap: 0
    externalNormalMap: 0
    heightScale: 0.25
    normalMapFilter: 0
    flipGreenChannel: 0
  isReadable: 1
  streamingMipmaps: 0
  streamingMipmapsPriority: 0
  vTOnly: 0
  ignoreMipmapLimit: 0
  grayScaleToAlpha: 0
  generateCubemap: 6
  cubemapConvolution: 0
  seamlessCubemap: 0
  textureFormat: 1
  maxTextureSize: 16384
  textureSettings:
    serializedVersion: 2
    filterMode: 1
    aniso: 1
    mipBias: 0
    wrapU: 1
    wrapV: 1
    wrapW: 1
  nPOTScale: 0
  lightmap: 0
  compressionQuality: 50
  spriteMode: 2
  spriteExtrude: 1
  spriteMeshType: 1
  alignment: 0
  spritePivot: {x: 0.5, y: 0.5}
  spritePixelsToUnits: 100
  spriteBorder: {x: 0, y: 0, z: 0, w: 0}
  spriteGenerateFallbackPhysicsShape: 1
  alphaUsage: 1
  alphaIsTransparency: 1
  spriteTessellationDetail: -1
  textureType: 8
  textureShape: 1
  singleChannelComponent: 0
  flipbookRows: 1
  flipbookColumns: 1
  maxTextureSizeSet: 0
  compressionQualitySet: 0
  textureFormatSet: 0
  ignorePngGamma: 0
  applyGammaDecoding: 0
  swizzle: 50462976
  cookieLightType: 0
  platformSettings:
  - serializedVersion: 4
    buildTarget: DefaultTexturePlatform
    maxTextureSize: 16384
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 0
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  - serializedVersion: 4
    buildTarget: Win64
    maxTextureSize: 16384
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  - serializedVersion: 4
    buildTarget: Linux64
    maxTextureSize: 16384
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  - serializedVersion: 4
    buildTarget: Standalone
    maxTextureSize: 16384
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  - serializedVersion: 4
    buildTarget: Android
    maxTextureSize: 16384
    resizeAlgorithm: 0
    textureFormat: -1
    textureCompression: 1
    compressionQuality: 50
    crunchedCompression: 0
    allowsAlphaSplitting: 0
    overridden: 0
    ignorePlatformSupport: 0
    androidETC2FallbackOverride: 0
    forceMaximumCompressionQuality_BC6H_BC7: 0
  spriteSheet:
    serializedVersion: 2
    sprites:
    - serializedVersion: 2
      name: ꗈ1_0
      rect:
        serializedVersion: 2
        x: 0
        y: 0
        width: 242
        height: 188
      alignment: 0
      pivot: {x: 0, y: 0}
      border: {x: 0, y: 0, z: 0, w: 0}
      customData: 
      outline: []
      physicsShape: []
      tessellationDetail: -1
      bones: []
      spriteID: 85166db83dab01790800000000000000
      internalID: 0
      vertices: []
      indices: 
      edges: []
      weights: []
    outline: []
    customData: 
    physicsShape: []
    bones: []
    spriteID: 
    internalID: 0
    vertices: []
    indices: 
    edges: []
    weights: []
    secondaryTextures: []
    spriteCustomMetadata:
      entries: []
    nameFileIdTable:
      ꗈ1_0: 0
  mipmapLimitGroupName: 
  pSDRemoveMatte: 0
  userData: 
  assetBundleName: 
  assetBundleVariant: '''
	PREFAB_INSTANCE_TEMPLATE = '''--- !u!1001 &ꗈ0
PrefabInstance:
  m_ObjectHideFlags: 0
  serializedVersion: 2
  m_Modification:
    serializedVersion: 3
    m_TransformParent: {fileID: ꗈ1}
    m_Modifications:
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalPosition.x
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalPosition.y
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalPosition.z
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalRotation.w
      value: 1
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalRotation.x
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalRotation.y
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalRotation.z
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalEulerAnglesHint.x
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalEulerAnglesHint.y
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ2, guid: ꗈ3, type: 3}
      propertyPath: m_LocalEulerAnglesHint.z
      value: 0
      objectReference: {fileID: 0}
    - target: {fileID: ꗈ4, guid: ꗈ3, type: 3}
      propertyPath: m_Name
      value: ꗈ5
      objectReference: {fileID: 0}
	ꗈ6
    m_RemovedComponents: ꗈ7
    m_RemovedGameObjects: ꗈ8
    m_AddedGameObjects: ꗈ9
    m_AddedComponents: ꗈ10
  m_SourcePrefab: {fileID: 100100000, guid: ꗈ3, type: 3}
--- !u!4 &ꗈ11 stripped
Transform:
  m_CorrespondingSourceObject: {fileID: ꗈ2, guid: ꗈ3, type: 3}
  m_PrefabInstance: {fileID: ꗈ0}
  m_PrefabAsset: {fileID: 0}'''
	gameObjectsAndComponentsText = ''
	rootTransformsIds = []
	componentIds = []
	projectExportPath = ''
	unityVersionPath = ''
	lastId = 5
	prefabGuidsDict = {}
	isMakingScene = False
	dataText = ''
	gameObjectAndTrsVarsDict = {}
	gameObjectIdsDict = {}
	trsIdsDict = {}
	exportedObjs = []

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		unityVersionsPath = os.path.expanduser(os.path.join('~', 'Unity', 'Hub', 'Editor'))
		self.unityVersionPath = ''
		if os.path.isdir(unityVersionsPath):
			unityVersions = os.listdir(unityVersionsPath)
			for unityVersion in unityVersions:
				self.unityVersionPath = unityVersionsPath + '/' + unityVersion + '/Editor/Unity'
				if os.path.isfile(self.unityVersionPath):
					self.unityVersionPath = self.unityVersionPath
					break
		if self.unityVersionPath == '':
			print('No Unity version installed')
			return {"FINISHED"}

		self.lastId = 5
		self.projectExportPath = os.path.expanduser(context.scene.world.unity_project_export_path)
		if not os.path.isdir(self.projectExportPath):
			os.mkdir(self.projectExportPath)
		meshesDict = {}
		for mesh in bpy.data.meshes:
			meshesDict[mesh.name] = []
		scriptsPath = os.path.join(self.projectExportPath, 'Assets', 'Scripts')
		MakeFolderForFile (os.path.join(scriptsPath, ''))
		for obj in bpy.context.scene.objects:
			if obj.type == 'MESH' and obj.data.name in meshesDict:
				meshesDict[obj.data.name].append(obj.name)
				fileExportFolder = os.path.join(self.projectExportPath, 'Assets', 'Art', 'Models')
				fileExportPath = os.path.join(fileExportFolder, '')
				MakeFolderForFile (fileExportPath)
				# prevoiusObjectSize = obj.scale
				# obj.scale *= 100
				fileExportPath = ExportObject(obj, fileExportFolder)
				# obj.scale = prevoiusObjectSize
				for materialSlot in obj.material_slots:
					fileExportPath = self.projectExportPath + '/Assets/Art/Materials/' + materialSlot.material.name + '.mat'
					MakeFolderForFile (fileExportPath)
					materialColor = materialSlot.material.diffuse_color
					material = open(os.path.join(TEMPLATES_PATH, 'Material.mat'), 'rb').read().decode('utf-8')
					material = material.replace(REPLACE_INDICATOR + '0', materialSlot.material.name)
					material = material.replace(REPLACE_INDICATOR + '1', str(materialColor[0]))
					material = material.replace(REPLACE_INDICATOR + '2', str(materialColor[1]))
					material = material.replace(REPLACE_INDICATOR + '3', str(materialColor[2]))
					material = material.replace(REPLACE_INDICATOR + '4', str(materialColor[3]))
					open(fileExportPath, 'wb').write(material.encode('utf-8'))
			elif obj.type == 'EMPTY' and obj.empty_display_type == 'IMAGE':
				spritePath = obj.data.filepath
				spritePath = os.path.expanduser('~') + spritePath[1 :]
				spriteName = spritePath[spritePath.rfind('/') + 1 :]
				newSpritePath = os.path.join(self.projectExportPath, 'Assets', 'Art', 'Textures', spriteName)
				MakeFolderForFile (newSpritePath)
				sprite = open(spritePath, 'rb').read()
				open(newSpritePath, 'wb').write(sprite)
		MakeFolderForFile (os.path.join(self.projectExportPath, 'Assets', 'Editor', ''))
		CopyFile (os.path.join(UNITY_SCRIPTS_PATH, 'GetUnityProjectInfo.cs'), os.path.join(self.projectExportPath, 'Assets', 'Editor', 'GetUnityProjectInfo.cs'))
		CopyFile (os.path.join(EXTENSIONS_PATH, 'SystemExtensions.cs'), os.path.join(scriptsPath, 'SystemExtensions.cs'))
		CopyFile (os.path.join(EXTENSIONS_PATH, 'StringExtensions.cs'), os.path.join(scriptsPath, 'StringExtensions.cs'))
		command = self.unityVersionPath + ' -quit -createProject ' + self.projectExportPath + ' -executeMethod GetUnityProjectInfo.Do ' + self.projectExportPath
		print(command)
		
		subprocess.check_call(command.split())

		os.system('cp -r ' + os.path.join(_thisdir, 'UnityGLTF') + ' ' + os.path.join(self.projectExportPath, 'Assets', 'UnityGLTF'))

		self.dataText = open('/tmp/HolyBlender Data (BlenderToUnity)', 'rb').read().decode('utf-8')
		prefabsPath = os.path.join(self.projectExportPath, 'Assets', 'Resources')
		MakeFolderForFile (os.path.join(prefabsPath, ''))
		self.isMakingScene = False
		self.prefabGuidsDict.clear()
		self.gameObjectAndTrsVarsDict.clear()
		self.gameObjectIdsDict.clear()
		self.trsIdsDict.clear()
		self.exportedObjs.clear()
		for collection in bpy.data.collections:
			self.gameObjectsAndComponentsText = ''
			prefabPath = os.path.join(prefabsPath, collection.name + '.prefab')
			self.prefabGuidsDict[collection.name] = GetGuid(prefabPath)
			open(prefabPath + '.meta', 'w').write('guid: ' + self.prefabGuidsDict[collection.name])
			for obj in collection.objects:
				if GetObjectId(obj) not in self.exportedObjs:
					self.MakeObject (obj)
			prefab = self.INIT_YAML_TEXT
			prefab += '\n' + self.gameObjectsAndComponentsText
			open(prefabPath, 'w').write(prefab)
		self.isMakingScene = True
		self.gameObjectsAndComponentsText = ''
		self.rootTransformsIds = []
		for obj in bpy.context.scene.objects:
			if obj.parent == None and GetObjectId(obj) not in self.exportedObjs:
				self.MakeObject (obj)
		scriptsFolder = os.path.join(self.projectExportPath, 'Assets', 'Scripts')
		MakeFolderForFile (os.path.join(self.projectExportPath, 'Assets', 'Scripts', ''))
		sendAndRecieveServerEventsScriptPath = os.path.join(scriptsFolder, 'SendAndRecieveServerEvents.cs')
		CopyFile (os.path.join(UNITY_SCRIPTS_PATH, 'SendAndRecieveServerEvents.cs'), sendAndRecieveServerEventsScriptPath)
		gameObjectIdAndTrsId = self.MakeEmptyObject('Send And Recieve Server Events')
		sendAndRecieveServerEventsScriptMetaPath = sendAndRecieveServerEventsScriptPath + '.meta'
		scriptGuid = GetGuid(sendAndRecieveServerEventsScriptMetaPath)
		open(sendAndRecieveServerEventsScriptMetaPath, 'w').write('guid: ' + scriptGuid)
		script = self.SCRIPT_TEMPLATE
		script = script.replace(REPLACE_INDICATOR + '0', str(self.lastId))
		script = script.replace(REPLACE_INDICATOR + '1', str(gameObjectIdAndTrsId[0]))
		script = script.replace(REPLACE_INDICATOR + '2', scriptGuid)
		self.gameObjectsAndComponentsText += script + '\n'
		self.componentIds.append(self.lastId)
		self.gameObjectsAndComponentsText = self.gameObjectsAndComponentsText.replace(REPLACE_INDICATOR + '2', self.COMPONENT_TEMPLATE.replace(REPLACE_INDICATOR, str(self.lastId)))
		for key in self.gameObjectAndTrsVarsDict:
			if varaiblesTypesDict[key[1]] == 'GameObject':
				self.gameObjectsAndComponentsText = self.gameObjectsAndComponentsText.replace(REPLACE_INDICATOR, '{fileID: ' + str(self.gameObjectIdsDict[self.gameObjectAndTrsVarsDict[key]]) + '}')
			else:# elif varaiblesTypesDict[key[1]] == 'Transform':
				for obj in self.trsIdsDict:
					print(obj)
				self.gameObjectsAndComponentsText = self.gameObjectsAndComponentsText.replace(REPLACE_INDICATOR, '{fileID: ' + str(self.trsIdsDict[self.gameObjectAndTrsVarsDict[key]]) + '}')
		sceneRootsText = ''
		for transformId in self.rootTransformsIds:
			sceneRoot = self.SCENE_ROOT_TEMPLATE
			sceneRoot = sceneRoot.replace(REPLACE_INDICATOR, str(transformId))
			sceneRootsText += sceneRoot + '\n'
		scenePath = bpy.data.filepath.replace('.blend', '.unity')
		scenePath = scenePath[scenePath.rfind('/') + 1 :]
		scenesFolderPath = self.projectExportPath + '/Assets/Scenes'
		if not os.path.isdir(scenesFolderPath):
			os.mkdir(scenesFolderPath)
		if scenePath == '':
			scenePath = 'Test.unity'
		scenePath = scenesFolderPath + '/' + scenePath
		sceneTemplateText = open(os.path.expanduser('~/HolyBlender/Templates/Scene.unity'), 'rb').read().decode('utf-8')
		sceneText = sceneTemplateText.replace(REPLACE_INDICATOR + '0', self.gameObjectsAndComponentsText)
		sceneText = sceneText.replace(REPLACE_INDICATOR + '1', sceneRootsText)
		open(scenePath, 'wb').write(sceneText.encode('utf-8'))
		if self.unityVersionPath != '':
			command = [ self.unityVersionPath, '-createProject', self.projectExportPath ]
			subprocess.check_call(command)
		return {"FINISHED"}

	def MakeEmptyObject (self, name : str, layer = 0, parentTransformId = 0) -> (int, int):
		gameObject = self.GAME_OBJECT_TEMPLATE
		gameObject = gameObject.replace(REPLACE_INDICATOR + '0', str(self.lastId))
		gameObject = gameObject.replace(REPLACE_INDICATOR + '1', str(self.lastId + 1))
		gameObject = gameObject.replace(REPLACE_INDICATOR + '3', str(layer))
		gameObject = gameObject.replace(REPLACE_INDICATOR + '4', name)
		gameObject = gameObject.replace(REPLACE_INDICATOR + '5', 'Untagged')
		self.gameObjectsAndComponentsText += gameObject + '\n'
		gameObjectId = self.lastId
		self.lastId += 1
		transform = self.TRANSFORM_TEMPLATE
		transform = transform.replace(REPLACE_INDICATOR + '10', '1')
		transform = transform.replace(REPLACE_INDICATOR + '11', '1')
		transform = transform.replace(REPLACE_INDICATOR + '12', '[]')
		transform = transform.replace(REPLACE_INDICATOR + '13', str(parentTransformId))
		transform = transform.replace(REPLACE_INDICATOR + '0', str(self.lastId))
		transform = transform.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
		transform = transform.replace(REPLACE_INDICATOR + '2', '0')
		transform = transform.replace(REPLACE_INDICATOR + '3', '0')
		transform = transform.replace(REPLACE_INDICATOR + '4', '0')
		transform = transform.replace(REPLACE_INDICATOR + '5', '1')
		transform = transform.replace(REPLACE_INDICATOR + '6', '0')
		transform = transform.replace(REPLACE_INDICATOR + '7', '0')
		transform = transform.replace(REPLACE_INDICATOR + '8', '0')
		transform = transform.replace(REPLACE_INDICATOR + '9', '1')
		self.gameObjectsAndComponentsText += transform + '\n'
		if parentTransformId == 0:
			self.rootTransformsIds.append(self.lastId)
		self.lastId += 1
		return (gameObjectId, self.lastId - 1)

	def MakeObject (self, obj, parentTransformId = 0) -> int:
		attachedUnityScriptsDict = get_user_scripts('unity')
		self.componentIds = []
		prefabName = ''
		# for collection in bpy.data.collections:
		# 	for obj2 in collection.objects:
		# 		if obj == obj2:
		# 			prefabName = collection.name
		# 			break
		# 	if prefabName != '':
		# 		break
		gameObject = ''
		meshFileId = '10202'
		meshGuid = ''
		gameObjectId = self.lastId
		myTransformId = self.lastId + 1
		self.lastId += 2
		children = ''
		for childObj in obj.children:
			if GetObjectId(childObj) not in self.exportedObjs:
				transformId = self.MakeObject(childObj, myTransformId)
				children += '\n' + self.CHILD_TRANSFORM_TEMPLATE.replace(REPLACE_INDICATOR, str(transformId))
		if obj.type == 'MESH':
			filePath = self.projectExportPath + '/Assets/Art/Models/' + obj.name + '.fbx.meta'
			meshGuid = GetGuid(filePath)
			open(filePath, 'w').write('guid: ' + meshGuid)
			if self.unityVersionPath != '':
				meshDatas = self.dataText.split('\n')[0]
				fileIdIndicator = '-' + self.projectExportPath + '/Assets/Art/Models/' + obj.name + '.fbx'
				indexOfFile = meshDatas.find(fileIdIndicator)
				indexOfFileId = indexOfFile + len(fileIdIndicator) + 1
				indexOfEndOfFileId = meshDatas.find(' ', indexOfFileId)
				meshFileId = meshDatas[indexOfFileId : indexOfEndOfFileId]
			gameObjectIdAndTrsId = self.MakeClickableChild(obj.name, meshFileId, meshGuid, myTransformId)
			children += '\n' + self.CHILD_TRANSFORM_TEMPLATE.replace(REPLACE_INDICATOR, str(gameObjectIdAndTrsId[1]))
		elif len(obj.children) == 0:
			children = '[]'
		if prefabName == '' or not self.isMakingScene:
			tag = 'Untagged'
			if obj.type == 'CAMERA':
				tag = 'MainCamera'
			gameObject = self.GAME_OBJECT_TEMPLATE
			gameObject = gameObject.replace(REPLACE_INDICATOR + '0', str(gameObjectId))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '1', str(myTransformId))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '3', '0')
			gameObject = gameObject.replace(REPLACE_INDICATOR + '4', obj.name)
			gameObject = gameObject.replace(REPLACE_INDICATOR + '5', tag)
			self.lastId += 1
			location = obj.matrix_local.translation
			rotation = obj.matrix_local.to_euler()
			if obj.type != 'MESH':
				rotation.x -= PI / 2
				previousYRot = rotation.y
				rotation.y = -rotation.z
				rotation.z = -previousYRot
			rotation = rotation.to_quaternion()
			scale = obj.matrix_local.to_scale()
			transform = self.TRANSFORM_TEMPLATE
			transform = transform.replace(REPLACE_INDICATOR + '10', str(scale.z))
			transform = transform.replace(REPLACE_INDICATOR + '11', str(scale.y))
			transform = transform.replace(REPLACE_INDICATOR + '12', children)
			transform = transform.replace(REPLACE_INDICATOR + '13', str(parentTransformId))
			transform = transform.replace(REPLACE_INDICATOR + '0', str(myTransformId))
			transform = transform.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			transform = transform.replace(REPLACE_INDICATOR + '2', str(rotation.x))
			transform = transform.replace(REPLACE_INDICATOR + '3', str(rotation.y))
			transform = transform.replace(REPLACE_INDICATOR + '4', str(rotation.z))
			transform = transform.replace(REPLACE_INDICATOR + '5', str(rotation.w))
			transform = transform.replace(REPLACE_INDICATOR + '6', str(location.x))
			transform = transform.replace(REPLACE_INDICATOR + '7', str(location.z))
			transform = transform.replace(REPLACE_INDICATOR + '8', str(location.y))
			transform = transform.replace(REPLACE_INDICATOR + '9', str(scale.x))
			self.gameObjectsAndComponentsText += transform + '\n'
		else:
			gameObject = self.PREFAB_INSTANCE_TEMPLATE
			gameObject = gameObject.replace(REPLACE_INDICATOR + '10', '[]')
			gameObject = gameObject.replace(REPLACE_INDICATOR + '11', str(myTransformId))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '0', str(gameObjectId))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '1', str(parentTransformId))
			gameObject = gameObject.replace(REPLACE_INDICATOR + '2', '6')
			gameObject = gameObject.replace(REPLACE_INDICATOR + '3', self.prefabGuidsDict[prefabName])
			gameObject = gameObject.replace(REPLACE_INDICATOR + '4', '5')
			gameObject = gameObject.replace(REPLACE_INDICATOR + '5', prefabName)
			gameObject = gameObject.replace(REPLACE_INDICATOR + '6', '')
			gameObject = gameObject.replace(REPLACE_INDICATOR + '7', '[]')
			gameObject = gameObject.replace(REPLACE_INDICATOR + '8', '[]')
			gameObject = gameObject.replace(REPLACE_INDICATOR + '9', '[]')
		if parentTransformId == 0:
			self.rootTransformsIds.append(myTransformId)
		self.gameObjectsAndComponentsText += gameObject + '\n'
		self.lastId += 1
		if obj.type == 'EMPTY' and obj.empty_display_type == 'IMAGE':
			spritePath = obj.data.filepath
			spritePath = os.path.expanduser('~') + spritePath[1 :]
			spriteName = spritePath[spritePath.rfind('/') + 1 :]
			newSpritePath = os.path.join(self.projectExportPath, 'Assets', 'Art', 'Textures', spriteName)
			spriteGuid = GetGuid(newSpritePath)
			spriteMeta = self.SPRITE_META_TEMPLATE
			spriteMeta = spriteMeta.replace(REPLACE_INDICATOR + '0', spriteGuid)
			spriteMeta = spriteMeta.replace(REPLACE_INDICATOR + '1', spriteName)
			open(newSpritePath + '.meta', 'wb').write(spriteMeta.encode('utf-8'))
			spriteRenderer = self.SPRITE_RENDERER_TEMPLATE
			spriteRenderer = spriteRenderer.replace(REPLACE_INDICATOR + '0', str(self.lastId))
			spriteRenderer = spriteRenderer.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			spriteRenderer = spriteRenderer.replace(REPLACE_INDICATOR + '2', '0')
			spriteRenderer = spriteRenderer.replace(REPLACE_INDICATOR + '3', '0')
			spriteRenderer = spriteRenderer.replace(REPLACE_INDICATOR + '4', '0')
			spriteRenderer = spriteRenderer.replace(REPLACE_INDICATOR + '5', spriteGuid)
			self.gameObjectsAndComponentsText += spriteRenderer + '\n'
			self.componentIds.append(self.lastId)
			self.lastId += 1
		elif obj.type == 'LIGHT':
			lightObject = bpy.data.lights[obj.name]
			lightType = 2
			if lightObject.type == 'SUN':
				lightType = 1
			elif lightObject.type == 'SPOT':
				lightType = 0
			elif lightObject.type == 'AREA':
				lightType = 3
			spotSize = 0
			innerSpotAngle = 0
			if lightType == 0:
				spotSize = lightObject.spot_size
				innerSpotAngle = spotSize * (1.0 - lightObject.spot_blend)
			light = self.LIGHT_TEMPLATE
			light = light.replace(REPLACE_INDICATOR + '0', str(self.lastId))
			light = light.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			light = light.replace(REPLACE_INDICATOR + '2', str(lightType))
			light = light.replace(REPLACE_INDICATOR + '3', str(lightObject.color[0]))
			light = light.replace(REPLACE_INDICATOR + '4', str(lightObject.color[1]))
			light = light.replace(REPLACE_INDICATOR + '5', str(lightObject.color[2]))
			light = light.replace(REPLACE_INDICATOR + '6', str(lightObject.energy * WATTS_TO_CANDELAS))
			light = light.replace(REPLACE_INDICATOR + '7', str(10))
			light = light.replace(REPLACE_INDICATOR + '8', str(spotSize))
			light = light.replace(REPLACE_INDICATOR + '9', str(innerSpotAngle))
			self.gameObjectsAndComponentsText += light + '\n'
			self.componentIds.append(self.lastId)
			self.lastId += 1
		elif obj.type == 'MESH':
			meshFilter = self.MESH_FILTER_TEMPLATE
			meshFilter = meshFilter.replace(REPLACE_INDICATOR + '0', str(self.lastId))
			meshFilter = meshFilter.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			meshFilter = meshFilter.replace(REPLACE_INDICATOR + '2', meshFileId)
			meshFilter = meshFilter.replace(REPLACE_INDICATOR + '3', meshGuid)
			self.gameObjectsAndComponentsText += meshFilter + '\n'
			self.componentIds.append(self.lastId)
			self.lastId += 1
			for modifier in obj.modifiers:
				if modifier.type == 'COLLISION':
					self.AddMeshCollider (gameObjectId, False, False, meshFileId, meshGuid)
					break
			if obj.rigid_body != None:
				rigidbody = self.RIGIDBODY_TEMPLATE
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '0', str(self.lastId))
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '2', str(obj.rigid_body.mass))
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '3', str(obj.rigid_body.linear_damping))
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '4', str(obj.rigid_body.angular_damping))
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '5', '1')
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '6', str(int(obj.rigid_body.enabled)))
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '7', '0')
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '8', '0')
				rigidbody = rigidbody.replace(REPLACE_INDICATOR + '9', '0')
				self.gameObjectsAndComponentsText += rigidbody + '\n'
				self.componentIds.append(self.lastId)
				self.lastId += 1
			materials = ''
			for materialSlot in obj.material_slots:
				filePath = self.projectExportPath + '/Assets/Art/Materials/' + materialSlot.material.name + '.mat.meta'
				materialGuid = GetGuid(filePath)
				open(filePath, 'w').write('guid: ' + materialGuid)
				if self.unityVersionPath != '':
					fileIdIndicator = '-' + self.projectExportPath + '/Assets/Art/Materials/' + materialSlot.material.name + '.mat'
					indexOfFile = self.dataText.find(fileIdIndicator)
					indexOfFileId = indexOfFile + len(fileIdIndicator) + 1
					indexOfEndOfFileId = self.dataText.find(' ', indexOfFileId)
					fileId = self.dataText[indexOfFileId : indexOfEndOfFileId]
				else:
					fileId = '10303'
				material = self.MATERIAL_TEMPLATE
				material = material.replace(REPLACE_INDICATOR + '0', fileId)
				material = material.replace(REPLACE_INDICATOR + '1', materialGuid)
				materials += material + '\n'
			materials = materials[: -1]
			meshRenderer = self.MESH_RENDERER_TEMPLATE
			meshRenderer = meshRenderer.replace(REPLACE_INDICATOR + '0', str(self.lastId))
			meshRenderer = meshRenderer.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			meshRenderer = meshRenderer.replace(REPLACE_INDICATOR + '2', materials)
			self.gameObjectsAndComponentsText += meshRenderer + '\n'
			self.componentIds.append(self.lastId)
			self.lastId += 1
		elif obj.type == 'CAMERA':
			cameraObj = bpy.data.cameras[obj.name]
			fovAxisMode = 0
			if cameraObj.sensor_fit == 'HORIZONTAL':
				fovAxisMode = 1
			isOrthographic = 0
			if cameraObj.type == 'ORTHO':
				isOrthographic = 1
			camera = self.CAMERA_TEMPLATE
			camera = camera.replace(REPLACE_INDICATOR + '0', str(self.lastId))
			camera = camera.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			camera = camera.replace(REPLACE_INDICATOR + '2', str(fovAxisMode))
			camera = camera.replace(REPLACE_INDICATOR + '3', str(cameraObj.clip_start))
			camera = camera.replace(REPLACE_INDICATOR + '4', str(cameraObj.clip_end))
			camera = camera.replace(REPLACE_INDICATOR + '5', str(cameraObj.angle * (180.0 / PI)))
			camera = camera.replace(REPLACE_INDICATOR + '6', str(isOrthographic))
			camera = camera.replace(REPLACE_INDICATOR + '7', str(cameraObj.ortho_scale / 2))
			self.gameObjectsAndComponentsText += camera + '\n'
			self.componentIds.append(self.lastId)
			self.lastId += 1
		attachedScripts = attachedUnityScriptsDict.get(obj, [])
		for scriptName in attachedScripts:
			filePath = self.projectExportPath + '/Assets/Scripts/' + scriptName
			MakeFolderForFile (filePath)
			for textBlock in bpy.data.texts:
				if textBlock.name == scriptName:
					if not scriptName.endswith('.cs'):
						filePath += '.cs'
					scriptText = textBlock.as_string()
					open(filePath, 'wb').write(scriptText.encode('utf-8'))
					break
			filePath += '.meta'
			scriptGuid = GetGuid(filePath)
			open(filePath, 'w').write('guid: ' + scriptGuid)
			script = self.SCRIPT_TEMPLATE
			script = script.replace(REPLACE_INDICATOR + '0', str(self.lastId))
			script = script.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			script = script.replace(REPLACE_INDICATOR + '2', scriptGuid)
			hasPublicVariable = False
			for propertyName in propertyNames:
				scriptIndicator = scriptName + '_'
				if propertyName.startswith(scriptIndicator):
					propertyValue = getattr(obj, propertyName)
					variableType = varaiblesTypesDict[propertyName]
					if variableType == 'Color':
						if not Equals(propertyValue, NULL_COLOR):
							color = '{r: ' + str(propertyValue[0]) + ', g: ' + str(propertyValue[1]) + ', b: ' + str(propertyValue[2]) + ', a: ' + str(propertyValue[3]) + '}'
							script += '\n  ' + propertyName[len(scriptIndicator) :] + ': ' + color
					elif variableType == 'GameObject' or variableType == 'Transform':
						self.gameObjectAndTrsVarsDict[(obj, propertyName)] = propertyValue
						script += '\n  ' + propertyName[len(scriptIndicator) :] + ': ' + REPLACE_INDICATOR
					else:
						script += '\n  ' + propertyName[len(scriptIndicator) :] + ': ' + str(propertyValue)
			self.gameObjectsAndComponentsText += script + '\n'
			self.componentIds.append(self.lastId)
			self.lastId += 1
		indexOfComponentsList = self.gameObjectsAndComponentsText.find(REPLACE_INDICATOR + '2')
		for componentId in self.componentIds:
			component = self.COMPONENT_TEMPLATE
			component = component.replace(REPLACE_INDICATOR, str(componentId))
			self.gameObjectsAndComponentsText = self.gameObjectsAndComponentsText[: indexOfComponentsList] + component + '\n' + self.gameObjectsAndComponentsText[indexOfComponentsList :]
		self.gameObjectsAndComponentsText = self.gameObjectsAndComponentsText.replace(REPLACE_INDICATOR + '2', '')
		self.gameObjectIdsDict[obj] = gameObjectId
		self.trsIdsDict[obj] = myTransformId
		self.exportedObjs.append(GetObjectId(obj))
		return myTransformId

	def AddMeshCollider (self, gameObjectId : int, isTirgger : bool, isConvex : bool, fileId : str, meshGuid : str):
		meshCollider = self.MESH_COLLIDER_TEMPLATE
		meshCollider = meshCollider.replace(REPLACE_INDICATOR + '0', str(self.lastId))
		meshCollider = meshCollider.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
		meshCollider = meshCollider.replace(REPLACE_INDICATOR + '2', str(int(isTirgger)))
		meshCollider = meshCollider.replace(REPLACE_INDICATOR + '3', str(int(isConvex)))
		meshCollider = meshCollider.replace(REPLACE_INDICATOR + '4', fileId)
		meshCollider = meshCollider.replace(REPLACE_INDICATOR + '5', meshGuid)
		self.gameObjectsAndComponentsText += meshCollider + '\n'
		self.componentIds.append(self.lastId)
		self.lastId += 1

	def MakeClickableChild (self, name : str, fileId : str, meshGuid : str, parentTransformId = 0) -> (int, int):
		gameObjectAndTrsId = self.MakeEmptyObject(name, 31, parentTransformId)
		self.AddMeshCollider (gameObjectAndTrsId[0], True, True, fileId, meshGuid)
		return gameObjectAndTrsId

@bpy.utils.register_class
class WorldPanel(bpy.types.Panel):
	bl_idname = 'WORLD_PT_WorldUnity_Panel'
	bl_label = 'HolyUnity'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'

	def draw (self, context):
		self.layout.prop(context.world, 'unity_project_import_path')
		self.layout.prop(context.world, 'unity_project_export_path')
		self.layout.operator('unity.export', icon='CONSOLE')
		self.layout.operator('unity.play', icon='CONSOLE')


@bpy.utils.register_class
class ScriptVariablesPanel (bpy.types.Panel):
	bl_label = "Scripts Public Variables"
	bl_idname = "OBJECT_PT_Script_Public_Variables"
	bl_space_type = "PROPERTIES"
	bl_region_type = "WINDOW"
	bl_context = "object"

	def draw (self, context):
		for propertyName in propertyNames:
			if varaiblesTypesDict[propertyName] == 'Color':
				if not Equals(getattr(context.active_object, propertyName), NULL_COLOR):
					self.layout.prop(context.active_object, propertyName)
			elif varaiblesTypesDict[propertyName] == 'GameObject' or varaiblesTypesDict[propertyName] == 'Transform':
				if propertyName in gameObjectAndTrsVarsDict[context.active_object]:
					self.layout.prop(context.active_object, propertyName)
			else:
				self.layout.prop(context.active_object, propertyName)

@bpy.utils.register_class
class UnityScriptsPanel (bpy.types.Panel):
	bl_idname = 'OBJECT_PT_Unity_Scripts_Panel'
	bl_label = 'HolyBlender Unity Scripts'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'

	def draw (self, context):
		self.layout.label(text='Attach Unity scripts')
		foundUnassignedScript = False
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			hasScript = getattr(context.active_object, 'unity_script' + str(i)) != None
			if hasScript or not foundUnassignedScript:
				self.layout.prop(context.active_object, 'unity_script' + str(i))
			if not foundUnassignedScript:
				foundUnassignedScript = not hasScript

@bpy.utils.register_class
class PlayButton (bpy.types.Operator):
	bl_idname = 'unity.play'
	bl_label = 'Start Playing (Unfinished)'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		for textBlock in bpy.data.texts:
			textBlock.run_cs = True
