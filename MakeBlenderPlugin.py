import bpy, subprocess, os, sys, hashlib, mathutils, math, base64, webbrowser

user_args = None
for arg in sys.argv:
	if arg=='--': user_args = []
	elif type(user_args) is list: user_args.append(arg)
if user_args:print('user_args:', user_args)

__thisdir = os.path.split(os.path.abspath(__file__))[0]
sys.path.append( __thisdir )
sys.path.append( os.path.join(__thisdir, 'Blender_bevy_components_workflow/tools') )
print(sys.path)
import bevy_components
print(bevy_components)
import gltf_auto_export
print(gltf_auto_export)
bpy.ops.preferences.addon_enable(module='bevy_components')
bpy.ops.preferences.addon_enable(module='gltf_auto_export')

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
    m_Layer: ꗈ3
    m_Name: ꗈ4
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
MESH_COLLIDER_TEMPLATE = '''--- !u!64 &ꗈ0
MeshCollider:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {fileID: 0}
  m_PrefabInstance: {fileID: 0}
  m_PrefabAsset: {fileID: 0}
  m_GameObject: {fileID: ꗈ1}
  m_Material: {fileID: 0}
  m_IncludeLayers:
    serializedVersion: 2
    m_Bits: 0
  m_ExcludeLayers:
    serializedVersion: 2
    m_Bits: 0
  m_LayerOverridePriority: 0
  m_IsTrigger: ꗈ2
  m_ProvidesContacts: 0
  m_Enabled: 1
  serializedVersion: 5
  m_Convex: ꗈ3
  m_CookingOptions: 30
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
	'Hello World (bevy)' : 'println!("Hello World!");',
	'Rotate (bevy)' : 'trs.rotate_y(5.0 * time.delta_seconds());)'
}
INIT_HTML = '''
<script>
function Test ()
{
	alert("Ok");
	//TODO xmlhttprequest
}
</script>
<button onclick="Test ()">Hello World!</button>
<a href="/bpy/data/objects/Cube">Cube</a>
'''
# HTML_IMAGE_TEMPLATE = '<img id="ꗈ0" style="position:fixed; left:ꗈ1px; top:ꗈ2px; width:ꗈ3px; height:ꗈ4px; z-index:ꗈ5" src="data:image/gif;base64,ꗈ6">'
HTML_IMAGE_TEMPLATE = '<img id="ꗈ0" style="position:fixed; left:ꗈ1px; top:ꗈ2px; z-index:ꗈ5" src="data:image/gif;base64,ꗈ6">'
BLENDER_SERVER = '''
import bpy
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler

LOCALHOST_PORT = 8000

class BlenderServer (BaseHTTPRequestHandler):
	def do_GET (self):
		self.send_response(200)
		self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
		self.send_header("Pragma", "no-cache")
		self.send_header("Expires", "0")

		ret = 'OK'
		hint = ''
		if self.path.endswith('.ico'):
			pass
		elif self.path == '/':
			if '__index__.html' in bpy.data.texts:
				ret = bpy.data.texts['__index__.html'].as_string()
			else:
				for t in bpy.data.texts:
					if t.name.endswith('.html'):
						ret = t.as_string()
						break
		elif self.path.startswith('/bpy/data/objects/'):
			name = self.path.split('/')[-1]
			if name in bpy.data.objects:
				ret = str(bpy.data.objects[name])
		elif os.path.isfile(self.path[1:]): # the .wasm file
			ret = open(self.path[1:], 'rb').read()
		elif self.path.endswith('.glb'):
			bpy.ops.object.select_all(action='DESELECT')
			name = self.path.split('/')[-1][: -len('.glb') ]
			if name in bpy.data.objects:
				ob = bpy.data.objects[name]
				ob.select_set(True)
				tmp = '/tmp/__httpd__.glb'
				bpy.ops.export_scene.gltf(filepath=tmp, export_selected = True)
				ret = open(tmp,'rb').read()

		if ret is None:
			ret = 'None?'
		if type(ret) is not bytes:
			ret = ret.encode('utf-8')

		self.send_header("Content-Length", str(len(ret)))
		self.end_headers()

		try:
			self.wfile.write( ret )
		except BrokenPipeError:
			print('CLIENT WRITE ERROR: failed bytes', len(ret))


httpd = HTTPServer(('localhost', LOCALHOST_PORT), BlenderServer)
httpd.timeout=0.1
print(httpd)

timer = None

@bpy.utils.register_class
class HttpServerOperator (bpy.types.Operator):
	"HolyBlender HTTP Server"
	bl_idname = "httpd.run"
	bl_label = "httpd"
	bl_options = {'REGISTER'}
	def modal(self, context, event):
		if event.type == "TIMER":
			if HTTPD_ACTIVE:
				httpd.handle_request() # this blocks for a short time
		return {'PASS_THROUGH'} # will not supress event bubbles

	def invoke (self, context, event):
		global timer
		if timer is None:
			timer = self._timer = context.window_manager.event_timer_add(
				time_step=0.016666667,
				window=context.window
			)
			context.window_manager.modal_handler_add(self)
			return {'RUNNING_MODAL'}
		return {'FINISHED'}

	def execute (self, context):
		return self.invoke(context, None)

