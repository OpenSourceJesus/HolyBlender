#pragma warning disable 168, 618
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using TriLibCore.Mappers;
using TriLibCore.Utils;
using UnityEngine;
using FileMode = System.IO.FileMode;
using HumanDescription = UnityEngine.HumanDescription;
using Object = UnityEngine.Object;
using System.Collections;
using System.Runtime;
using TriLibCore.Extensions;
using TriLibCore.General;
using TriLibCore.Interfaces;
using TriLibCore.Materials;
using TriLibCore.Textures;
#if TRILIB_DRACO
using TriLibCore.Gltf.Reader;
using TriLibCore.Gltf.Draco;
using TriLibCore.Collections;
#endif
#if UNITY_EDITOR
using UnityEditor;
#endif
namespace TriLibCore
{
    /// <summary>Represents the main class containing methods to load the Models.</summary>
    public static partial class AssetLoader
    {
        /// <summary>
        /// Asset Loader Options validation message.
        /// </summary>
        private const string ValidationMessage = "You can disable these validations in the 'Edit->Project Settings->TriLib' menu.";

        /// <summary>
        /// Constant that defines the namespace used by TriLib Mappers.
        /// </summary>
        private const string TriLibMappersNamespace = "TriLibCore.Mappers";

        /// <summary>Loads a Model from the given path asynchronously.</summary>
        /// <param name="path">The Model file path.</param>
        /// <param name="onLoad">The Method to call on the Main Thread when the Model is loaded but resources may still pending.</param>
        /// <param name="onMaterialsLoad">The Method to call on the Main Thread when the Model and resources are loaded.</param>
        /// <param name="onProgress">The Method to call when the Model loading progress changes.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="haltTask">Turn on this field to avoid loading the model immediately and chain the Tasks.</param>
        /// <param name="onPreLoad">The method to call on the parallel Thread before the Unity objects are created.</param>
        /// <param name="isZipFile">Indicates whether to load from a Zip file.</param>
        /// <returns>The Asset Loader Context, containing Model loading information and the output Game Object.</returns>
        public static AssetLoaderContext LoadModelFromFile(string path,
            Action<AssetLoaderContext> onLoad = null,
            Action<AssetLoaderContext> onMaterialsLoad = null,
            Action<AssetLoaderContext, float> onProgress = null,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            bool haltTask = false,
            Action<AssetLoaderContext> onPreLoad = null,
            bool isZipFile = false)
        {
            var assetLoaderContext = new AssetLoaderContext
            {
                Options = assetLoaderOptions ? assetLoaderOptions : CreateDefaultLoaderOptions(),
                Filename = path,
                BasePath = FileUtils.GetFileDirectory(path),
                WrapperGameObject = wrapperGameObject,
                OnMaterialsLoad = onMaterialsLoad,
                OnLoad = onLoad,
                OnProgress = onProgress,
                HandleError = HandleError,
                OnError = onError,
                OnPreLoad = onPreLoad,
                CustomData = customContextData,
                HaltTasks = haltTask,
#if (UNITY_WEBGL && !TRILIB_ENABLE_WEBGL_THREADS) || (UNITY_WSA && !TRILIB_ENABLE_UWP_THREADS) || TRILIB_FORCE_SYNC
                Async = false,
#else
                Async = true,
#endif
                IsZipFile = isZipFile,
                PersistentDataPath = Application.persistentDataPath
            };
            assetLoaderContext.Setup();
            LoadModelInternal(assetLoaderContext);
            return assetLoaderContext;
        }

        /// <summary>Loads a Model from the given Stream asynchronously.</summary>
        /// <param name="stream">The Stream containing the Model data.</param>
        /// <param name="filename">The Model filename.</param>
        /// <param name="fileExtension">The Model file extension. (Eg.: fbx)</param>
        /// <param name="onLoad">The Method to call on the Main Thread when the Model is loaded but resources may still pending.</param>
        /// <param name="onMaterialsLoad">The Method to call on the Main Thread when the Model and resources are loaded.</param>
        /// <param name="onProgress">The Method to call when the Model loading progress changes.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="haltTask">Turn on this field to avoid loading the model immediately and chain the Tasks.</param>
        /// <param name="onPreLoad">The method to call on the parallel Thread before the Unity objects are created.</param>
        /// <param name="isZipFile">Indicates whether to load from a Zip file.</param>
        /// <returns>The Asset Loader Context, containing Model loading information and the output Game Object.</returns>
        public static AssetLoaderContext LoadModelFromStream(Stream stream,
            string filename = null,
            string fileExtension = null,
            Action<AssetLoaderContext> onLoad = null,
            Action<AssetLoaderContext> onMaterialsLoad = null,
            Action<AssetLoaderContext, float> onProgress = null,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            bool haltTask = false,
            Action<AssetLoaderContext> onPreLoad = null,
            bool isZipFile = false)
        {
            var assetLoaderContext = new AssetLoaderContext
            {
                Options = assetLoaderOptions ? assetLoaderOptions : CreateDefaultLoaderOptions(),
                Stream = stream,
                Filename = filename,
                FileExtension = fileExtension ?? FileUtils.GetFileExtension(filename, false),
                BasePath = FileUtils.GetFileDirectory(filename),
                WrapperGameObject = wrapperGameObject,
                OnMaterialsLoad = onMaterialsLoad,
                OnLoad = onLoad,
                OnProgress = onProgress,
                HandleError = HandleError,
                OnError = onError,
                OnPreLoad = onPreLoad,
                CustomData = customContextData,
                HaltTasks = haltTask,
#if (UNITY_WEBGL && !TRILIB_ENABLE_WEBGL_THREADS) || (UNITY_WSA && !TRILIB_ENABLE_UWP_THREADS) || TRILIB_FORCE_SYNC
                Async = false,
#else
                Async = true,
#endif
                IsZipFile = isZipFile,
                PersistentDataPath = Application.persistentDataPath
            };
            assetLoaderContext.Setup();
            LoadModelInternal(assetLoaderContext);
            return assetLoaderContext;
        }

        /// <summary>Loads a Model from the given path synchronously.</summary>
        /// <param name="path">The Model file path.</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="isZipFile">Indicates whether to load from a Zip file.</param>
        /// <returns>The Asset Loader Context, containing Model loading information and the output Game Object.</returns>
        public static AssetLoaderContext LoadModelFromFileNoThread(string path,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            bool isZipFile = false)
        {
            var assetLoaderContext = new AssetLoaderContext
            {
                Options = assetLoaderOptions ? assetLoaderOptions : CreateDefaultLoaderOptions(),
                Filename = path,
                BasePath = FileUtils.GetFileDirectory(path),
                CustomData = customContextData,
                HandleError = HandleError,
                OnError = onError,
                WrapperGameObject = wrapperGameObject,
                Async = false,
                IsZipFile = isZipFile,
                PersistentDataPath = Application.persistentDataPath
            };
            assetLoaderContext.Setup();
            LoadModelInternal(assetLoaderContext);
            return assetLoaderContext;
        }

