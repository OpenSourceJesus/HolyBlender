using System;
using System.Collections.Generic;
using TriLibCore.Utils;
#if UNITY_EDITOR
using UnityEditor;
#endif
using UnityEngine;

namespace TriLibCore
{
    /// <summary>
    /// Represents the TriLib project settings provider.
    /// You can override this behavior to store the settings in other places.
    /// </summary>
    public class TriLibSettings : ScriptableObject, ISerializationCallbackReceiver
    {
        private const int MaxSettings = 64;

        private Dictionary<string, bool> _boolPreferences;
        [SerializeField]
        [HideInInspector]
        private string[] _dictionaryBoolKeys = new string[MaxSettings];
        [SerializeField]
        [HideInInspector]
        private bool[] _dictionaryBoolValues = new bool[MaxSettings];
        [SerializeField]
        [HideInInspector]
        private int _settingsCount;

        private static TriLibSettings GetTriLibPreferences(bool createPreferences = true)
        {
            var preferencesFiles = Resources.LoadAll<TriLibSettings>("TriLibSettings");
            TriLibSettings triLibSettings;
            if (preferencesFiles.Length == 0)
            {
#if UNITY_EDITOR
                if (createPreferences)
                {
                    var triLibDirectories = AssetDatabase.FindAssets("TriLibMainFolderPlaceholder");
                    var triLibDirectory = triLibDirectories.Length > 0 ? FileUtils.GetFileDirectory(AssetDatabase.GUIDToAssetPath(triLibDirectories[0])) : "";
                    triLibSettings = CreateInstance<TriLibSettings>();
                    AssetDatabase.CreateAsset(triLibSettings, $"{triLibDirectory}/TriLibSettings.asset");
                    AssetDatabase.SaveAssets();
                }
                else
                {
                    return null;
                }
#else
                throw new Exception("Could not find TriLib preferences file.");
#endif
            }
            else
            {
                if (preferencesFiles.Length > 1)
                {
                    Debug.LogWarning("There is more than one TriLibSettings asset, and there is only one allowed per project.");
                }
                triLibSettings = preferencesFiles[0];
            }
            return triLibSettings;
        }

        public Dictionary<string, bool>.Enumerator GetKvp()
        {
            return _boolPreferences.GetEnumerator();
        }

        public static bool GetBool(string key, bool createPreferences = true)
        {
            var triLibPreferences = GetTriLibPreferences(createPreferences);
            if (triLibPreferences == null)
            {
                return false;
            }
            if (triLibPreferences._boolPreferences == null || !triLibPreferences._boolPreferences.TryGetValue(key, out var value))
            {
                return false;
            }
            return value;
        }

        public static void SetBool(string key, bool value, bool createPreferences = true)
        {
            var triLibPreferences = GetTriLibPreferences(createPreferences);
            if (triLibPreferences == null)
            {
                return;
            }
            if (triLibPreferences._boolPreferences == null)
            {
                triLibPreferences._boolPreferences = new Dictionary<string, bool>();
            }
            triLibPreferences._boolPreferences[key] = value;
#if UNITY_EDITOR
            if (Application.isPlaying)
            {
                Debug.LogWarning("Can't save TriLib settings while in play mode. Please refer to the Project Settings/TriLib area.");
            }
            EditorUtility.SetDirty(triLibPreferences);
            AssetDatabase.SaveAssets();
            AssetDatabase.Refresh();
#endif
        }

        public void OnBeforeSerialize()
        {
            if (_boolPreferences == null)
            {
                return;
            }
            _settingsCount = 0;
            Array.Clear(_dictionaryBoolKeys, 0, MaxSettings);
            Array.Clear(_dictionaryBoolValues, 0, MaxSettings);
            foreach (var kvp in _boolPreferences)
            {
                _dictionaryBoolKeys[_settingsCount] = kvp.Key;
                _dictionaryBoolValues[_settingsCount] = kvp.Value;
                _settingsCount++;
            }
        }

        public void OnAfterDeserialize()
        {
            if (_boolPreferences == null)
            {
                _boolPreferences = new Dictionary<string, bool>(_settingsCount);
            }
            _boolPreferences.Clear();
            for (var i = 0; i < _settingsCount; i++)
            {
                _boolPreferences.Add(_dictionaryBoolKeys[i], _dictionaryBoolValues[i]);
            }
        }
    }
}
