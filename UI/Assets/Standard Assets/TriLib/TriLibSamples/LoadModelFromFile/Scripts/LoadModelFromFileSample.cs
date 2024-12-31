#pragma warning disable 649
using TriLibCore.General;
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif
namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a sample that loads the "TriLibSample.obj" Model from the "Models" folder.
    /// </summary>
    public class LoadModelFromFileSample : MonoBehaviour
    {
        /// <summary>
        /// Returns the path to the "TriLibSample.obj" Model.
        /// </summary>
        private string ModelPath
        {
            get
            {
#if UNITY_EDITOR
                return $"{Application.dataPath}/TriLib/TriLibSamples/LoadModelFromFile/Models/TriLibSampleModel.obj";
#else
                return "Models/TriLibSampleModel.obj";
#endif
            }
        }

        /// <summary>
        /// Cached Asset Loader Options instance.
        /// </summary>
        private AssetLoaderOptions _assetLoaderOptions;

        /// <summary>
        /// Loads the "Models/TriLibSample.obj" Model using the given AssetLoaderOptions.
        /// </summary>
        /// <remarks>
        /// You can create the AssetLoaderOptions by right clicking on the Assets Explorer and selecting "TriLib->Create->AssetLoaderOptions->Pre-Built AssetLoaderOptions".
        /// </remarks>
        private void Start()
        {
            if (_assetLoaderOptions == null)
            {
                _assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(false, true);
            }
            AssetLoader.LoadModelFromFile(ModelPath, OnLoad, OnMaterialsLoad, OnProgress, OnError, null, _assetLoaderOptions);
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
        /// Called when the Model loading progress changes.
        /// </summary>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        /// <param name="progress">The loading progress.</param>
        private void OnProgress(AssetLoaderContext assetLoaderContext, float progress)
        {
            Debug.Log($"Loading Model. Progress: {progress:P}");
        }

        /// <summary>
        /// Called when the Model (including Textures and Materials) has been fully loaded.
        /// </summary>
        /// <remarks>The loaded GameObject is available on the assetLoaderContext.RootGameObject field.</remarks>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        private void OnMaterialsLoad(AssetLoaderContext assetLoaderContext)
        {
            Debug.Log("Materials loaded. Model fully loaded.");
        }

        /// <summary>
        /// Called when the Model Meshes and hierarchy are loaded.
        /// </summary>
        /// <remarks>The loaded GameObject is available on the assetLoaderContext.RootGameObject field.</remarks>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        private void OnLoad(AssetLoaderContext assetLoaderContext)
        {
            Debug.Log("Model loaded. Loading materials.");
        }
    }
}