        /// <summary>Loads a Model from the given Stream synchronously.</summary>
        /// <param name="stream">The Stream containing the Model data.</param>
        /// <param name="filename">The Model filename.</param>
        /// <param name="fileExtension">The Model file extension. (Eg.: fbx)</param>
        /// <param name="onError">The Method to call on the Main Thread when any error occurs.</param>
        /// <param name="wrapperGameObject">The Game Object that will be the parent of the loaded Game Object. Can be null.</param>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        /// <param name="customContextData">The Custom Data that will be passed along the Context.</param>
        /// <param name="isZipFile">Indicates whether to load from a Zip file.</param>
        /// <returns>The Asset Loader Context, containing Model loading information and the output Game Object.</returns>
        public static AssetLoaderContext LoadModelFromStreamNoThread(Stream stream,
            string filename = null,
            string fileExtension = null,
            Action<IContextualizedError> onError = null,
            GameObject wrapperGameObject = null,
            AssetLoaderOptions assetLoaderOptions = null,
            object customContextData = null,
            bool isZipFile = false)
        {
            var assetLoaderContext = new AssetLoaderContext
            {
                Options = assetLoaderOptions ? assetLoaderOptions : CreateDefaultLoaderOptions(),
                Stream = stream,
                Filename = filename,
                FileExtension = fileExtension ?? FileUtils.GetFileExtension(filename, false),
                BasePath = FileUtils.GetFileDirectory(filename),
                CustomData = customContextData,
                HandleError = HandleError,
                OnError = onError,
                WrapperGameObject = wrapperGameObject,
                Async = false,
                IsZipFile = isZipFile,
                PersistentDataPath = Application.persistentDataPath
            };
            assetLoaderContext.Setup();
            LoadModelInternal(assetLoaderContext);
            return assetLoaderContext;
        }

        /// <summary>Begins the model loading process.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        private static void LoadModelInternal(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.Options.CompactHeap)
            {
                GCSettings.LargeObjectHeapCompactionMode = GCLargeObjectHeapCompactionMode.CompactOnce;
            }
#if !TRILIB_DISABLE_VALIDATIONS
            ValidateAssetLoaderOptions(assetLoaderContext.Options);
#endif
#if TRILIB_USE_THREAD_NAMES && !UNITY_WSA
            var threadName = "TriLib_LoadModelFromStream";
#else
            string threadName = null;
#endif
            var fileExtension = assetLoaderContext.FileExtension;
            if (fileExtension == null && assetLoaderContext.Filename != null)
            {
                fileExtension = FileUtils.GetFileExtension(assetLoaderContext.Filename, false);
            }
            if (fileExtension == "zip")
            {
                AssetLoaderZip.LoadModelFromZipFile(assetLoaderContext.Filename,
                    assetLoaderContext.OnLoad,
                    assetLoaderContext.OnMaterialsLoad,
                    assetLoaderContext.OnProgress,
                    assetLoaderContext.OnError,
                    assetLoaderContext.WrapperGameObject,
                    assetLoaderContext.Options,
                    assetLoaderContext.CustomData,
                    assetLoaderContext.FileExtension,
                    assetLoaderContext.HaltTasks,
                    assetLoaderContext.OnPreLoad);
            }
            else
            {
                ThreadUtils.RequestNewThreadFor(
                        assetLoaderContext,
                        LoadModel,
                        ProcessRootModel,
                        HandleError,
                        assetLoaderContext.Options.Timeout,
                        threadName,
                        !assetLoaderContext.HaltTasks,
                        assetLoaderContext.OnPreLoad
                    );
            }
        }

        /// <summary>
        /// Validates the given AssetLoaderOptions.
        /// </summary>
        /// <param name="assetLoaderOptions">The options to use when loading the Model.</param>
        private static void ValidateAssetLoaderOptions(AssetLoaderOptions assetLoaderOptions)
        {
#if ENABLE_IL2CPP
            if (assetLoaderOptions.EnableProfiler) {
                assetLoaderOptions.EnableProfiler = false;
                Debug.LogWarning("TriLib: The built in profiler has been disabled as it does not work with IL2CPP builds.");
                Debug.LogWarning(ValidationMessage);
            }
#endif
            if (GraphicsSettingsUtils.IsUsingUniversalPipeline && assetLoaderOptions.LoadTexturesAsSRGB)
            {
                Debug.LogWarning("Textures must be loaded as Linear on the UniversalRP. The \"AssetLoaderOptions.LoadTexturesAsSRGB\" option will be changed automatically.");
                Debug.LogWarning(ValidationMessage);
                assetLoaderOptions.LoadTexturesAsSRGB = false;
            }
            if (assetLoaderOptions.GetCompatibleTextureFormat || assetLoaderOptions.EnforceAlphaChannelTextures)
            {
                Debug.LogWarning("On some platforms, disabling the \"AssetLoaderOptions.GetCompatibleTextureFormat\" and \"AssetLoaderOptions.EnforceAlphaChannelTextures\" options can improve memory usage, but it could cause issues on other platforms. Turning off these options and testing your loader routine are encouraged.");
                Debug.LogWarning(ValidationMessage);
            }
            if (!assetLoaderOptions.UseUnityNativeTextureLoader)
            {
                Debug.LogWarning("Please consider enabling your \"AssetLoaderOptions.UseUnityNativeTextureLoader\" field. That will narrow down the accepted image file formats to PNG and JPG, but this method is faster than the default TriLib StbImage.");
                Debug.LogWarning(ValidationMessage);
            }
            if (!assetLoaderOptions.UseUnityNativeNormalCalculator)
            {
                Debug.LogWarning("Please consider enabling your \"AssetLoaderOptions.UseUnityNativeNormalCalculator\" field. That will simplify the normal calculation algorithm but is faster than the default TriLib normal calculator.");
                Debug.LogWarning(ValidationMessage);
            }
#if !UNITY_WSA
            if (assetLoaderOptions.CompactHeap)
            {
                Debug.LogWarning("Heap compactation only works on UWP compilations. You can safely disable your \"AssetLoaderOptions.CompactHeap\" field.");
                Debug.LogWarning(ValidationMessage);
            }
#endif
#if UNITY_ANDROID || UNITY_IOS || UNITY_WSA
            if (assetLoaderOptions.ExtractEmbeddedData)
            {
                Debug.LogWarning("You have enabled TriLib embedded data caching. Some platforms like Android, iOS, and UWP require special permission to access temporary file folders. If you are getting file-system errors when loading your models. Try setting your \"AssetLoaderOptions.ExtractEmbeddedData\" field value to \"false\".");
                Debug.LogWarning(ValidationMessage);
            }
#endif
#if UNITY_WEBGL
            if (!assetLoaderOptions.UseCoroutines)
            {
                Debug.LogWarning("Please consider enabling your \"AssetLoaderOptions.UseCoroutines\" field. That might prevent your browser from showing \"The page is not responding\" messages.");
                Debug.LogWarning(ValidationMessage);
            }
#endif
        }

#if UNITY_EDITOR
        private static Object LoadOrCreateScriptableObject(string type, string @namespace, string subFolder)
        {
            string mappersFilePath;
            var triLibMapperAssets = AssetDatabase.FindAssets("TriLibMappersPlaceholder");
            if (triLibMapperAssets.Length > 0)
            {
                mappersFilePath = AssetDatabase.GUIDToAssetPath(triLibMapperAssets[0]);
            }
            else
            {
                throw new Exception("Could not find \"TriLibMappersPlaceholder\" file. Please re-import TriLib package.");
            }
            var mappersDirectory = $"{FileUtils.GetFileDirectory(mappersFilePath)}";
            var assetDirectory = $"{mappersDirectory}/{subFolder}";
            if (!AssetDatabase.IsValidFolder(assetDirectory))
            {
                AssetDatabase.CreateFolder(mappersDirectory, subFolder);
            }
            var assetPath = $"{assetDirectory}/{type}.asset";
            var scriptableObject = AssetDatabase.LoadAssetAtPath(assetPath, typeof(Object));
            if (scriptableObject == null)
            {
                scriptableObject = CreateScriptableObjectSafe(type, @namespace);
                if (scriptableObject != null)
                {
                    AssetDatabase.CreateAsset(scriptableObject, assetPath);
                }
            }
            return scriptableObject;
        }
#endif

