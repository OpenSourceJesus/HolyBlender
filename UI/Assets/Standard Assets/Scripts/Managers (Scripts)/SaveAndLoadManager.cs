using System;
using System.IO;
using Extensions;
using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.Serialization.Formatters.Binary;

namespace HolyBlender
{
	public class SaveAndLoadManager : SingletonMonoBehaviour<SaveAndLoadManager>
	{
#if !UNITY_WEBGL
		static string SAVE_FILE_PATH;
		static SaveData saveData = new SaveData();

		public static void Init ()
		{
			SAVE_FILE_PATH = Application.persistentDataPath + Path.DirectorySeparatorChar + "Save Data";
			print(SAVE_FILE_PATH);
			if (BuildManager.IsFirstStartup)
			{
				PlayerPrefs.DeleteAll();
				if (File.Exists(SAVE_FILE_PATH))
					File.Delete(SAVE_FILE_PATH);
				BuildManager.IsFirstStartup = false;
			}
			saveData.boolDict = new Dictionary<string, bool>();
			saveData.intDict = new Dictionary<string, int>();
			saveData.floatDict = new Dictionary<string, float>();
			saveData.stringDict = new Dictionary<string, string>();
			saveData.vector2Dict = new Dictionary<string, Vector2>();
			saveData.boolArrayDict = new Dictionary<string, bool[]>();
			saveData.vector2IntArrayDict = new Dictionary<string, _Vector2Int[]>();
			if (File.Exists(SAVE_FILE_PATH))
				Load ();
		}

		static void OnAboutToSave ()
		{
			saveData.blenderPath = HolyBlender.Instance.blenderPathInputField.text;
			saveData.blendFilePath = HolyBlender.instance.blendFilePathInputField.text;
		}

		public static void Save ()
		{
			OnAboutToSave ();
			FileStream fileStream = new FileStream(SAVE_FILE_PATH, FileMode.Create);
			BinaryFormatter binaryFormatter = new BinaryFormatter();
			binaryFormatter.Serialize(fileStream, saveData);
			fileStream.Close();
		}

		static void OnLoad ()
		{
			HolyBlender.Instance.blenderPathInputField.text = saveData.blenderPath;
			HolyBlender.instance.blendFilePathInputField.text = saveData.blendFilePath;
		}

		public static void Load ()
		{
			FileStream fileStream = new FileStream(SAVE_FILE_PATH, FileMode.Open);
			BinaryFormatter binaryFormatter = new BinaryFormatter();
			saveData = (SaveData) binaryFormatter.Deserialize(fileStream);
			fileStream.Close();
			OnLoad ();
		}
#endif

		public static bool GetBool (string key, bool value = false)
		{
#if UNITY_WEBGL
			return PlayerPrefs.GetInt(key, value.GetHashCode()) == 1;
#else
			bool output = false;
			if (saveData.boolDict.TryGetValue(key, out output))
				return output;
			else
				return value;
#endif
		}

		public static void SetBool (string key, bool value)
		{
#if UNITY_WEBGL
			PlayerPrefs.SetInt(key, value.GetHashCode());
#else
			saveData.boolDict[key] = value;
#endif
		}

		public static int GetInt (string key, int value = 0)
		{
#if UNITY_WEBGL
			return PlayerPrefs.GetInt(key, value);
#else
			int output = 0;
			if (saveData.intDict.TryGetValue(key, out output))
				return output;
			else
				return value;
#endif
		}

		public static void SetInt (string key, int value)
		{
#if UNITY_WEBGL
			PlayerPrefs.SetInt(key, value);
#else
			saveData.intDict[key] = value;
#endif
		}

		public static float GetFloat (string key, float value = 0)
		{
#if UNITY_WEBGL
			return PlayerPrefs.GetFloat(key, value);
#else
			float output = 0;
			if (saveData.floatDict.TryGetValue(key, out output))
				return output;
			else
				return value;
#endif
		}

		public static void SetFloat (string key, float value)
		{
#if UNITY_WEBGL
			PlayerPrefs.SetFloat(key, value);
#else
			saveData.floatDict[key] = value;
#endif
		}

		public static Vector2 GetVector2 (string key, Vector2 value = new Vector2())
		{
#if UNITY_WEBGL
			return new Vector2(PlayerPrefs.GetFloat(key + ".x", value.x), PlayerPrefs.GetFloat(key + ".y", value.y));
#else
			Vector2 output = new Vector2();
			if (saveData.vector2Dict.TryGetValue(key, out output))
				return output;
			else
				return value;
#endif
		}

		public static void SetVector2 (string key, Vector2 value)
		{
#if UNITY_WEBGL
			PlayerPrefs.SetFloat(key + ".x", value.x);
			PlayerPrefs.SetFloat(key + ".y", value.y);
#else
			saveData.vector2Dict[key] = value;
#endif
		}

