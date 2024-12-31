#pragma warning disable 649
using System.Collections.Generic;
using TriLibCore.Extensions;
using TriLibCore.Utils;
using UnityEngine;
using UnityEngine.UI;
#if UNITY_EDITOR
using UnityEditor;
#endif
namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a sample that loads a base Model and adds extra Animations from other Models to it.
    /// </summary>
    public class LoadExtraAnimationsSample : MonoBehaviour
    {
        /// <summary>
        /// Returns the path to the base "BuddyBase.fbx" Model.
        /// </summary>
        private string BaseModelPath
        {
            get
            {
#if UNITY_EDITOR
                return $"{Application.dataPath}/TriLib/TriLibSamples/LoadExtraAnimations/Models/BuddyBase.fbx";
#else
                return "Models/BuddyBase.fbx";
#endif
            }
        }

        /// <summary>
        /// Button to instantiate when a new Animation is loaded.
        /// </summary>
        [SerializeField]
        private Button _playAnimationTemplate;

        /// <summary>
        /// The Animation Component from the base Model.
        /// </summary>
        private Animation _baseAnimation;

        /// <summary>
        /// Gathers the AssetLoaderContext from the loaded Animations.
        /// This list is used to process the Animations if the Animations are loaded before the base Model.
        /// </summary>
        private readonly IList<AssetLoaderContext> _loadedAnimations = new List<AssetLoaderContext>();

        /// <summary>
        /// Cached Asset Loader Options instance.
        /// </summary>
        private AssetLoaderOptions _assetLoaderOptions;

        /// <summary>
        /// Loads the "Models/BuddyBase.fbx" Model, then loads all the extra Animations in the same folder.
        /// </summary>
        private void Start()
        {
            LoadBaseModel();
            LoadAnimation("BuddyIdle.fbx");
            LoadAnimation("BuddyWalk.fbx");
            LoadAnimation("BuddyJump.fbx");
        }

        /// <summary>
        /// Loads the Animations from the given Model.
        /// </summary>
        /// <param name="modelFilename">The animated Model filename under the same folder as the base Model.</param>
        private void LoadAnimation(string modelFilename)
        {
            var modelsDirectory = FileUtils.GetFileDirectory(BaseModelPath);
            var modelPath = FileUtils.SanitizePath($"{modelsDirectory}/{modelFilename}");
            if (_assetLoaderOptions == null)
            {
                _assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(false, true);
                _assetLoaderOptions.ImportMeshes = false;
                _assetLoaderOptions.ImportTextures = false;
                _assetLoaderOptions.ImportMaterials = false;
            }
            AssetLoader.LoadModelFromFile(modelPath, OnAnimationModelLoad, null, OnProgress, OnError, gameObject, _assetLoaderOptions);
        }

        /// <summary>
        /// Gathers all Animations from the loaded Model and adds them to the base Model Animation Component.
        /// </summary>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        private void OnAnimationModelLoad(AssetLoaderContext assetLoaderContext)
        {
            Debug.Log($"Animation loaded: {FileUtils.GetShortFilename(assetLoaderContext.Filename)}");
            if (_baseAnimation != null)
            {
                AddAnimation(assetLoaderContext);
            }
            else
            {
                _loadedAnimations.Add(assetLoaderContext);
            }
            assetLoaderContext.RootGameObject.SetActive(false);
        }

        /// <summary>
        /// Adds the Animation Clips from the given AssetLoaderContext RootGameObject to the base Model Animations list.
        /// </summary>
        /// <param name="loadedAnimationContext">The AssetLoaderContext containing the loaded Animation component.</param>
        private void AddAnimation(AssetLoaderContext loadedAnimationContext)
        {
            var rootGameObjectAnimation = loadedAnimationContext.RootGameObject.GetComponent<Animation>();
            if (rootGameObjectAnimation != null)
            {
                var shortFilename = FileUtils.GetShortFilename(loadedAnimationContext.Filename);
                var newAnimationClips = rootGameObjectAnimation.GetAllAnimationClips();
                foreach (var newAnimationClip in newAnimationClips)
                {
                    var animationName = $"{shortFilename}_{newAnimationClip.name}";
                    _baseAnimation.AddClip(newAnimationClip, animationName);
                    var playAnimationButton = Instantiate(_playAnimationTemplate, _playAnimationTemplate.transform.parent);
                    var playAnimationButtonText = playAnimationButton.GetComponentInChildren<Text>();
                    playAnimationButtonText.text = shortFilename;
                    playAnimationButton.gameObject.SetActive(true);
                    playAnimationButton.onClick.AddListener(delegate
                    {
                        _baseAnimation.CrossFade(animationName);
                    });
                }
            }
            Destroy(loadedAnimationContext.RootGameObject);
        }

        /// <summary>
        /// Loads the Model from BaseModelPath including all Model data.
        /// </summary>
        private void LoadBaseModel()
        {
            if (_assetLoaderOptions == null)
            {
                _assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(false, true);
            }
            AssetLoader.LoadModelFromFile(BaseModelPath, OnBaseModelLoad, OnBaseModelMaterialsLoad, OnProgress, OnError, gameObject, _assetLoaderOptions);
        }

        /// <summary>
        /// Called when any error occurs.
        /// </summary>
        /// <param name="obj">The contextualized error, containing the original exception and the context passed to the method where the error was thrown.</param>
        private void OnError(IContextualizedError obj)
        {
            Debug.LogError($"An error occurred while loading your Model: {obj.GetInnerException()}");
        }

        /// <summary>
        /// Called when a Model loading progress changes.
        /// </summary>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        /// <param name="progress">The loading progress.</param>
        private void OnProgress(AssetLoaderContext assetLoaderContext, float progress)
        {

        }

        /// <summary>
        /// Called when the Base Model (including Textures and Materials) has been fully loaded.
        /// This method processes previously loaded Animations from the loaded Animations list.
        /// </summary>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        private void OnBaseModelMaterialsLoad(AssetLoaderContext assetLoaderContext)
        {
            Debug.Log($"Base Model loaded:{FileUtils.GetShortFilename(assetLoaderContext.Filename)}");
            _baseAnimation = assetLoaderContext.RootGameObject.GetComponent<Animation>();
            for (var i = _loadedAnimations.Count - 1; i >= 0; i--)
            {
                AddAnimation(_loadedAnimations[i]);
                _loadedAnimations.RemoveAt(i);
            }
        }

        /// <summary>
        /// Called when the Base Model Meshes and hierarchy are loaded.
        /// </summary>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        private void OnBaseModelLoad(AssetLoaderContext assetLoaderContext)
        {

        }
    }
}
