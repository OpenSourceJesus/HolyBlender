#pragma warning disable 649
using System.IO;
using TriLibCore.General;
using TriLibCore.Mappers;
using UnityEngine;
#if UNITY_EDITOR
using UnityEditor;
#endif
namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a sample that loads the "TriLibSample.obj" Model from the "Models" folder
    /// using a File Stream and sample Mappers to find external Resources and Textures.
    /// </summary>
    public class LoadModelFromStreamSample : MonoBehaviour
    {
        /// <summary>
        /// Cached Asset Loader Options instance.
        /// </summary>
        private AssetLoaderOptions _assetLoaderOptions;

        /// <summary>
        /// Returns the path to the "TriLibSample.obj" Model.
        /// </summary>
        private string ModelPath
        {
            get
            {
#if UNITY_EDITOR
                return $"{Application.dataPath}/TriLib/TriLibSamples/LoadModelFromStream/Models/TriLibSampleModel.obj";
#else
                return "Models/TriLibSampleModel.obj";
#endif
            }
        }

        /// <summary>
        /// Creates the AssetLoaderOptions instance, adds the sample Mappers to it and loads the Model from a File Stream.
        /// </summary>
        /// <remarks>
        /// You can create the AssetLoaderOptions by right clicking on the Assets Explorer and selecting "TriLib->Create->AssetLoaderOptions->Pre-Built AssetLoaderOptions".
        /// You can configure the Mappers straight into the AssetLoaderOptions instance in the Editor.
        /// You can create Mapper assets from existing Mapper Scripts by right-clicking them on the Assets Explorer and selecting "Create Mapper Instance".
        /// </remarks>
        private void Start()
        {
            if (_assetLoaderOptions == null)
            {
                _assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(false, true);
                _assetLoaderOptions.ExternalDataMapper = ScriptableObject.CreateInstance<ExternalDataMapperSample>();
                _assetLoaderOptions.TextureMappers = new TextureMapper[] { ScriptableObject.CreateInstance<TextureMapperSample>() };
            }
            AssetLoader.LoadModelFromStream(File.OpenRead(ModelPath), ModelPath, null, OnLoad, OnMaterialsLoad, OnProgress, OnError, null, _assetLoaderOptions);
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