		public static _Vector2Int[] GetVector2IntArray (string key, _Vector2Int[] values = null)
		{
#if UNITY_WEBGL
			List<_Vector2Int> output = new List<_Vector2Int>();
			int index = 0;
			while (PlayerPrefs.HasKey(key + "[" + index + "].x"))
			{
				output.Add(new _Vector2Int(PlayerPrefs.GetInt(key + "[" + index + "].x"), PlayerPrefs.GetInt(key + "[" + index + "].y")));
				index ++;
			}
			if (output.Count == 0)
				return values;
			else
				return output.ToArray();
#else
			_Vector2Int[] output = new _Vector2Int[0];
			if (saveData.vector2IntArrayDict.TryGetValue(key, out output))
				return output;
			else
				return values;
#endif
		}

		public static void SetVector2IntArray (string key, _Vector2Int[] values)
		{
#if UNITY_WEBGL
			for (int i = 0; i < values.Length; i ++)
			{
				_Vector2Int value = values[i];
				PlayerPrefs.SetInt(key + "[" + i + "].x", value.x);
				PlayerPrefs.SetInt(key + "[" + i + "].y", value.y);
			}
			int index = values.Length;
			while (PlayerPrefs.HasKey(key + "[" + index + "].x"))
			{
				PlayerPrefs.DeleteKey(key + "[" + index + "].x");
				PlayerPrefs.DeleteKey(key + "[" + index + "].y");
				index ++;
			}
#else
			saveData.vector2IntArrayDict[key] = values;
#endif
		}

		public static bool[] GetBoolArray (string key, bool[] values = null)
		{
#if UNITY_WEBGL
			List<bool> output = new List<bool>();
			int index = 0;
			while (PlayerPrefs.HasKey(key + "[" + index + "]"))
			{
				output.Add(PlayerPrefsExtensions.GetBool(key + "[" + index + "]"));
				index ++;
			}
			if (output.Count == 0)
				return values;
			else
				return output.ToArray();
#else
			bool[] output = new bool[0];
			if (saveData.boolArrayDict.TryGetValue(key, out output))
				return output;
			else
				return values;
#endif
		}

		public static void SetBoolArray (string key, bool[] values)
		{
#if UNITY_WEBGL
			for (int i = 0; i < values.Length; i ++)
			{
				bool value = values[i];
				PlayerPrefsExtensions.SetBool (key + "[" + i + "]", value);
			}
			int index = values.Length;
			while (PlayerPrefs.HasKey(key + "[" + index + "]"))
			{
				PlayerPrefs.DeleteKey(key + "[" + index + "]");
				index ++;
			}
#else
			saveData.boolArrayDict[key] = values;
#endif
		}

		public static string GetString (string key, string value = "")
		{
#if UNITY_WEBGL
			return PlayerPrefs.GetString(key, value);
#else
			string output = null;
			if (saveData.stringDict.TryGetValue(key, out output))
				return output;
			else
				return value;
#endif
		}

		public static void SetString (string key, string value)
		{
#if UNITY_WEBGL
			PlayerPrefs.SetString(key, value);
#else
			saveData.stringDict[key] = value;
#endif
		}

		public static void DeleteKey (string key)
		{
#if UNITY_WEBGL
			PlayerPrefs.DeleteKey(key);
#else
			if (saveData.boolDict.Remove(key))
				return;
			else if (saveData.intDict.Remove(key))
				return;
			else if (saveData.floatDict.Remove(key))
				return;
			else if (saveData.vector2Dict.Remove(key))
				return;
			else if (saveData.vector2IntArrayDict.Remove(key))
				return;
			else
				saveData.stringDict.Remove(key);
#endif
		}

		public static void DeleteAll (string key)
		{
#if UNITY_WEBGL
			PlayerPrefs.DeleteAll();
#else
			saveData.boolDict.Clear();
			saveData.intDict.Clear();
			saveData.floatDict.Clear();
			saveData.floatDict.Clear();
			saveData.vector2IntArrayDict.Clear();
			saveData.boolArrayDict.Clear();
			saveData.stringDict.Clear();
#endif
		}

#if !UNITY_WEBGL
		[Serializable]
		public struct SaveData
		{
			public string blenderPath;
			public string blendFilePath;
			public Dictionary<string, bool> boolDict;
			public Dictionary<string, int> intDict;
			public Dictionary<string, float> floatDict;
			public Dictionary<string, string> stringDict;
			public Dictionary<string, Vector2> vector2Dict;
			public Dictionary<string, bool[]> boolArrayDict;
			public Dictionary<string, _Vector2Int[]> vector2IntArrayDict;
		}
#endif
	}
}