HTTPD_ACTIVE = True
bpy.ops.httpd.run()
'''
MATERIAL_TEMPLATE = '    - {fileID: ꗈ0, guid: ꗈ1, type: 2}'
COMPONENT_TEMPLATE = '    - component: {fileID: ꗈ}'
CHILD_TRANSFORM_TEMPLATE = '    - {fileID: ꗈ}'
SCENE_ROOT_TEMPLATE = CHILD_TRANSFORM_TEMPLATE
WATTS_TO_CANDELAS = 0.001341022
PI = 3.141592653589793
UNITY_SCRIPTS_PATH = os.path.join(__thisdir, 'Unity Scripts')
TEMPLATES_PATH = os.path.join(__thisdir, 'Templates')
TEMPLATE_REGISTRY_PATH = os.path.join(TEMPLATES_PATH, 'registry.json')
REGISTRY_PATH = '/tmp/registry.json'
MAX_SCRIPTS_PER_OBJECT = 16
unrealCodePath = ''
unrealCodePathSuffix = '/Source/'
excludeItems = [ '/Library' ]
lastId = 5
operatorContext = None
currentTextBlock = None
mainClassNames = []
attachedUnityScriptsDict = {}
attachedBevyScriptsDict = {}
attachedUnrealScriptsDict = {}
previousRunningScripts = []
textBlocksTextsDict = {}
previousTextBlocksTextsDict = {}
propertiesDefaultValuesDict = {}
propertiesTypesDict = {}
childrenDict = {}

class WorldPanel (bpy.types.Panel):
	bl_idname = 'WORLD_PT_World_Panel'
	bl_label = 'HolyBlender Export'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'world'

	def draw(self, context):
		self.layout.prop(context.world, 'unity_project_import_path')
		self.layout.prop(context.world, 'unity_project_export_path')
		self.layout.prop(context.world, 'unrealExportPath')
		self.layout.prop(context.world, 'bevy_project_path')
		self.layout.prop(context.world, 'htmlExportPath')
		self.layout.prop(context.world, 'html_code')
		self.layout.operator(UnrealExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(BevyExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(UnityExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(HTMLExportButton.bl_idname, icon='CONSOLE')
		self.layout.operator(PlayButton.bl_idname, icon='CONSOLE')

class UnityScriptsPanel (bpy.types.Panel):
	bl_idname = 'OBJECT_PT_Unity_Scripts_Panel'
	bl_label = 'HolyBlender Unity Scripts'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'

	def draw(self, context):
		self.layout.label(text='Attach Unity scripts')
		foundUnassignedScript = False
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			hasProperty = getattr(context.active_object, 'unity_script' + str(i)) != None
			if hasProperty or not foundUnassignedScript:
				self.layout.prop(context.active_object, 'unity_script' + str(i))
			if not foundUnassignedScript:
				foundUnassignedScript = not hasProperty

class BevyScriptsPanel (bpy.types.Panel):
	bl_idname = 'OBJECT_PT_bevy_Scripts_Panel'
	bl_label = 'HolyBlender Bevy Scripts'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'

	def draw(self, context):
		self.layout.label(text='Attach bevy scripts')
		foundUnassignedScript = False
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			hasProperty = getattr(context.active_object, 'bevy_script' + str(i)) != None
			if hasProperty or not foundUnassignedScript:
				self.layout.prop(context.active_object, 'bevy_script' + str(i))
			if not foundUnassignedScript:
				foundUnassignedScript = not hasProperty

class UnrealScriptsPanel (bpy.types.Panel):
	bl_idname = 'OBJECT_PT_Unreal_Scripts_Panel'
	bl_label = 'HolyBlender Unreal Scripts'
	bl_space_type = 'PROPERTIES'
	bl_region_type = 'WINDOW'
	bl_context = 'object'

	def draw(self, context):
		self.layout.label(text='Attach Unreal scripts')
		foundUnassignedScript = False
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			hasProperty = getattr(context.active_object, 'unreal_script' + str(i)) != None
			if hasProperty or not foundUnassignedScript:
				self.layout.prop(context.active_object, 'unreal_script' + str(i))
			if not foundUnassignedScript:
				foundUnassignedScript = not hasProperty

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
	bl_label = 'HolyBlender Templates'

	def draw (self, context):
		layout = self.layout
		for name in EXAMPLES_DICT:
			op = layout.operator('u2m.show_template', text=name)
			op.template = name

class AttachedObjectsMenu (bpy.types.Menu):
	bl_idname = 'TEXT_MT_u2m_menu_obj'
	bl_label = 'HolyBlender Attached Objects'

	def draw (self, context):
		layout = self.layout
		if not context.edit_text:
			layout.label(text='No text block')
			return
		objs = []
		for obj in bpy.data.objects:
			attachedScripts = attachedUnityScriptsDict.get(obj, [])
			if context.edit_text.name in attachedScripts:
				objs.append(obj)
			attachedScripts = attachedBevyScriptsDict.get(obj, [])
			if context.edit_text.name in attachedScripts:
				objs.append(obj)
			attachedScripts = attachedUnrealScriptsDict.get(obj, [])
			if context.edit_text.name in attachedScripts:
				objs.append(obj)
		if objs:
			for obj in objs:
				layout.label(text=obj.name)
		else:
			layout.label(text='Script not attached to any objects')

class PlayButton (bpy.types.Operator):
	bl_idname = 'blender.play'
	bl_label = 'Start Playing (Unfinished)'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		for textBlock in bpy.data.texts:
			textBlock.run_cs = True

class HTMLExportButton (bpy.types.Operator):
	bl_idname = 'html.export'
	bl_label = 'Export To HTML'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		htmlExportPath = os.path.expanduser(context.scene.world.htmlExportPath)
		previousVisibleObjects = []
		for obj in bpy.data.objects:
			if obj.type == 'MESH' and not obj.hide_get():
				previousVisibleObjects.append(obj)
				obj.hide_render = True
		bpy.context.scene.render.resolution_percentage = 10
		camera = bpy.data.cameras[0]
		cameraObj = bpy.data.objects[camera.name]
		bpy.ops.object.select_all(action='DESELECT')
		bpy.context.view_layer.objects.active = cameraObj
		cameraObj.select_set(True)
		preivousAreaType = bpy.context.area.type
		bpy.context.area.type = 'VIEW_3D'
		bpy.ops.view3d.object_as_camera()
		bpy.context.area.type = preivousAreaType
		bpy.context.scene.render.film_transparent = True
		bpy.context.scene.render.image_settings.color_mode = 'RGBA'
		previousCameraLocation = cameraObj.location
		previousCameraRotationMode = cameraObj.rotation_mode
		cameraObj.rotation_mode = 'XYZ'
		previousCameraRotation = cameraObj.rotation_euler
		previousCameraType = camera.type
		camera.type = 'ORTHO'
		previousCameraOrthoScale = camera.ortho_scale

		html = [
			'<!DOCTYPE html>',
			'<html><head><script>',
		]

		js_blocks = {}
		imgs = []
		for obj in bpy.data.objects:
			if obj.type == 'MESH':
				obj.hide_render = False
				bpy.context.scene.render.filepath = htmlExportPath + '/' + obj.name
				cameraObj.rotation_euler = mathutils.Vector((math.radians(90), 0, 0))
				bounds = GetObjectBounds(obj)
				cameraObj.location = bounds[0] - mathutils.Vector((0, bounds[1].y, 0))
				camera.ortho_scale = max(bounds[1].x, bounds[1].z) * 2
				if os.path.isfile( htmlExportPath + '/' + obj.name ):
					pass
				else:
					bpy.ops.render.render(animation=False, write_still=True)
				obj.hide_render = True
				imagePath = bpy.context.scene.render.filepath + '.png'
				command = [ 'convert', '-delay', '10', '-loop', '0', imagePath, imagePath.replace('.png', '.gif') ]
				subprocess.check_call(command)
				imagePath = imagePath.replace('.png', '.gif')
				cameraSize = mathutils.Vector((camera.sensor_width, camera.sensor_height))
				imageData = open(imagePath, 'rb').read()
				base64EncodedStr = base64.b64encode(imageData).decode('utf-8')
				multiplyUnits = 256
				zindex = int(bounds[0].y)
				zindex += 10
				if zindex < 0: zindex = 0
				onclick =  ''
				if obj.html_on_click:
					fname = '__on_click_' + obj.html_on_click.name.replace('.','_')
					if obj.html_on_click.name not in js_blocks:
						js = 'function %s(){%s}' % (fname, obj.html_on_click.as_string())
						js_blocks[obj.html_on_click.name] = js
					onclick = 'javascript:%s()' % fname
				user_css = ''
				if obj.html_css:
					user_css = obj.html_css.as_string().replace('\n', ' ').strip()
				imageText = '<img id="%s" onclick="%s" style="position:fixed; left:%spx; top:%spx; z-index:%s;%s" src="data:image/gif;base64,%s">\n' %(
					obj.name,
					onclick,
					bounds[0].x * multiplyUnits,
					-bounds[0].z * multiplyUnits,
					zindex,
					user_css,
					base64EncodedStr
				)
				imgs.append(imageText)
		for obj in previousVisibleObjects:
			obj.hide_render = False
		cameraObj.location = previousCameraLocation
		cameraObj.rotation_mode = previousCameraRotationMode
		cameraObj.rotation_euler = previousCameraRotation
		camera.type = previousCameraType
		camera.ortho_scale = previousCameraOrthoScale

		for tname in js_blocks:
			html.append('//'+tname)
			html.append(js_blocks[tname])

		html.append('</script>')
		html.append('<body>')
		html += imgs
		html.append('</body></html>')
		htmlText = '\n'.join(html)
		open(htmlExportPath + '/index.html', 'wb').write(htmlText.encode('utf-8'))
		if '__index__.html' not in bpy.data.texts: bpy.data.texts.new(name='__index__.html')
		bpy.data.texts['__index__.html'].from_string(htmlText)
		if bpy.data.worlds[0].holyserver:
			scope = globals()
			exec(bpy.data.worlds[0].holyserver.as_string(), scope, scope)
			webbrowser.open('http://localhost:8000/')
		else:
			webbrowser.open(htmlExportPath + '/index.html')
		return {'FINISHED'}

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
						data += GetObjectsData(collection.objects) + '\n'
			data += '\nScenes\n'
			for scene in bpy.data.scenes:
				data += GetObjectsData(scene.objects) + '\n'
			data += 'Children\n'
			data += GetObjectsData(childrenDict) + '\n'
			data += '\nScripts'
			for obj in attachedUnrealScriptsDict:
				if len(attachedUnrealScriptsDict[obj]) > 0:
					data += '\n' + GetBasicObjectData(obj) + '☣️' + '☣️'.join(attachedUnrealScriptsDict[obj]) + '\n'
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

class BevyExportButton (bpy.types.Operator):
	bl_idname = 'bevy.export'
	bl_label = 'Export To Bevy'

	@classmethod
	def poll (cls, context):
		return True
	
	def execute (self, context):
		# BuildTool ('UnityToBevy')
		bevyExportPath = os.path.expanduser(context.scene.world.bevy_project_path)
		if not os.path.isdir(bevyExportPath):
			MakeFolderForFile (bevyExportPath + '/')
		importPath = os.path.expanduser(context.scene.world.unity_project_import_path)
		if importPath != '':
			command = [ 'python3', os.path.expanduser('~/HolyBlender/UnityToBevy.py'), 'input=' + importPath, 'output=' + bevyExportPath, 'exclude=/Library', 'webgl' ]
			print(command)

			subprocess.check_call(command)

		else:
			data = bevyExportPath
			for obj in attachedBevyScriptsDict:
				data += '\n' + obj.name + '☢️' + '☣️'.join(attachedBevyScriptsDict[obj])
			open('/tmp/HolyBlender Data (BlenderToBevy)', 'wb').write(data.encode('utf-8'))
			import MakeBevyBlenderApp as makeBevyBlenderApp
			makeBevyBlenderApp.Do (attachedBevyScriptsDict)
			# webbrowser.open('http://localhost:1334')

class UnityExportButton (bpy.types.Operator):
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
					material = open(os.path.expanduser('~/HolyBlender/Templates/Material.mat'), 'rb').read().decode('utf-8')
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
			MakeFolderForFile (os.path.join(projectExportPath, 'Assets', 'Editor', ''))

			os.system('cp ' + os.path.join(UNITY_SCRIPTS_PATH, 'GetUnityProjectInfo.cs') + ' ' + os.path.join(projectExportPath, 'Assets', 'Editor', 'GetUnityProjectInfo.cs'))
			os.system('cp ' + os.path.expanduser('~/HolyBlender/SystemExtensions.cs') + ' ' + projectExportPath + '/Assets/Editor/SystemExtensions.cs')

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
		sceneTemplateText = open(os.path.expanduser('~/HolyBlender/Templates/Scene.unity'), 'rb').read().decode('utf-8')
		gameObjectsAndComponentsText = ''
		transformIds = []
		for obj in bpy.data.objects:
			MakeUnityObject (obj)
		scriptsFolder = os.path.join(projectExportPath, 'Assets', 'Scripts')
		MakeFolderForFile (os.path.join(projectExportPath, 'Assets', 'Scripts', ''))
		sendAndRecieveClickEventsScriptPath = os.path.join(scriptsFolder, 'SendAndRecieveClickEvents.cs')

		os.system('cp ' + os.path.join(UNITY_SCRIPTS_PATH, 'SendAndRecieveClickEvents.cs') + ' ' + sendAndRecieveClickEventsScriptPath)

		gameObjectIdAndTransformId = MakeEmptyUnityObject('Send And Recieve Click Events')
		script = SCRIPT_TEMPLATE
		script = script.replace(REPLACE_INDICATOR + '0', str(lastId))
		script = script.replace(REPLACE_INDICATOR + '1', str(gameObjectIdAndTransformId[0]))
		sendAndRecieveClickEventsScriptMetaPath = sendAndRecieveClickEventsScriptPath + '.meta'
		scriptGuid = GetGuid(sendAndRecieveClickEventsScriptMetaPath)
		scriptMeta = SCRIPT_META_TEMPLATE
		scriptMeta += scriptGuid
		open(sendAndRecieveClickEventsScriptMetaPath, 'wb').write(scriptMeta.encode('utf-8'))
		script = script.replace(REPLACE_INDICATOR + '2', scriptGuid)
		gameObjectsAndComponentsText += script + '\n'
		componentIds.append(lastId)
		lastId += 1
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

def MakeEmptyUnityObject (name : str, layer = 0, parentTransformId = 0) -> (int, int):
	global lastId
	global transformIds
	global gameObjectsAndComponentsText
	gameObject = GAME_OBJECT_TEMPLATE
	gameObject = gameObject.replace(REPLACE_INDICATOR + '0', str(lastId))
	gameObject = gameObject.replace(REPLACE_INDICATOR + '1', str(lastId + 1))
	gameObject = gameObject.replace(REPLACE_INDICATOR + '3', str(layer))
	gameObject = gameObject.replace(REPLACE_INDICATOR + '4', name)
	gameObjectsAndComponentsText += gameObject + '\n'
	gameObjectId = lastId
	lastId += 1
	transform = TRANSFORM_TEMPLATE
	transform = transform.replace(REPLACE_INDICATOR + '10', str(obj.scale.z))
	transform = transform.replace(REPLACE_INDICATOR + '11', str(obj.scale.y))
	transform = transform.replace(REPLACE_INDICATOR + '12', '[]')
	transform = transform.replace(REPLACE_INDICATOR + '13', str(parentTransformId))
	transform = transform.replace(REPLACE_INDICATOR + '0', str(lastId))
	transform = transform.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
	transform = transform.replace(REPLACE_INDICATOR + '2', '0')
	transform = transform.replace(REPLACE_INDICATOR + '3', '0')
	transform = transform.replace(REPLACE_INDICATOR + '4', '0')
	transform = transform.replace(REPLACE_INDICATOR + '5', '0')
	transform = transform.replace(REPLACE_INDICATOR + '6', '0')
	transform = transform.replace(REPLACE_INDICATOR + '7', '0')
	transform = transform.replace(REPLACE_INDICATOR + '8', '0')
	transform = transform.replace(REPLACE_INDICATOR + '9', '1')
	gameObjectsAndComponentsText += transform + '\n'
	transformIds.append(lastId)
	lastId += 1
	return (gameObjectId, transformId)

def MakeUnityObject (obj, parentTransformId = 0) -> int:
	global lastId
	global transformIds
	global gameObjectsAndComponentsText
	componentIds = []
	gameObject = GAME_OBJECT_TEMPLATE
	gameObject = gameObject.replace(REPLACE_INDICATOR + '0', str(lastId))
	gameObject = gameObject.replace(REPLACE_INDICATOR + '1', str(lastId + 1))
	gameObject = gameObject.replace(REPLACE_INDICATOR + '3', '0')
	gameObject = gameObject.replace(REPLACE_INDICATOR + '4', obj.name)
	gameObjectsAndComponentsText += gameObject + '\n'
	gameObjectId = lastId
	lastId += 1
	transform = TRANSFORM_TEMPLATE
	transform = transform.replace(REPLACE_INDICATOR + '10', str(obj.scale.z))
	transform = transform.replace(REPLACE_INDICATOR + '11', str(obj.scale.y))
	myTransformId = lastId
	children = ''
	for childObj in obj.children:
		transformId = MakeUnityObject(child, lastId)
		children += '\n' + CHILD_TRANSFORM_TEMPLATE.replace(REPLACE_INDICATOR, transformId)
	meshFileId = '10202'
	meshGuid = ''
	if obj.type == 'MESH':
		filePath = projectExportPath + '/Assets/Art/Models/' + obj.data.name + '.fbx.meta'
		meshGuid = GetGuid(filePath)
		open(filePath, 'wb').write(MESH_META_TEMPLATE.replace(REPLACE_INDICATOR, meshGuid).encode('utf-8'))
		if unityVersionPath != '':
			dataText = open('/tmp/HolyBlender Data (BlenderToUnity)', 'rb').read().decode('utf-8')
			fileIdIndicator = '-' + projectExportPath + '/Assets/Art/Models/' + obj.data.name + '.fbx'
			indexOfFile = dataText.find(fileIdIndicator)
			indexOfFileId = indexOfFile + len(fileIdIndicator) + 1
			indexOfEndOfFileId = dataText.find(' ', indexOfFileId)
			meshFileId = dataText[indexOfFileId : indexOfEndOfFileId]
		gameObjectIdAndTransformId = MakeClickableChild(obj.name, meshFileId, meshGuid, myTransformId)
		children += '\n' + CHILD_TRANSFORM_TEMPLATE.replace(REPLACE_INDICATOR, gameObjectIdAndTransformId[1])
	elif len(obj.children) == 0:
		children = '[]'
	transform = transform.replace(REPLACE_INDICATOR + '12', children)
	transform = transform.replace(REPLACE_INDICATOR + '13', str(parentTransformId))
	transform = transform.replace(REPLACE_INDICATOR + '0', str(myTransformId))
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
	transformIds.append(myTransformId)
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
		meshFilter = meshFilter.replace(REPLACE_INDICATOR + '2', meshFileId)
		meshFilter = meshFilter.replace(REPLACE_INDICATOR + '3', meshGuid)
		gameObjectsAndComponentsText += meshFilter + '\n'
		componentIds.append(lastId)
		lastId += 1
		for modifier in obj.modifiers:
			if modifier.type == 'COLLISION':
				AddMeshCollider (gameObjectId, False, False, meshFileId, meshGuid)
				break
		if obj.rigid_body != None:
			rigidbody = RIGIDBODY_TEMPLATE
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '0', str(lastId))
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '2', str(obj.rigid_body.mass))
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '3', str(obj.rigid_body.linear_damping))
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '4', str(obj.rigid_body.angular_damping))
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '5', '1')
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '6', str(int(obj.rigid_body.enabled)))
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '7', '0')
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '8', '0')
			rigidbody = rigidbody.replace(REPLACE_INDICATOR + '9', '0')
			gameObjectsAndComponentsText += rigidbody + '\n'
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
				dataText = open('/tmp/HolyBlender Data (BlenderToUnity)', 'rb').read().decode('utf-8')
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
	attachedScripts = attachedUnityScriptsDict.get(obj, [])
	for scriptName in attachedScripts:
		script = SCRIPT_TEMPLATE
		script = script.replace(REPLACE_INDICATOR + '0', str(lastId))
		script = script.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
		filePath = projectExportPath + '/Assets/Standard Assets/Scripts/' + scriptName
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
		scriptMeta = SCRIPT_META_TEMPLATE
		scriptMeta += scriptGuid
		open(filePath, 'wb').write(scriptMeta.encode('utf-8'))
		script = script.replace(REPLACE_INDICATOR + '2', scriptGuid)
		gameObjectsAndComponentsText += script + '\n'
		componentIds.append(lastId)
		lastId += 1
	indexOfComponentsList = gameObjectsAndComponentsText.find(REPLACE_INDICATOR + '2')
	for componentId in componentIds:
		component = COMPONENT_TEMPLATE
		component = component.replace(REPLACE_INDICATOR, str(componentId))
		gameObjectsAndComponentsText = gameObjectsAndComponentsText[: indexOfComponentsList] + component + '\n' + gameObjectsAndComponentsText[indexOfComponentsList :]
		gameObjectsAndComponentsText = gameObjectsAndComponentsText.replace(REPLACE_INDICATOR + '2', '')
	return transformId

def AddMeshCollider (gameObjectId : int, isTirgger : bool, isConvex : bool, fileId : str, meshGuid : str):
	meshCollider = MESH_COLLIDER_TEMPLATE
	meshCollider = meshCollider.replace(REPLACE_INDICATOR + '0', str(lastId))
	meshCollider = meshCollider.replace(REPLACE_INDICATOR + '1', str(gameObjectId))
	meshCollider = meshCollider.replace(REPLACE_INDICATOR + '2', str(int(isTirgger)))
	meshCollider = meshCollider.replace(REPLACE_INDICATOR + '3', str(int(isConvex)))
	meshCollider = meshCollider.replace(REPLACE_INDICATOR + '4', fileId)
	meshCollider = meshCollider.replace(REPLACE_INDICATOR + '5', meshGuid)
	gameObjectsAndComponentsText += meshCollider + '\n'
	componentIds.append(lastId)
	lastId += 1

def MakeClickableChild (name : str, fileId : str, meshGuid : str, parentTransformId = 0) -> (int, int):
	gameObjectIdAndTransformId = MakeEmptyUnityObject(name, 31, parentTransformId)
	AddMeshCollider (gameObjectIdAndTransformId[0], True, False, fileId, meshGuid)
	return gameObjectIdAndTransformId

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

class BevyTranslateButton (bpy.types.Operator):
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
		return {'PASS_THROUGH'} # Won't supress event bubbles

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
	UnrealExportButton,
	BevyExportButton,
	UnityExportButton,
	HTMLExportButton,
	PlayButton,
	UnrealTranslateButton,
	BevyTranslateButton,
	ExamplesOperator,
	ExamplesMenu,
	AttachedObjectsMenu,
	Loop,
	UnityScriptsPanel,
	BevyScriptsPanel,
	UnrealScriptsPanel,
	WorldPanel
]

def BuildTool (toolName : str):
	command = [ 'make', 'build_' + toolName ]
	print(command)

	subprocess.check_call(command)

def ExportMesh (obj):
	meshAssetPath = '/tmp/' + obj.name.replace(' ', '_') + '.fbx'
	bpy.ops.object.select_all(action='DESELECT')
	bpy.context.view_layer.objects.active = obj
	obj.select_set(True)
	bpy.ops.export_scene.fbx(filepath=meshAssetPath, use_selection=True, use_custom_props=True, mesh_smooth_type='FACE')

def GetObjectBounds (obj) -> (mathutils.Vector, mathutils.Vector):
	_min = mathutils.Vector((float('inf'), float('inf'), float('inf')))
	_max = mathutils.Vector((float('-inf'), float('-inf'), float('-inf')))
	if obj.type == 'MESH':
		for vertex in obj.data.vertices:
			_min.x = min((obj.matrix_world @ vertex.co).x, _min.x)
			_min.y = min((obj.matrix_world @ vertex.co).y, _min.y)
			_min.z = min((obj.matrix_world @ vertex.co).z, _min.z)
			_max.x = max((obj.matrix_world @ vertex.co).x, _max.x)
			_max.y = max((obj.matrix_world @ vertex.co).y, _max.y)
			_max.z = max((obj.matrix_world @ vertex.co).z, _max.z)
	else:
		print('GetObjectBounds is not implemented for object types besides meshes')
	return ((_min + _max) / 2, _max - _min)

def GetObjectsData (objectGroup):
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
			ExportMesh (obj)
			data += '\n' + GetBasicObjectData(obj)
			if obj.rigid_body != None:
				data += '☣️' + str(obj.rigid_body.mass) + '☣️' + str(obj.rigid_body.linear_damping) + '☣️' + str(obj.rigid_body.angular_damping) + '☣️' + str(obj.rigid_body.enabled)
			for modifier in obj.modifiers:
				if modifier.type == 'COLLISION':
					data += '☣️True'
					break
	return data

def GetBasicObjectData (obj):
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

def ConvertCSFileToRust (filePath):
	global mainClassName
	mainClassName = filePath[filePath.rfind('/') + 1 : filePath.rfind('.')]
	assert os.path.isfile(filePath)
	MakeFolderForFile ('/tmp/src/main.rs')
	MakeFolderForFile ('/tmp/assets/registry.json')
	data = 'output=/tmp\n' + filePath
	open('/tmp/HolyBlender Data (UnityToBevy)', 'wb').write(data.encode('utf-8'))
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
	
	data = open('/tmp/HolyBlender Data (UnityToBevy)', 'rb').read().decode('utf-8')
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

def DrawUnrealTranslateButton (self, context):
	self.layout.operator(UnrealTranslateButton.bl_idname, icon='CONSOLE')

def DrawBevyTranslateButton (self, context):
	self.layout.operator(BevyTranslateButton.bl_idname, icon='CONSOLE')

def SetupTextEditorFooterContext (self, context):
	global currentTextBlock
	global previousRunningScripts
	currentTextBlock = context.edit_text
	previousRunningScripts = []
	for textBlock in bpy.data.texts:
		if textBlock.run_cs and textBlock.name != '.gltf_auto_export_gltf_settings':
			previousRunningScripts.append(textBlock.name)

def DrawRunCSToggle (self, context):
	self.layout.prop(context.edit_text, 'run_cs')

def DrawIsInitScriptToggle (self, context):
	self.layout.prop(context.edit_text, 'is_init_script')

def OnUpdateUnityScripts (self, context):
	attachedScripts = []
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		script = getattr(self, 'unity_script' + str(i))
		if script != None:
			attachedScripts.append(script.name)
	attachedUnityScriptsDict[self] = attachedScripts

def OnUpdateBevyScripts (self, context):
	attachedScripts = []
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		script = getattr(self, 'bevy_script' + str(i))
		if script != None:
			attachedScripts.append(script.name)
	attachedBevyScriptsDict[self] = attachedScripts

def OnUpdateUnrealScripts (self, context):
	attachedScripts = []
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		script = getattr(self, 'unreal_script' + str(i))
		if script != None:
			attachedScripts.append(script.name)
	attachedUnrealScriptsDict[self] = attachedScripts

def UpdateInspectorFields (textBlock):
	global attachedUnityScriptsDict
	global propertiesTypesDict
	global propertiesDefaultValuesDict
	text = textBlock.as_string()
	publicIndicator = 'public '
	indexOfPublicIndicator = text.find(publicIndicator)
	while indexOfPublicIndicator != -1:
		indexOfType = indexOfPublicIndicator + len(publicIndicator)
		if text[indexOfType :].startswith('class '):
			indexOfPublicIndicator = text.find(publicIndicator, indexOfType)
			continue
		indexOfVariableName = indexOfType
		while indexOfVariableName < len(text) - 1:
			indexOfVariableName += 1
			if text[indexOfVariableName] != ' ':
				break
		if text[indexOfVariableName + 1] == '(':
			indexOfPublicIndicator = text.find(publicIndicator, indexOfType)
			continue
		indexOfVariableName = text.find(' ', indexOfVariableName + 1)
		type = text[indexOfType : indexOfVariableName]
		indexOfPotentialEndOfVariable = IndexOfAny(text, [ ' '  ';' , '=' ], indexOfVariableName + 1)
		variableName = text[indexOfVariableName : indexOfPotentialEndOfVariable]
		variableName = variableName.strip()
		shouldBreak = False
		for obj in attachedUnityScriptsDict.keys():
			for attachedScript in attachedUnityScriptsDict[obj]:
				if attachedScript == textBlock.name:
					value = ''
					isSetToValue = False
					if text[indexOfPotentialEndOfVariable] == '=':
						indexOfSemicolon = text.find(';', indexOfPotentialEndOfVariable + 1)
						value = text[indexOfPotentialEndOfVariable + 1 : indexOfSemicolon]
						value = value.strip()
						isSetToValue = True
					if type == 'int':
						if not isSetToValue:
							value = 0
						else:
							value = int(value)
					elif type == 'float' or type == 'double':
						if not isSetToValue:
							value = 0.0
						else:
							value = value.replace('f', '')
							value = float(value)
					elif type == 'bool':
						if not isSetToValue:
							value = False
						elif value == 'true':
							value = True
						else:
							value = False
					attachedScript = attachedScript.replace('.cs', '')
					attachedScript = attachedScript.replace('.cpp', '')
					attachedScript = attachedScript.replace('.h', '')
					propertyName = variableName + '_' + attachedScript
					if propertyName not in obj.keys():
						obj[propertyName] = value
						propertiesDefaultValuesDict[variableName] = value
					else:
						propertiesDefaultValuesDict[variableName] = obj[propertyName]
					propertiesTypesDict[variableName] = type
					shouldBreak = True
					break
			if shouldBreak:
				break
		indexOfPublicIndicator = text.find(publicIndicator, indexOfType)

def OnRedrawView ():
	global currentTextBlock
	global textBlocksTextsDict
	global attachedUnityScriptsDict
	global previousRunningScripts
	global previousTextBlocksTextsDict
	textBlocksTextsDict = {}
	for textBlock in bpy.data.texts:
		if textBlock.name == '.gltf_auto_export_gltf_settings':
			continue
		textBlocksTextsDict[textBlock.name] = textBlock.as_string()
		if textBlock.name not in previousTextBlocksTextsDict or previousTextBlocksTextsDict[textBlock.name] != textBlock.as_string():
			UpdateInspectorFields (textBlock)
	previousTextBlocksTextsDict = textBlocksTextsDict.copy()
	bpy.types.TEXT_HT_footer.remove(SetupTextEditorFooterContext)
	bpy.types.TEXT_HT_footer.append(SetupTextEditorFooterContext)
	if currentTextBlock != None:
		if currentTextBlock.run_cs:
			import RunCSInBlender as runCSInBlender
			for obj in attachedUnityScriptsDict:
				if currentTextBlock.name in attachedUnityScriptsDict[obj]:
					filePath = os.path.expanduser('/tmp/HolyBlender Data (UnityInBlender)/' + currentTextBlock.name)
					filePath = filePath.replace('.cs', '.py')
					if not filePath.endswith('.py'):
						filePath += '.py'
					if currentTextBlock.name not in previousRunningScripts:
						MakeFolderForFile (filePath)
						open(filePath, 'wb').write(currentTextBlock.as_string().encode('utf-8'))
						BuildTool ('UnityInBlender')
						command = [
							'dotnet',
							os.path.expanduser('~/HolyBlender/UnityInBlender/HolyBlender.dll'), 
							'includeFile=' + filePath,
							'output=/tmp/HolyBlender Data (UnityInBlender)'
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
	# blf.draw(id, 'Hello World!')

def register ():
	global attachedUnityScriptsDict
	MakeFolderForFile ('/tmp/')
	registryText = open(TEMPLATE_REGISTRY_PATH, 'rb').read().decode('utf-8')
	registryText = registryText.replace('ꗈ', '')
	open(REGISTRY_PATH, 'wb').write(registryText.encode('utf-8'))
	registry = bpy.context.window_manager.components_registry
	registry.schemaPath = REGISTRY_PATH
	bpy.ops.object.reload_registry()

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
		default = '~/TestUnityProject'
	)
	# bpy.types.World.unity_export_version = bpy.props.StringProperty(
	# 	name = 'Unity export version',
	# 	description = '',
	# 	default = ''
	# )
	bpy.types.World.unrealExportPath = bpy.props.StringProperty(
		name = 'Unreal project path',
		description = '',
		default = '~/TestUnrealProject'
	)
	bpy.types.World.bevy_project_path = bpy.props.StringProperty(
		name = 'Bevy project path',
		description = '',
		default = '~/TestBevyProject'
	)
	bpy.types.World.htmlExportPath = bpy.props.StringProperty(
		name = 'HTML project path',
		description = '',
		default = '~/TestHtmlProject'
	)

	bpy.types.World.holyserver = bpy.props.PointerProperty(name='Python Server', type=bpy.types.Text)
	bpy.types.World.html_code = bpy.props.PointerProperty(name='HTML code', type=bpy.types.Text)
	bpy.types.Object.html_on_click = bpy.props.PointerProperty(name='JavaScript on click', type=bpy.types.Text)
	bpy.types.Object.html_css = bpy.props.PointerProperty(name='CSS', type=bpy.types.Text)

	bpy.types.Text.run_cs = bpy.props.BoolProperty(
		name = 'Run C# Script',
		description = ''
	)
	bpy.types.Text.is_init_script = bpy.props.BoolProperty(
		name = 'Is Initialization Script',
		description = ''
	)
	bpy.types.TEXT_HT_header.append(DrawExamplesMenu)
	bpy.types.TEXT_HT_header.append(DrawAttachedObjectsMenu)
	bpy.types.TEXT_HT_footer.append(DrawUnrealTranslateButton)
	bpy.types.TEXT_HT_footer.append(DrawBevyTranslateButton)
	bpy.types.TEXT_HT_footer.append(DrawRunCSToggle)
	bpy.types.TEXT_HT_footer.append(DrawIsInitScriptToggle)
	for i in range(MAX_SCRIPTS_PER_OBJECT):
		setattr(bpy.types.Object, 'unity_script' + str(i), bpy.props.PointerProperty(name='Attach Unity script', type=bpy.types.Text, update=OnUpdateUnityScripts))
		setattr(bpy.types.Object, 'bevy_script' + str(i), bpy.props.PointerProperty(name='Attach bevy script', type=bpy.types.Text, update=OnUpdateBevyScripts))
		setattr(bpy.types.Object, 'unreal_script' + str(i), bpy.props.PointerProperty(name='Attach Unreal script', type=bpy.types.Text, update=OnUpdateUnrealScripts))
	for obj in bpy.data.objects:
		attachedScripts = []
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			script = getattr(obj, 'unity_script' + str(i))
			if script != None:
				attachedScripts.append(script.name)
		attachedUnityScriptsDict[obj] = attachedScripts
		attachedScripts = []
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			script = getattr(obj, 'bevy_script' + str(i))
			if script != None:
				attachedScripts.append(script.name)
		attachedBevyScriptsDict[obj] = attachedScripts
		attachedScripts = []
		for i in range(MAX_SCRIPTS_PER_OBJECT):
			script = getattr(obj, 'unreal_script' + str(i))
			if script != None:
				attachedScripts.append(script.name)
		attachedUnrealScriptsDict[obj] = attachedScripts
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
	bpy.types.TEXT_HT_footer.remove(DrawIsInitScriptToggle)
	for cls in classes:
		bpy.utils.unregister_class(cls)

def InitTexts ():
	if bpy.data.worlds[0].html_code is None:
		textBlock = bpy.data.texts.new(name='__Html__.html')
		textBlock.from_string(INIT_HTML)
		bpy.data.worlds[0].html_code = textBlock
	if '__Server__.py' not in bpy.data.texts:
		textBlock = bpy.data.texts.new(name='__Server__.py')
		textBlock.from_string(BLENDER_SERVER)

if __name__ == '__main__':
	register ()
	InitTexts ()
	if user_args:
		for arg in user_args:
			if arg.endswith('.py'):
				print('exec:', arg)
				exec(open(arg).read())
