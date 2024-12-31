#pragma warning disable 649

using System.Collections.Generic;
using TriLibCore.Extensions;
using UnityEngine;
using UnityEngine.UI;
#if UNITY_EDITOR
using UnityEditor;
#endif

namespace TriLibCore.Samples
{
    /// <summary>
    /// Represents a sample that allows users to load a Model using the built-in File-Picker and displays the Model User Properties.
    /// </summary>
    public class UserPropertiesLoadingSample : MonoBehaviour
    {
        /// <summary>
        /// The Dictionaries containing the Model Properties sorted by type.
        /// </summary>
        private Dictionary<string, float> _floatValues;
        private Dictionary<string, int> _intValues;
        private Dictionary<string, Vector2> _vector2Values;
        private Dictionary<string, Vector3> _vector3Values;
        private Dictionary<string, Vector4> _vector4Values;
        private Dictionary<string, Color> _colorValues;
        private Dictionary<string, bool> _boolValues;
        private Dictionary<string, string> _stringValues;

        /// <summary>
        /// The last loaded GameObject.
        /// </summary>
        private GameObject _loadedGameObject;

        /// <summary>
        /// The load Model Button.
        /// </summary>
        [SerializeField]
        private Button _loadModelButton;

        /// <summary>
        /// The progress indicator Text;
        /// </summary>
        [SerializeField]
        private Text _progressText;