        /// <summary>Creates an Asset Loader Options with the default settings and Mappers.</summary>
        /// <param name="generateAssets">Indicates whether created Scriptable Objects will be saved as assets.</param>
        /// <param name="supressWarning">Pass `true `if you are caching your AssetLoaderOptions instance.</param>
        /// <returns>The Asset Loader Options containing the default settings.</returns>
        public static AssetLoaderOptions CreateDefaultLoaderOptions(bool generateAssets = false, bool supressWarning = false)
        {
            if (!supressWarning)
            {
                Debug.LogWarning("TriLib: You are creating a new AssetLoaderOptions instance. If you are caching this instance and don't want this message to be displayed again, pass `false` to the `supressWarning` parameter of `CreateDefaultLoaderOptions` call.");
            }
            var assetLoaderOptions = ScriptableObject.CreateInstance<AssetLoaderOptions>();
            ByBonesRootBoneMapper byBonesRootBoneMapper;
#if UNITY_EDITOR
            if (generateAssets)
            {
                byBonesRootBoneMapper = (ByBonesRootBoneMapper)LoadOrCreateScriptableObject("ByBonesRootBoneMapper", TriLibMappersNamespace, "RootBone");
            }
            else
            {
                byBonesRootBoneMapper = ScriptableObject.CreateInstance<ByBonesRootBoneMapper>();
            }
#else
            byBonesRootBoneMapper = ScriptableObject.CreateInstance<ByBonesRootBoneMapper>();
#endif
            byBonesRootBoneMapper.name = "ByBonesRootBoneMapper";
            assetLoaderOptions.RootBoneMapper = byBonesRootBoneMapper;

            var materialMappers = new List<MaterialMapper>();
            for (var i = 0; i < MaterialMapper.RegisteredMappers.Count; i++)
            {
                var materialMapperName = MaterialMapper.RegisteredMappers[i];
                var materialMapperNamespace = MaterialMapper.RegisteredMapperNamespaces[i];
                if (materialMapperName == null)
                {
                    continue;
                }

                MaterialMapper materialMapper;
                try
                {
#if UNITY_EDITOR
                    if (generateAssets)
                    {
                        materialMapper = LoadOrCreateScriptableObject(materialMapperName, materialMapperNamespace, "Material") as MaterialMapper;
                    }
                    else
                    {
                        materialMapper = LoadOrCreateScriptableObjectSafe(materialMapperName, materialMapperNamespace, "Mappers/Material", true) as MaterialMapper;
                    }
#else
                    materialMapper = LoadOrCreateScriptableObjectSafe(materialMapperName, materialMapperNamespace, "Mappers/Material", true) as MaterialMapper;
#endif
                }
                catch
                {
                    materialMapper = null;
                }

                if (materialMapper is object)
                {
                    materialMapper.name = materialMapperName;
                    if (materialMapper.IsCompatible(null))
                    {
                        materialMappers.Add(materialMapper);
                    }
                    else
                    {
#if UNITY_EDITOR
                        var assetPath = AssetDatabase.GetAssetPath(materialMapper);
                        if (assetPath == null)
                        {
                            Object.DestroyImmediate(materialMapper);
                        }
#else
                        Object.Destroy(materialMapper);
#endif
                    }
                }
            }
            if (materialMappers.Count == 0)
            {
                Debug.LogWarning("TriLib could not find any suitable MaterialMapper on the project.");
            }
            else
            {
                assetLoaderOptions.MaterialMappers = materialMappers.ToArray();
            }
            return assetLoaderOptions;
        }

        /// <summary>
        /// Tries to create a ScriptableObject with the given parameters, without throwing an internal Exception.
        /// </summary>
        /// <param name="typeName">The ScriptableObject type name.</param>
        /// <param name="typeNamespace">The ScriptableObject type namespace.</param>
        /// <returns>The created ScriptableObject, or <c>null</c>.</returns>
        private static ScriptableObject CreateScriptableObjectSafe(string typeName, string typeNamespace)
        {
            var type = Type.GetType($"{typeNamespace}.{typeName}");
            return type != null ? ScriptableObject.CreateInstance(typeName) : null;
        }

        /// <summary>
        /// Tries to load an ScriptableObject, or creates it with the given parameters if the ScriptableObject can't be found.
        /// </summary>
        /// <param name="typeName">The ScriptableObject type name.</param>
        /// <param name="typeNamespace">The ScriptableObject type namespace.</param>
        /// <param name="directory">The directory where the ScriptableObject instance might be.</param>
        /// <param name="instantiate">Turn on this field to instantiate the ScriptableObject.</param>
        /// <returns>The created ScriptableObject, or <c>null</c>.</returns>
        public static ScriptableObject LoadOrCreateScriptableObjectSafe(string typeName, string typeNamespace, string directory, bool instantiate)
        {
            var scriptableObject = Resources.Load<ScriptableObject>($"{directory}/{typeName}");
            if (scriptableObject == null)
            {
                var type = Type.GetType($"{typeNamespace}.{typeName}");
                return type != null ? ScriptableObject.CreateInstance(typeName) : null;
            }
            return instantiate ? Object.Instantiate(scriptableObject) : scriptableObject;
        }


        /// <summary>
        /// Returns the Material Mapper configured for the Unity project.
        /// </summary>
        /// <param name="instantiate">Pass <c>true</c> to instantiate a new Material Mapper, or <c>false</c> to use the Material Mapper prefab instead.</param>
        /// <returns>The Material Mapper configured for the project, if there is any. Otherwise, <c>null</c>.</returns>
        public static MaterialMapper GetSelectedMaterialMapper(bool instantiate)
        {
            for (var i = 0; i < MaterialMapper.RegisteredMappers.Count; i++)
            {
                var materialMapperName = MaterialMapper.RegisteredMappers[i];
                var materialMapperNamespace = MaterialMapper.RegisteredMapperNamespaces[i];
                if (TriLibSettings.GetBool(materialMapperName))
                {
                    return LoadOrCreateScriptableObjectSafe(materialMapperName, materialMapperNamespace, "Mappers/Materials", instantiate) as MaterialMapper;
                }
            }
            return null;
        }

        /// <summary>
        /// Gets the name of a compatible Material Mapper based on the render pipeline.
        /// </summary>
        /// <returns>The Material Mapper name, if found. Otherwise <c>null</c>.</returns>
        public static string GetCompatibleMaterialMapperName()
        {
            string materialMapper;
            if (GraphicsSettingsUtils.IsUsingHDRPPipeline)
            {
                materialMapper = "HDRPMaterialMapper";
            }
            else if (GraphicsSettingsUtils.IsUsingUniversalPipeline)
            {
                materialMapper = "UniversalRPMaterialMapper";
            }
            else
            {
                materialMapper = "StandardMaterialMapper";
            }
            return materialMapper;
        }

        private static IEnumerator CreateRootModel(AssetLoaderContext assetLoaderContext)
        {
            var transform = assetLoaderContext.WrapperGameObject != null ? assetLoaderContext.WrapperGameObject.transform : null;
            var rootModel = assetLoaderContext.RootModel;
            foreach (var item in CreateModel(assetLoaderContext, transform, rootModel, rootModel, true))
            {
                yield return item;
            }
            PostProcessModels(assetLoaderContext);
            foreach (var item in ProcessMaterials(assetLoaderContext))
            {
                yield return item;
            }
        }

