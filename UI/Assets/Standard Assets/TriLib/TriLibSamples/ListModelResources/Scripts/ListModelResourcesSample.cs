#pragma warning disable 649
using TriLibCore.General;
using UnityEngine;
using UnityEngine.UI;
#if UNITY_EDITOR
using UnityEditor;
#endif
namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a sample that loads the "TriLibSample.obj" Model from the "Models" folder and lists the Model Resources.
    /// </summary>
    public class ListModelResourcesSample : MonoBehaviour
    {

#if UNITY_EDITOR
        /// <summary>
        /// The Model asset used to locate the filename when running in Unity Editor.
        /// </summary>
        [SerializeField]
        private Object ModelAsset;
#endif

        /// <summary>
        /// Returns the path to the "TriLibSample.obj" Model.
        /// </summary>
        private string ModelPath
        {
            get
            {
#if UNITY_EDITOR
                return AssetDatabase.GetAssetPath(ModelAsset);
#else
                return "Models/TriLibSampleModel.obj";
#endif
            }
        }

        /// <summary>
        /// The Text used to display the Model Resources.
        /// </summary>
        [SerializeField]
        private Text ResourcesText;

        /// <summary>
        /// The previously loaded GameObject, if any.
        /// </summary>
        private GameObject _loadedGameObject;

        /// <summary>
        /// Cached Asset Loader Options instance.
        /// </summary>
        private AssetLoaderOptions _assetLoaderOptions;

        /// <summary>
        /// Creates the AssetLoaderOptions instance and displays the Model file-picker.
        /// </summary>
        /// <remarks>
        /// You can create the AssetLoaderOptions by right clicking on the Assets Explorer and selecting "TriLib->Create->AssetLoaderOptions->Pre-Built AssetLoaderOptions".
        /// </remarks>
        public void LoadModel()
        {
            if (_assetLoaderOptions == null)
            {
                _assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(false, true);
            }
            var assetLoaderFilePicker = AssetLoaderFilePicker.Create();
            assetLoaderFilePicker.LoadModelFromFilePickerAsync("Select a Model file", OnLoad, OnMaterialsLoad, OnProgress, OnBeginLoad, OnError, null, _assetLoaderOptions);
        }

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
        /// Called when the the Model begins to load, configuring the scene.
        /// </summary>
        /// <param name="filesSelected">Indicates if any file has been selected.</param>
        private void OnBeginLoad(bool filesSelected)
        {
            if (filesSelected)
            {
                Debug.Log($"User selected a Model.");

                //Destroys the previously loaded GameObject, if any.
                if (_loadedGameObject != null)
                {
                    Destroy(_loadedGameObject);
                }

                //Resets the Resources Text and the previous loaded GameObject.
                ResourcesText.text = "Loading Model";
                _loadedGameObject = null;
            }
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

            //The text containing all the Model Resources.
            var text = "";

            //ModelPath contains the loaded model path
            var modelPath = assetLoaderContext.Filename;
            if (!string.IsNullOrEmpty(modelPath))
            {
                text += $"Model: '{modelPath}'\n";
            }

            //Iterate the loaded textures list
            foreach (var kvp in assetLoaderContext.LoadedCompoundTextures)
            {
                //FinalPath contains the loaded texture filename
                string finalPath = kvp.Key.ResolvedFilename;
                if (!string.IsNullOrEmpty(finalPath))
                {
                    text += $"Texture: '{finalPath}'\n";
                }
            }

            //Iterate the loaded resources list
            foreach (var kvp in assetLoaderContext.LoadedExternalData)
            {
                //FinalPath contains the loaded resource filename
                string finalPath = kvp.Value;
                if (!string.IsNullOrEmpty(finalPath))
                {
                    text += $"External Data: '{finalPath}'\n";
                }
            }

            //Displays the Model Resources text.
            ResourcesText.text = text;
        }

        /// <summary>
        /// Called when the Model Meshes and hierarchy are loaded.
        /// </summary>
        /// <remarks>The loaded GameObject is available on the assetLoaderContext.RootGameObject field.</remarks>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        private void OnLoad(AssetLoaderContext assetLoaderContext)
        {
            Debug.Log("Model loaded. Loading materials.");

            //Stores the loaded GameObject reference.
            _loadedGameObject = assetLoaderContext.RootGameObject;
        }
    }
}