        /// <summary>
        /// The properties listing Text;
        /// </summary>
        [SerializeField]
        private Text _propertiesText;

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
                return $"{Application.dataPath}/TriLib/TriLibSamples/UserPropertiesLoading/Models/WithMyData.fbx";
#else
                return "Models/WithMyData.fbx";
#endif
            }
        }

        /// <summary>
        /// The callback passed to our custom UserPropertiesMapper, called for every Model and its every User Property.
        /// </summary>
        /// <param name="gameObject">The GameObject containing the User Property.</param>
        /// <param name="propertyName">The User Property name.</param>
        /// <param name="propertyValue">The User Property value.</param>
        private void OnUserDataProcessed(GameObject gameObject, string propertyName, object propertyValue)
        {
            var propertyKey = $"{gameObject.name}.{propertyName}";
            switch (propertyValue)
            {
                case float floatValue:
                    if (!_floatValues.ContainsKey(propertyKey))
                    {
                        _floatValues.Add(propertyKey, floatValue);
                    }
                    break;
                case int intValue:
                    if (!_intValues.ContainsKey(propertyKey))
                    {
                        _intValues.Add(propertyKey, intValue);
                    }
                    break;
                case Vector2 vector2Value:
                    if (!_vector2Values.ContainsKey(propertyKey))
                    {
                        _vector2Values.Add(propertyKey, vector2Value);
                    }
                    break;
                case Vector3 vector3Value:
                    if (!_vector3Values.ContainsKey(propertyKey))
                    {
                        _vector3Values.Add(propertyKey, vector3Value);
                    }
                    break;
                case Vector4 vector4Value:
                    if (!_vector4Values.ContainsKey(propertyKey))
                    {
                        _vector4Values.Add(propertyKey, vector4Value);
                    }
                    break;
                case Color colorValue:
                    if (!_colorValues.ContainsKey(propertyKey))
                    {
                        _colorValues.Add(propertyKey, colorValue);
                    }
                    break;
                case bool boolValue:
                    if (!_boolValues.ContainsKey(propertyKey))
                    {
                        _boolValues.Add(propertyKey, boolValue);
                    }
                    break;
                case string stringValue:
                    if (!_stringValues.ContainsKey(propertyKey))
                    {
                        _stringValues.Add(propertyKey, stringValue);
                    }
                    break;
            }
        }

        /// <summary>
        /// Creates the AssetLoaderOptions instance and displays the Model file-picker.
        /// It also creates our custom UserPropertiesMapper (SampleUserPropertiesMapper) instance and passes a callback function to it.
        /// </summary>
        /// <remarks>
        /// You can create the AssetLoaderOptions by right clicking on the Assets Explorer and selecting "TriLib->Create->AssetLoaderOptions->Pre-Built AssetLoaderOptions".
        /// </remarks>
        public void LoadModel()
        {
            var assetLoaderOptions = CreateAssetLoaderOptions();
            var assetLoaderFilePicker = AssetLoaderFilePicker.Create();
            assetLoaderFilePicker.LoadModelFromFilePickerAsync("Select a Model file", OnLoad, OnMaterialsLoad, OnProgress, OnBeginLoad, OnError, null, assetLoaderOptions);
        }

        /// <summary>
        /// Creates an AssetLoaderOptions with the sample UserPropertiesMapper.
        /// </summary>
        /// <returns>The created AssetLoaderOptions.</returns>
        private AssetLoaderOptions CreateAssetLoaderOptions()
        {
            if (_assetLoaderOptions == null)
            {
                _assetLoaderOptions = AssetLoader.CreateDefaultLoaderOptions(false, true);
                var userPropertiesMapper = ScriptableObject.CreateInstance<SampleUserPropertiesMapper>();
                userPropertiesMapper.OnUserDataProcessed += OnUserDataProcessed;
                _assetLoaderOptions.UserPropertiesMapper = userPropertiesMapper;
            }
            return _assetLoaderOptions;
        }

        /// <summary>
        /// Called when the the Model begins to load, configuring the scene.
        /// </summary>
        /// <param name="filesSelected">Indicates if any file has been selected.</param>
        private void OnBeginLoad(bool filesSelected)
        {
            _floatValues = new Dictionary<string, float>();
            _intValues = new Dictionary<string, int>();
            _vector2Values = new Dictionary<string, Vector2>();
            _vector3Values = new Dictionary<string, Vector3>();
            _vector4Values = new Dictionary<string, Vector4>();
            _colorValues = new Dictionary<string, Color>();
            _boolValues = new Dictionary<string, bool>();
            _stringValues = new Dictionary<string, string>();
            _loadModelButton.interactable = !filesSelected;
            _progressText.enabled = filesSelected;
            _progressText.text = string.Empty;
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
            _progressText.text = $"Progress: {progress:P}";
        }

        /// <summary>
        /// Called when the Model (including Textures and Materials) has been fully loaded.
        /// </summary>
        /// <remarks>The loaded GameObject is available on the assetLoaderContext.RootGameObject field.</remarks>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        private void OnMaterialsLoad(AssetLoaderContext assetLoaderContext)
        {
            if (assetLoaderContext.RootGameObject != null)
            {
                Debug.Log("Model fully loaded.");
                ListProperties();
            }
            else
            {
                Debug.Log("Model could not be loaded.");
            }
            _loadModelButton.interactable = true;
            _progressText.enabled = false;
        }

        /// <summary>
        /// Updates the User Properties Text content with the loaded Model User Properties, categorizing the Properties by type.
        /// </summary>
        private void ListProperties()
        {
            var text = string.Empty;
            if (_stringValues.Count > 0)
            {
                text += "<b>String</b>\n";
                foreach (var kvp in _stringValues)
                {
                    text += $"{kvp.Key}=\"{kvp.Value}\"\n";
                }
            }
            if (_floatValues.Count > 0)
            {
                text += "\n<b>Float</b>\n";
                foreach (var kvp in _floatValues)
                {
                    text += $"{kvp.Key}={kvp.Value}\n";
                }
            }
            if (_intValues.Count > 0)
            {
                text += "\n<b>Integer</b>\n";
                foreach (var kvp in _intValues)
                {
                    text += $"{kvp.Key}={kvp.Value}\n";
                }
            }
            if (_boolValues.Count > 0)
            {
                text += "\n<b>Boolean</b>\n";
                foreach (var kvp in _boolValues)
                {
                    text += $"{kvp.Key}={kvp.Value}\n";
                }
            }
            if (_vector2Values.Count > 0)
            {
                text += "\n<b>Vector2</b>\n";
                foreach (var kvp in _vector2Values)
                {
                    text += $"{kvp.Key}={kvp.Value}\n";
                }
            }
            if (_vector3Values.Count > 0)
            {
                text += "\n<b>Vector3</b>\n";
                foreach (var kvp in _vector3Values)
                {
                    text += $"{kvp.Key}={kvp.Value}\n";
                }
            }
            if (_vector4Values.Count > 0)
            {
                text += "\n<b>Vector4</b>\n";
                foreach (var kvp in _vector4Values)
                {
                    text += $"{kvp.Key}={kvp.Value}\n";
                }
            }
            if (_colorValues.Count > 0)
            {
                text += "\n<b>Color</b>\n";
                foreach (var kvp in _colorValues)
                {
                    text += "<color=#" + ColorUtility.ToHtmlStringRGB(kvp.Value) + ">";
                    text += $"{kvp.Key}={kvp.Value}\n";
                    text += "</color>";
                }
            }
            _propertiesText.text = string.IsNullOrEmpty(text) ? "The model has no user properties" : $"<b>Model User Properties</b>\n\n{text}";
        }

        /// <summary>
        /// Called when the Model Meshes and hierarchy are loaded.
        /// </summary>
        /// <remarks>The loaded GameObject is available on the assetLoaderContext.RootGameObject field.</remarks>
        /// <param name="assetLoaderContext">The context used to load the Model.</param>
        private void OnLoad(AssetLoaderContext assetLoaderContext)
        {
            if (_loadedGameObject != null)
            {
                Destroy(_loadedGameObject);
            }
            _loadedGameObject = assetLoaderContext.RootGameObject;
            if (_loadedGameObject != null)
            {
                Camera.main.FitToBounds(assetLoaderContext.RootGameObject, 4f);
            }
        }

        /// <summary>
        /// Loads the sample Model.
        /// </summary>
        private void Start()
        {
            var assetLoaderOptions = CreateAssetLoaderOptions();
            OnBeginLoad(true); //Workaround to create lists
            AssetLoader.LoadModelFromFile(ModelPath, OnLoad, OnMaterialsLoad, OnProgress, OnError, null, assetLoaderOptions);
        }
    }
}