        private static void PostProcessModels(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.RootGameObject.transform.localScale.sqrMagnitude == 0f)
            {
                assetLoaderContext.RootGameObject.transform.localScale = Vector3.one;
            }
            SetupModelLod(assetLoaderContext, assetLoaderContext.RootModel);
            if (assetLoaderContext.Options.AnimationType != AnimationType.None || assetLoaderContext.Options.ImportBlendShapes)
            {
                SetupModelBones(assetLoaderContext, assetLoaderContext.RootModel);
                BuildGameObjectsPaths(assetLoaderContext);
                SetupRig(assetLoaderContext);
            }
            assetLoaderContext.RootGameObject.isStatic = assetLoaderContext.Options.Static;
            assetLoaderContext.OnLoad?.Invoke(assetLoaderContext);
        }

        /// <summary>Configures the context Model LODs (levels-of-detail) if there are any.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="model">The Model containing the LOD data.</param>

        private static void SetupModelLod(AssetLoaderContext assetLoaderContext, IModel model)
        {
            if (model.Children != null && model.Children.Count > 0)
            {
                var lodModels = new Dictionary<int, List<Renderer>>(model.Children.Count);
                var minLod = int.MaxValue;
                var maxLod = 0;
                for (var i = 0; i < model.Children.Count; i++)
                {
                    var child = model.Children[i];
                    var match = Regex.Match(child.Name, "_LOD(?<number>[0-9]+)|LOD_(?<number>[0-9]+)");
                    if (match.Success)
                    {
                        var lodNumber = Convert.ToInt32(match.Groups["number"].Value);
                        minLod = Mathf.Min(lodNumber, minLod);
                        maxLod = Mathf.Max(lodNumber, maxLod);
                        if (!lodModels.TryGetValue(lodNumber, out var renderers))
                        {
                            renderers = new List<Renderer>();
                            lodModels.Add(lodNumber, renderers);
                        }
                        renderers.AddRange(assetLoaderContext.GameObjects[child].GetComponentsInChildren<Renderer>());
                    }

                }
                if (lodModels.Count > 1)
                {
                    var newGameObject = assetLoaderContext.GameObjects[model];
                    var lods = new List<LOD>(lodModels.Count + 1);
                    var lodGroup = newGameObject.AddComponent<LODGroup>();
                    var lastPosition = assetLoaderContext.Options.LODScreenRelativeTransitionHeightBase;
                    for (var i = minLod; i <= maxLod; i++)
                    {
                        if (lodModels.TryGetValue(i, out var renderers))
                        {
                            lods.Add(new LOD(lastPosition, renderers.ToArray()));
                            lastPosition *= 0.5f;
                        }
                    }
                    lodGroup.SetLODs(lods.ToArray());
                }
                for (var i = 0; i < model.Children.Count; i++)
                {
                    var child = model.Children[i];
                    SetupModelLod(assetLoaderContext, child);
                }
            }
        }

        /// <summary>Builds the Game Object Converts hierarchy paths.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        private static void BuildGameObjectsPaths(AssetLoaderContext assetLoaderContext)
        {
            foreach (var value in assetLoaderContext.GameObjects.Values)
            {
                assetLoaderContext.GameObjectPaths.Add(value, value.transform.BuildPath(assetLoaderContext.RootGameObject.transform));

            }
        }

        /// <summary>Configures the context Model rigging if there is any.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        private static void SetupRig(AssetLoaderContext assetLoaderContext)
        {
            var animations = assetLoaderContext.RootModel.AllAnimations;
            AnimationClip[] animationClips = null;
            if (assetLoaderContext.Options.AnimationType == AnimationType.Humanoid || animations != null && animations.Count > 0)
            {
                switch (assetLoaderContext.Options.AnimationType)
                {
                    case AnimationType.Legacy:
                        {
                            SetupAnimationComponents(assetLoaderContext, animations, out animationClips, out var animator, out var unityAnimation);
                            break;
                        }
                    case AnimationType.Generic:
                        {
                            SetupAnimationComponents(assetLoaderContext, animations, out animationClips, out var animator, out var unityAnimation);
                            if (assetLoaderContext.Options.AvatarDefinition == AvatarDefinitionType.CopyFromOtherAvatar)
                            {
                                animator.avatar = assetLoaderContext.Options.Avatar;
                            }
                            else
                            {
                                SetupGenericAvatar(assetLoaderContext, animator);
                            }
                            break;
                        }
                    case AnimationType.Humanoid:
                        {
                            SetupAnimationComponents(assetLoaderContext, animations, out animationClips, out var animator, out var unityAnimation);
                            if (assetLoaderContext.Options.AvatarDefinition == AvatarDefinitionType.CopyFromOtherAvatar)
                            {
                                animator.avatar = assetLoaderContext.Options.Avatar;
                            }
                            else if (assetLoaderContext.Options.HumanoidAvatarMapper != null)
                            {
                                SetupHumanoidAvatar(assetLoaderContext, animator);
                            }
                            break;
                        }
                }

                if (animationClips != null)
                {
                    if (assetLoaderContext.Options.AnimationClipMappers != null)
                    {
                        Array.Sort(assetLoaderContext.Options.AnimationClipMappers, (a, b) => a.CheckingOrder > b.CheckingOrder ? -1 : 1);
                        foreach (var animationClipMapper in assetLoaderContext.Options.AnimationClipMappers)
                        {
                            animationClips = animationClipMapper.MapArray(assetLoaderContext, animationClips);

                            if (animationClips != null && animationClips.Length > 0)
                            {
                                break;
                            }
                        }
                    }
                    for (var i = 0; i < animationClips.Length; i++)
                    {
                        var animationClip = animationClips[i];
                        assetLoaderContext.Allocations.Add(animationClip);
                    }
                }
            }
        }

        /// <summary>
        /// Creates animation components for the given context.
        /// </summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="animations">The Animations loaded for the Model.</param>
        /// <param name="animationClips">The AnimationClips that will be created for the Model.</param>
        /// <param name="animator">The Animator that will be created for the Model.</param>
        /// <param name="unityAnimation">The Animation Component that will be created for the Model.</param>
        private static void SetupAnimationComponents(AssetLoaderContext assetLoaderContext, IList<IAnimation> animations, out AnimationClip[] animationClips, out Animator animator, out Animation unityAnimation)
        {
            if (assetLoaderContext.Options.AnimationType == AnimationType.Legacy && assetLoaderContext.Options.EnforceAnimatorWithLegacyAnimations || assetLoaderContext.Options.AnimationType != AnimationType.Legacy)
            {
                animator = assetLoaderContext.RootGameObject.AddComponent<Animator>();
            }
            else
            {
                animator = null;
            }
            unityAnimation = assetLoaderContext.RootGameObject.AddComponent<Animation>();
            unityAnimation.playAutomatically = assetLoaderContext.Options.AutomaticallyPlayLegacyAnimations;
            unityAnimation.wrapMode = assetLoaderContext.Options.AnimationWrapMode;
            if (animations != null)
            {
                animationClips = new AnimationClip[animations.Count];
                for (var i = 0; i < animations.Count; i++)
                {
                    var triLibAnimation = animations[i];
                    var animationClip = CreateAnimation(assetLoaderContext, triLibAnimation);
                    unityAnimation.AddClip(animationClip, animationClip.name);
                    animationClips[i] = animationClip;
                    assetLoaderContext.Reader.UpdateLoadingPercentage(i, assetLoaderContext.Reader.LoadingStepsCount + (int)ReaderBase.PostLoadingSteps.PostProcessAnimationClips, animations.Count);
                }
                if (assetLoaderContext.Options.AutomaticallyPlayLegacyAnimations && animationClips.Length > 0)
                {
                    unityAnimation.clip = animationClips[0];
                    unityAnimation.Play(animationClips[0].name);
                }
            }
            else
            {
                animationClips = null;
            }
        }

        /// <summary>Creates a Skeleton Bone for the given Transform.</summary>
        /// <param name="boneTransform">The bone Transform to use on the Skeleton Bone.</param>
        /// <returns>The created Skeleton Bone.</returns>
        private static SkeletonBone CreateSkeletonBone(Transform boneTransform)
        {
            var skeletonBone = new SkeletonBone
            {
                name = boneTransform.name,
                position = boneTransform.localPosition,
                rotation = boneTransform.localRotation,
                scale = boneTransform.localScale
            };
            return skeletonBone;
        }

        /// <summary>Creates a Human Bone for the given Bone Mapping, containing the relationship between the Transform and Bone.</summary>
        /// <param name="boneMapping">The Bone Mapping used to create the Human Bone, containing the information used to search for bones.</param>
        /// <param name="boneName">The bone name to use on the created Human Bone.</param>
        /// <returns>The created Human Bone.</returns>
        private static HumanBone CreateHumanBone(BoneMapping boneMapping, string boneName)
        {
            var humanBone = new HumanBone
            {
                boneName = boneName,
                humanName = GetHumanBodyName(boneMapping.HumanBone),
                limit =
                {
                    useDefaultValues = boneMapping.HumanLimit.useDefaultValues,
                    axisLength = boneMapping.HumanLimit.axisLength,
                    center = boneMapping.HumanLimit.center,
                    max = boneMapping.HumanLimit.max,
                    min = boneMapping.HumanLimit.min
                }
            };
            return humanBone;
        }

        /// <summary>Returns the given Human Body Bones name as String.</summary>
        /// <param name="humanBodyBones">The Human Body Bones to get the name from.</param>
        /// <returns>The Human Body Bones name.</returns>
        private static string GetHumanBodyName(HumanBodyBones humanBodyBones)
        {
            return HumanTrait.BoneName[(int)humanBodyBones];
        }

        /// <summary>Creates a Generic Avatar to the given context Model.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="animator">The Animator assigned to the given Context Root Game Object.</param>
        private static void SetupGenericAvatar(AssetLoaderContext assetLoaderContext, Animator animator)
        {
            var parent = assetLoaderContext.RootGameObject.transform.parent;
            assetLoaderContext.RootGameObject.transform.SetParent(null, true);
            var bones = new List<Transform>();
            assetLoaderContext.RootModel.GetBones(assetLoaderContext, bones);
            var rootBone = assetLoaderContext.Options.RootBoneMapper.Map(assetLoaderContext, bones);
            var avatar = AvatarBuilder.BuildGenericAvatar(assetLoaderContext.RootGameObject, rootBone != null ? rootBone.name : "");
            avatar.name = $"{assetLoaderContext.RootGameObject.name}Avatar";
            animator.avatar = avatar;
            assetLoaderContext.RootGameObject.transform.SetParent(parent, true);
        }

        /// <summary>Creates a Humanoid Avatar to the given context Model.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="animator">The Animator assigned to the given Context Root Game Object.</param>
        private static void SetupHumanoidAvatar(AssetLoaderContext assetLoaderContext, Animator animator)
        {
            var valid = false;
            var mapping = assetLoaderContext.Options.HumanoidAvatarMapper.Map(assetLoaderContext);
            if (mapping.Count > 0)
            {
                var parent = assetLoaderContext.RootGameObject.transform.parent;
                var rootGameObjectPosition = assetLoaderContext.RootGameObject.transform.position;
                assetLoaderContext.RootGameObject.transform.SetParent(null, false);
                assetLoaderContext.Options.HumanoidAvatarMapper.PostSetup(assetLoaderContext, mapping);
                Transform hipsTransform = null;
                var humanBones = new HumanBone[mapping.Count];
                var boneIndex = 0;
                foreach (var kvp in mapping)
                {
                    if (kvp.Key.HumanBone == HumanBodyBones.Hips)
                    {
                        hipsTransform = kvp.Value;
                    }
                    humanBones[boneIndex++] = CreateHumanBone(kvp.Key, kvp.Value.name);
                }
                if (hipsTransform != null)
                {
                    var skeletonBones = new Dictionary<Transform, SkeletonBone>();
                    var bounds = assetLoaderContext.RootGameObject.CalculateBounds();
                    var toBottom = bounds.min.y;
                    if (toBottom < 0f)
                    {
                        var hipsTransformPosition = hipsTransform.position;
                        hipsTransformPosition.y -= toBottom;
                        hipsTransform.position = hipsTransformPosition;
                    }
                    var toCenter = Vector3.zero - bounds.center;
                    toCenter.y = 0f;
                    if (toCenter.sqrMagnitude > 0.01f)
                    {
                        var hipsTransformPosition = hipsTransform.position;
                        hipsTransformPosition += toCenter;
                        hipsTransform.position = hipsTransformPosition;
                    }
                    foreach (var kvp in assetLoaderContext.GameObjects)
                    {
                        if (!skeletonBones.ContainsKey(kvp.Value.transform))
                        {
                            skeletonBones.Add(kvp.Value.transform, CreateSkeletonBone(kvp.Value.transform));
                        }
                    }
                    var triLibHumanDescription = assetLoaderContext.Options.HumanDescription ?? new General.HumanDescription();
                    var humanDescription = new HumanDescription
                    {
                        armStretch = triLibHumanDescription.armStretch,
                        feetSpacing = triLibHumanDescription.feetSpacing,
                        hasTranslationDoF = triLibHumanDescription.hasTranslationDof,
                        legStretch = triLibHumanDescription.legStretch,
                        lowerArmTwist = triLibHumanDescription.lowerArmTwist,
                        lowerLegTwist = triLibHumanDescription.lowerLegTwist,
                        upperArmTwist = triLibHumanDescription.upperArmTwist,
                        upperLegTwist = triLibHumanDescription.upperLegTwist,
                        skeleton = skeletonBones.Values.ToArray(),
                        human = humanBones
                    };
                    var avatar = AvatarBuilder.BuildHumanAvatar(assetLoaderContext.RootGameObject, humanDescription);
                    avatar.name = $"{assetLoaderContext.RootGameObject.name}Avatar";
                    animator.avatar = avatar;
                }
                assetLoaderContext.RootGameObject.transform.SetParent(parent, false);
                assetLoaderContext.RootGameObject.transform.position = rootGameObjectPosition;
                valid = animator.avatar.isValid || !assetLoaderContext.Options.ShowLoadingWarnings;
            }
            if (!valid)
            {
                Debug.LogWarning($"Could not create an Avatar for the model \"{(assetLoaderContext.Filename == null ? "Unknown" : FileUtils.GetShortFilename(assetLoaderContext.Filename))}\"");
            }
        }

        /// <summary>Converts the given Model into a Game Object.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="parentTransform">The parent Game Object Transform.</param>
        /// <param name="rootModel">The root Model.</param>
        /// <param name="model">The Model to convert.</param>
        /// <param name="isRootGameObject">Is this the first node in the Model hierarchy?</param>
        private static IEnumerable CreateModel(AssetLoaderContext assetLoaderContext, Transform parentTransform, IRootModel rootModel, IModel model, bool isRootGameObject)
        {
            var newGameObject = new GameObject(model.Name);
            assetLoaderContext.GameObjects.Add(model, newGameObject);
            assetLoaderContext.Models.Add(newGameObject, model);
            newGameObject.transform.parent = parentTransform;
            newGameObject.transform.localPosition = model.LocalPosition;
            newGameObject.transform.localRotation = model.LocalRotation;
            newGameObject.transform.localScale = model.LocalScale;
            if (model.GeometryGroup != null)
            {
                foreach (var item in CreateGeometry(assetLoaderContext, newGameObject, rootModel, model))
                {
                    yield return item;
                }
            }
            if (assetLoaderContext.Options.ImportCameras && model is ICamera camera)
            {
                CreateCamera(assetLoaderContext, camera, newGameObject);
            }
            if (assetLoaderContext.Options.ImportLights && model is ILight light)
            {
                CreateLight(assetLoaderContext, light, newGameObject);
            }
            if (model.Children != null && model.Children.Count > 0)
            {
                for (var i = 0; i < model.Children.Count; i++)
                {
                    var child = model.Children[i];
                    foreach (var item in CreateModel(assetLoaderContext, newGameObject.transform, rootModel, child, false))
                    {
                        yield return item;
                    }
                }
            }
            if (assetLoaderContext.Options.UserPropertiesMapper != null && model.UserProperties != null)
            {
                foreach (var userProperty in model.UserProperties)
                {
                    assetLoaderContext.Options.UserPropertiesMapper.OnProcessUserData(assetLoaderContext, newGameObject, userProperty.Key, userProperty.Value);
                }
            }
            if (isRootGameObject)
            {
                assetLoaderContext.RootGameObject = newGameObject;
            }
        }

        /// <summary>Converts the given model light, if present into a Light.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="light">The Model.</param>
        /// <param name="newGameObject">The Model Game Object.</param>
        private static void CreateLight(AssetLoaderContext assetLoaderContext, ILight light, GameObject newGameObject)
        {
            var unityLight = newGameObject.AddComponent<Light>();
            unityLight.color = light.Color;
            unityLight.innerSpotAngle = light.InnerSpotAngle;
            unityLight.spotAngle = light.OuterSpotAngle;
            unityLight.intensity = light.Intensity;
            unityLight.range = light.Range;
            unityLight.type = light.LightType;
            unityLight.shadows = light.CastShadows ? LightShadows.Soft : LightShadows.None;
#if UNITY_EDITOR
            unityLight.areaSize = new Vector2(light.Width, light.Height);
#endif
        }

        /// <summary>Converts the given model camera, if present into a Camera.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="camera">The Model.</param>
        /// <param name="newGameObject">The Model Game Object.</param>
        private static void CreateCamera(AssetLoaderContext assetLoaderContext, ICamera camera, GameObject newGameObject)
        {
            var unityCamera = newGameObject.AddComponent<Camera>();
            unityCamera.aspect = camera.AspectRatio;
            unityCamera.orthographic = camera.Ortographic;
            unityCamera.orthographicSize = camera.OrtographicSize;
            unityCamera.fieldOfView = camera.FieldOfView;
            unityCamera.nearClipPlane = camera.NearClipPlane;
            unityCamera.farClipPlane = camera.FarClipPlane;
            unityCamera.focalLength = camera.FocalLength;
            unityCamera.sensorSize = camera.SensorSize;
            unityCamera.lensShift = camera.LensShift;
            unityCamera.gateFit = camera.GateFitMode;
            unityCamera.usePhysicalProperties = camera.PhysicalCamera;
            unityCamera.enabled = true;
        }

        /// <summary>Configures the given Model skinning if there is any.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="model">The Model containing the bones.</param>
        private static void SetupModelBones(AssetLoaderContext assetLoaderContext, IModel model)
        {
            var loadedGameObject = assetLoaderContext.GameObjects[model];
            var skinnedMeshRenderer = loadedGameObject.GetComponent<SkinnedMeshRenderer>();
            if (skinnedMeshRenderer != null)
            {
                var bones = model.Bones;
                if (bones != null && bones.Count > 0)
                {
                    var boneIndex = 0;
                    var gameObjectBones = new Transform[bones.Count];
                    for (var i = 0; i < bones.Count; i++)
                    {
                        var bone = bones[i];
                        gameObjectBones[boneIndex++] = assetLoaderContext.GameObjects[bone].transform;
                    }
                    skinnedMeshRenderer.bones = gameObjectBones;
                    skinnedMeshRenderer.rootBone = assetLoaderContext.Options.RootBoneMapper.Map(assetLoaderContext, gameObjectBones);
                }
                skinnedMeshRenderer.sharedMesh = model.GeometryGroup.Mesh;
                if (skinnedMeshRenderer.bounds.size.sqrMagnitude == 0f)
                {
                    skinnedMeshRenderer.localBounds = loadedGameObject.CalculateBounds(true);
                }
            }
            if (model.Children != null && model.Children.Count > 0)
            {
                for (var i = 0; i < model.Children.Count; i++)
                {
                    var subModel = model.Children[i];
                    SetupModelBones(assetLoaderContext, subModel);
                }
            }
        }

        /// <summary>Converts the given Animation into an Animation Clip.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="animation">The Animation to convert.</param>
        /// <returns>The converted Animation Clip.</returns>
        private static AnimationClip CreateAnimation(AssetLoaderContext assetLoaderContext, IAnimation animation)
        {
            var animationClip = new AnimationClip { name = animation.Name, legacy = true, frameRate = animation.FrameRate };
            var animationCurveBindings = animation.AnimationCurveBindings;
            if (animationCurveBindings == null)
            {
                return animationClip;
            }
            for (var i = animationCurveBindings.Count - 1; i >= 0; i--)
            {
                var animationCurveBinding = animationCurveBindings[i];
                var animationCurves = animationCurveBinding.AnimationCurves;
                if (!assetLoaderContext.GameObjects.ContainsKey(animationCurveBinding.Model))
                {
                    continue;
                }
                var gameObject = assetLoaderContext.GameObjects[animationCurveBinding.Model];
                for (var j = 0; j < animationCurves.Count; j++)
                {
                    var animationCurve = animationCurves[j];
                    var unityAnimationCurve = animationCurve.AnimationCurve;
                    var gameObjectPath = assetLoaderContext.GameObjectPaths[gameObject];
                    var propertyName = animationCurve.Property;
                    var propertyType = animationCurve.AnimatedType;
                    animationClip.SetCurve(gameObjectPath, propertyType, propertyName, unityAnimationCurve);
                }
            }
            if (assetLoaderContext.Options.EnsureQuaternionContinuity)
            {
                animationClip.EnsureQuaternionContinuity();
            }
            return animationClip;
        }


        /// <summary>Converts the given Geometry Group into a Mesh.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        /// <param name="meshGameObject">The Game Object where the Mesh belongs.</param>
        /// <param name="rootModel">The root Model.</param>
        /// <param name="meshModel">The Model used to generate the Game Object.</param>
        private static IEnumerable CreateGeometry(AssetLoaderContext assetLoaderContext, GameObject meshGameObject, IRootModel rootModel, IModel meshModel)
        {
            var geometryGroup = meshModel.GeometryGroup;
            if (geometryGroup.GeometriesData != null)
            {
                if (geometryGroup.Mesh == null)
                {
                    geometryGroup.GenerateMesh(assetLoaderContext, assetLoaderContext.Options.AnimationType == AnimationType.None ? null : meshModel.BindPoses, meshModel.MaterialIndices);
                    foreach (var item in assetLoaderContext.ReleaseMainThread())
                    {
                        yield return item;
                    }
                }
                assetLoaderContext.Allocations.Add(geometryGroup.Mesh);
                if (assetLoaderContext.Options.MarkMeshesAsDynamic)
                {
                    geometryGroup.Mesh.MarkDynamic();
                }
                if (assetLoaderContext.Options.LipSyncMappers != null)
                {
                    Array.Sort(assetLoaderContext.Options.LipSyncMappers, (a, b) => a.CheckingOrder > b.CheckingOrder ? -1 : 1);
                    foreach (var lipSyncMapper in assetLoaderContext.Options.LipSyncMappers)
                    {
                        if (lipSyncMapper.Map(assetLoaderContext, geometryGroup, out var visemeToBlendTargets))
                        {
                            var lipSyncMapping = meshGameObject.AddComponent<LipSyncMapping>();
                            lipSyncMapping.VisemeToBlendTargets = visemeToBlendTargets;
                            break;
                        }
                    }
                }
                if (assetLoaderContext.Options.GenerateColliders)
                {
                    if (assetLoaderContext.RootModel.AllAnimations != null && assetLoaderContext.RootModel.AllAnimations.Count > 0 && assetLoaderContext.Options.ShowLoadingWarnings)
                    {
                        Debug.LogWarning("Adding a MeshCollider to an animated object.");
                    }
                    var meshCollider = meshGameObject.AddComponent<MeshCollider>();
                    meshCollider.convex = assetLoaderContext.Options.ConvexColliders;
                    meshCollider.sharedMesh = geometryGroup.Mesh;
                    foreach (var item in assetLoaderContext.ReleaseMainThread())
                    {
                        yield return item;
                    }
                }
                Renderer renderer = null;
                if (assetLoaderContext.Options.AnimationType != AnimationType.None || assetLoaderContext.Options.ImportBlendShapes)
                {
                    var bones = assetLoaderContext.Options.AddAllBonesToSkinnedMeshRenderers ? GetAllBonesRecursive(assetLoaderContext) : meshModel.Bones;
                    var geometryGroupBlendShapeGeometryBindings = geometryGroup.BlendShapeKeys;
                    if ((bones != null && bones.Count > 0 || geometryGroupBlendShapeGeometryBindings != null && geometryGroupBlendShapeGeometryBindings.Count > 0) && assetLoaderContext.Options.AnimationType != AnimationType.None)
                    {
                        var skinnedMeshRenderer = meshGameObject.AddComponent<SkinnedMeshRenderer>();
                        skinnedMeshRenderer.enabled = !assetLoaderContext.Options.ImportVisibility || meshModel.Visibility;
                        renderer = skinnedMeshRenderer;
                    }
                }
                if (renderer == null)
                {
                    var meshFilter = meshGameObject.AddComponent<MeshFilter>();
                    meshFilter.sharedMesh = geometryGroup.Mesh;
                    if (!assetLoaderContext.Options.LoadPointClouds)
                    {
                        var meshRenderer = meshGameObject.AddComponent<MeshRenderer>();
                        meshRenderer.enabled = !assetLoaderContext.Options.ImportVisibility || meshModel.Visibility;
                        renderer = meshRenderer;
                    }
                }
                if (renderer != null)
                {
                    Material loadingMaterial = null;
                    if (assetLoaderContext.Options.MaterialMappers != null)
                    {
                        for (var i = 0; i < assetLoaderContext.Options.MaterialMappers.Length; i++)
                        {
                            var mapper = assetLoaderContext.Options.MaterialMappers[i];
                            if (mapper != null && mapper.IsCompatible(null))
                            {
                                loadingMaterial = mapper.LoadingMaterial;
                                break;
                            }
                        }
                    }
                    var unityMaterials = new Material[geometryGroup.GeometriesData.Count];
                    if (loadingMaterial == null)
                    {
                        if (assetLoaderContext.Options.ShowLoadingWarnings)
                        {
                            Debug.LogWarning("Could not find a suitable loading Material.");
                        }
                    }
                    else
                    {
                        for (var i = 0; i < unityMaterials.Length; i++)
                        {
                            unityMaterials[i] = loadingMaterial;
                        }
                    }
                    renderer.sharedMaterials = unityMaterials;
                    var materialIndices = meshModel.MaterialIndices;
                    foreach (var geometryData in geometryGroup.GeometriesData)
                    {
                        var geometry = geometryData.Value;
                        if (geometry == null)
                        {
                            continue;
                        }

                        var originalGeometryIndex = geometry.OriginalIndex;

                        if (originalGeometryIndex < 0 || originalGeometryIndex >= renderer.sharedMaterials.Length)
                        {
                            continue;
                        }

                        var materialIndex = materialIndices[originalGeometryIndex];

                        IMaterial sourceMaterial;
                        if (rootModel.AllMaterials == null)
                        {
                            rootModel.AllMaterials = new List<IMaterial>();
                        }
                        if (materialIndex < 0 || materialIndex >= rootModel.AllMaterials.Count)
                        {
                            if (!assetLoaderContext.Options.CreateMaterialsForAllModels)
                            {
                                continue;
                            }
                            sourceMaterial = new DummyMaterial() { Name = $"{geometryGroup.Name}_{geometry.Index}" };
                            rootModel.AllMaterials.Add(sourceMaterial);
                        }
                        else
                        {
                            sourceMaterial = rootModel.AllMaterials[materialIndex];
                            if (sourceMaterial == null)
                            {
                                if (!assetLoaderContext.Options.CreateMaterialsForAllModels)
                                {
                                    continue;
                                }
                                sourceMaterial = new DummyMaterial() { Name = $"{geometryGroup.Name}_{geometry.Index}" };
                                rootModel.AllMaterials.Add(sourceMaterial);
                            }
                        }

                        var materialRenderersContext = new MaterialRendererContext
                        {
                            Context = assetLoaderContext,
                            Renderer = renderer,
                            GeometryIndex = geometry.Index,
                            Material = sourceMaterial
                        };
                        if (assetLoaderContext.MaterialRenderers.TryGetValue(sourceMaterial, out var materialRendererContextList))
                        {
                            materialRendererContextList.Add(materialRenderersContext);
                        }
                        else
                        {
                            assetLoaderContext.MaterialRenderers.Add(sourceMaterial, new List<MaterialRendererContext> { materialRenderersContext });
                        }
                    }
                }
            }
        }

        /// <summary>
        /// Creates a list with every bone in the loaded model.
        /// </summary>
        private static IList<IModel> GetAllBonesRecursive(AssetLoaderContext assetLoaderContext)
        {
            var bones = new List<IModel>();
            foreach (var model in assetLoaderContext.RootModel.AllModels)
            {
                if (model.IsBone)
                {
                    bones.Add(model);
                }
            }
            return bones;
        }

        /// <summary>Loads the root Model.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        private static void LoadModel(AssetLoaderContext assetLoaderContext)
        {
            SetupModelLoading(assetLoaderContext);
        }

        private static void SetupModelLoading(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.Stream == null && string.IsNullOrWhiteSpace(assetLoaderContext.Filename))
            {
                throw new Exception("TriLib is unable to load the given file.");
            }
            if (assetLoaderContext.Options.MaterialMappers != null)
            {
                Array.Sort(assetLoaderContext.Options.MaterialMappers, (a, b) => a.CheckingOrder > b.CheckingOrder ? -1 : 1);
            }
            else
            {
                if (assetLoaderContext.Options.ShowLoadingWarnings)
                {
                    Debug.LogWarning("Your AssetLoaderOptions instance has no MaterialMappers. TriLib can't process materials without them.");
                }
            }
#if TRILIB_DRACO
            GltfReader.DracoDecompressorCallback = DracoMeshLoader.DracoDecompressorCallback;
#endif
            var fileExtension = assetLoaderContext.FileExtension;
            if (fileExtension == null)
            {
                fileExtension = FileUtils.GetFileExtension(assetLoaderContext.Filename, false);
            }
            else if (fileExtension[0] == '.' && fileExtension.Length > 1)
            {
                fileExtension = fileExtension.Substring(1);
            }
            if (assetLoaderContext.Stream == null)
            {
                var fileStream = new FileStream(assetLoaderContext.Filename, FileMode.Open, FileAccess.Read, FileShare.Read);
                assetLoaderContext.Stream = fileStream;
                var reader = Readers.FindReaderForExtension(fileExtension);
                if (reader != null)
                {
                    assetLoaderContext.RootModel = reader.ReadStream(fileStream, assetLoaderContext, assetLoaderContext.Filename, assetLoaderContext.OnProgress);
                }
            }
            else
            {
                var reader = Readers.FindReaderForExtension(fileExtension);
                if (reader != null)
                {
                    assetLoaderContext.RootModel = reader.ReadStream(assetLoaderContext.Stream, assetLoaderContext, assetLoaderContext.Filename, assetLoaderContext.OnProgress);
                }
                else
                {
                    throw new Exception("Could not find a suitable reader for the given model. Please fill the 'fileExtension' parameter when calling any model loading method.");
                }
                if (assetLoaderContext.RootModel == null)
                {
                    throw new Exception("TriLib could not load the given model.");
                }
            }
        }

        /// <summary>Processes the root Model.</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>

        private static void ProcessRootModel(AssetLoaderContext assetLoaderContext)
        {
            //Debug.Break();
            //Profiler.enabled = false;
            //return;
            if (assetLoaderContext.RootModel != null)
            {
                var enumerator = CreateRootModel(assetLoaderContext);
                if (assetLoaderContext.Options.UseCoroutines)
                {
                    CoroutineHelper.Instance.StartCoroutine(enumerator);
                }
                else
                {
                    CoroutineHelper.RunMethod(enumerator);
                }
            }
            else
            {
                assetLoaderContext.OnLoad?.Invoke(assetLoaderContext);
            }
        }

        /// <summary>
        /// Processes the Model Materials, if all source Materials have been loaded.
        /// </summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        private static IEnumerable ProcessMaterials(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.RootModel?.AllMaterials != null && assetLoaderContext.RootModel.AllMaterials.Count > 0)
            {
                if (assetLoaderContext.Options.MaterialMappers != null)
                {
                    foreach (var item in ProcessMaterialRenderers(assetLoaderContext))
                    {
                        yield return item;
                    }
                }
                else if (assetLoaderContext.Options.ShowLoadingWarnings)
                {
                    Debug.LogWarning("Please specify a TriLib Material Mapper, otherwise Materials can't be created.");
                }
            }
            else
            {
                if (assetLoaderContext.Options.DiscardUnusedTextures)
                {
                    FinishLoading(assetLoaderContext);
                }
                else
                {
                    LoadUnusedTextures(assetLoaderContext);
                }
            }
        }

        /// <summary>
        /// Loads the unused Textures and adds them to the allocations list.
        /// </summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        private static void LoadUnusedTextures(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.RootGameObject != null)
            {
                if (assetLoaderContext.RootModel.AllTextures != null)
                {
                    foreach (var texture in assetLoaderContext.RootModel.AllTextures)
                    {
                        var textureLoadingContext = new TextureLoadingContext()
                        {
                            Texture = texture,
                            Context = assetLoaderContext
                        };
                        if (!assetLoaderContext.TryGetLoadedTexture(textureLoadingContext, out _))
                        {
                            if (assetLoaderContext.Options.UseUnityNativeTextureLoader)
                            {
                                TextureLoaders.LoadTexture(textureLoadingContext);
                            }
                            else
                            {
                                TextureLoaders.CreateTexture(textureLoadingContext);
                                TextureLoaders.LoadTexture(textureLoadingContext);
                            }
                        }
                    }
                }
            }
            FinishLoading(assetLoaderContext);
        }

        ///<summary>
        /// Finishes the Model loading, calling the OnMaterialsLoad callback, if present.
        ///</summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        private static void FinishLoading(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.Options.AddAssetUnloader && (assetLoaderContext.RootGameObject != null || assetLoaderContext.WrapperGameObject != null))
            {
                var gameObject = assetLoaderContext.RootGameObject ?? assetLoaderContext.WrapperGameObject;
                var assetUnloader = gameObject.AddComponent<AssetUnloader>();
                assetUnloader.Id = AssetUnloader.GetNextId();
                assetUnloader.Allocations = assetLoaderContext.Allocations;
                assetUnloader.CustomData = assetLoaderContext.CustomData;
            }
            if (assetLoaderContext.Options.DiscardUnusedTextures)
            {
                assetLoaderContext.DiscardUnusedTextures();
            }
            assetLoaderContext.Reader?.UpdateLoadingPercentage(1f, assetLoaderContext.Reader.LoadingStepsCount + (int)ReaderBase.PostLoadingSteps.FinishedProcessing);
            assetLoaderContext.OnMaterialsLoad?.Invoke(assetLoaderContext);
            Cleanup(assetLoaderContext);
        }

        /// <summary>
        /// Processes Model Renderers.
        /// </summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>

        private static IEnumerable ProcessMaterialRenderers(AssetLoaderContext assetLoaderContext)
        {
            var materialMapperContexts = new MaterialMapperContext[assetLoaderContext.RootModel.AllMaterials.Count];
            for (var i = 0; i < assetLoaderContext.RootModel.AllMaterials.Count; i++)
            {
                var material = assetLoaderContext.RootModel.AllMaterials[i];
                var materialMapperContext = new MaterialMapperContext()
                {
                    Context = assetLoaderContext,
                    Material = material
                };
                materialMapperContexts[i] = materialMapperContext;
                for (var j = 0; j < assetLoaderContext.Options.MaterialMappers.Length; j++)
                {
                    var materialMapper = assetLoaderContext.Options.MaterialMappers[j];
                    if (materialMapper is object && materialMapper.IsCompatible(materialMapperContext))
                    {
                        materialMapperContext.MaterialMapper = materialMapper;
                        if (materialMapper.UsesCoroutines)
                        {
                            foreach (var item in materialMapper.MapCoroutine(materialMapperContext))
                            {
                                yield return item;
                            }
                        }
                        else
                        {
                            materialMapper.Map(materialMapperContext);
                        }
                        ApplyMaterialToRenderers(materialMapperContext);
                        break;
                    }
                }
                assetLoaderContext.Reader.UpdateLoadingPercentage(i, assetLoaderContext.Reader.LoadingStepsCount + (int)ReaderBase.PostLoadingSteps.PostProcessRenderers, assetLoaderContext.RootModel.AllMaterials.Count);
            }
            if (assetLoaderContext.Options.DiscardUnusedTextures)
            {
                FinishLoading(assetLoaderContext);
            }
            else
            {
                LoadUnusedTextures(assetLoaderContext);
            }
        }

        /// <summary>
        /// Applies the Material from the given context to its Renderers.
        /// </summary>
        /// <param name="materialMapperContext">The source Material Mapper Context, containing the Virtual Material and Unity Material.</param>
        private static void ApplyMaterialToRenderers(MaterialMapperContext materialMapperContext)
        {
            materialMapperContext.Completed = false;
            if (materialMapperContext.Context.MaterialRenderers.TryGetValue(materialMapperContext.Material, out var materialRendererList))
            {
                for (var k = 0; k < materialRendererList.Count; k++)
                {
                    var materialRendererContext = materialRendererList[k];
                    materialRendererContext.MaterialMapperContext = materialMapperContext;
                    materialMapperContext.MaterialMapper.ApplyMaterialToRenderer(materialRendererContext);
                }
            }
            materialMapperContext.Completed = true;
        }

        /// <summary>Handles all Model loading errors, unloads the partially loaded Model (if suitable), and calls the error callback (if existing).</summary>
        /// <param name="error">The Contextualized Error that has occurred.</param>
        private static void HandleError(IContextualizedError error)
        {
            var exception = error.GetInnerException();
            if (error.GetContext() is IAssetLoaderContext context)
            {
                var assetLoaderContext = context.Context;
                if (assetLoaderContext != null)
                {
                    Cleanup(assetLoaderContext);
                    if (assetLoaderContext.Options.DestroyOnError && assetLoaderContext.RootGameObject != null)
                    {
                        if (!Application.isPlaying)
                        {
                            Object.DestroyImmediate(assetLoaderContext.RootGameObject);
                        }
                        else
                        {
                            Object.Destroy(assetLoaderContext.RootGameObject);
                        }
                        assetLoaderContext.RootGameObject = null;
                    }
                    if (assetLoaderContext.OnError != null)
                    {
                        Dispatcher.InvokeAsync(assetLoaderContext.OnError, error);
                    }
                }
            }
            else
            {
                var contextualizedError = new ContextualizedError<object>(exception, null);
                Dispatcher.InvokeAsync(Rethrow, contextualizedError);
            }
        }

        /// <summary>
        /// Tries to close the Model Stream, if the used AssetLoaderOptions.CloseSteamAutomatically option is enabled.
        /// </summary>
        /// <param name="assetLoaderContext">The Asset Loader Context reference. Asset Loader Context contains the Model loading data.</param>
        private static void Cleanup(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.Stream != null && assetLoaderContext.Options.CloseStreamAutomatically)
            {
                assetLoaderContext.Stream.TryToDispose();
            }
            if (assetLoaderContext.Options.CollectCG)
            {
                GC.Collect();
                GC.WaitForPendingFinalizers();
                GC.Collect();
            }
        }

        /// <summary>Throws the given Contextualized Error on the main Thread.</summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="contextualizedError">The Contextualized Error to throw.</param>
        private static void Rethrow<T>(ContextualizedError<T> contextualizedError)
        {
            throw contextualizedError;
        }
    }
}
