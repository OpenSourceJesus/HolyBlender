#if UNITY_EDITOR
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using HolyBlender;
using UnityEditor;

namespace Extensions
{
	public static class EditorPrefsExtensions
	{
		public const bool USE_REGISTRY = false;
		public const string REGISTRY_KEY = "All Keys And Values";
		public const string REGISTRY_SEPERATOR = "↕";
		public const string REGISTRY_ENTRY_DATA_SEPARATOR = "↔";
		
		public static void SetBool (string key, bool value, bool registerKey = USE_REGISTRY)
		{
			EditorPrefs.SetBool(key, value);
			if (registerKey)
				RegisterKey (key, EditorPrefsValueType.Bool);
		}
		
		public static void SetInt (string key, int value, bool registerKey = USE_REGISTRY)
		{
			EditorPrefs.SetInt(key, value);
			if (registerKey)
				RegisterKey (key, EditorPrefsValueType.Int);
		}

		public static void SetFloat (string key, float value, bool registerKey = USE_REGISTRY)
		{
			EditorPrefs.SetFloat(key, value);
			if (registerKey)
				RegisterKey (key, EditorPrefsValueType.Float);
		}

		public static void SetString (string key, string value, bool registerKey = USE_REGISTRY)
		{
			EditorPrefs.SetString(key, value);
			if (registerKey)
				RegisterKey (key, EditorPrefsValueType.String);
		}
		
		public static Color GetColor (string key)
		{
			return GetColor(key, Color.black.SetAlpha(0));
		}
		
		public static Color GetColor (string key, Color defaultValue)
		{
			return new Color(EditorPrefs.GetFloat(key + ".r", defaultValue.r), EditorPrefs.GetFloat(key + ".g", defaultValue.g), EditorPrefs.GetFloat(key + ".b", defaultValue.b), EditorPrefs.GetFloat(key + ".a", defaultValue.a));
		}
		
		public static void SetColor (string key, Color value, bool registerKey = USE_REGISTRY)
		{
			SetFloat (key + ".r", value.r, registerKey);
			SetFloat (key + ".g", value.g, registerKey);
			SetFloat (key + ".b", value.b, registerKey);
			SetFloat (key + ".a", value.a, registerKey);
		}
		
		public static Vector2 GetVector2 (string key, Vector2 defaultValue = new Vector2())
		{
			return new Vector2(EditorPrefs.GetFloat(key + ".x", defaultValue.x), EditorPrefs.GetFloat(key + ".y", defaultValue.y));
		}
		
		public static void SetVector2 (string key, Vector2 value, bool registerKey = USE_REGISTRY)
		{
			SetFloat (key + ".x", value.x, registerKey);
			SetFloat (key + ".y", value.y, registerKey);
		}
		
		public static Vector2Int GetVector2Int (string key, Vector2Int defaultValue = new Vector2Int())
		{
			return new Vector2Int(EditorPrefs.GetInt(key + ".x", defaultValue.x), EditorPrefs.GetInt(key + ".y", defaultValue.y));
		}
		
		public static void SetVector2Int (string key, Vector2Int value, bool registerKey = USE_REGISTRY)
		{
			SetInt (key + ".x", value.x, registerKey);
			SetInt (key + ".y", value.y, registerKey);
		}

		public static void RegisterKey (string key, EditorPrefsValueType valueType)
		{
			string value = "";
			if (valueType == EditorPrefsValueType.Bool)
				value = "" + EditorPrefs.GetBool(key);
			else if (valueType == EditorPrefsValueType.Int)
				value = "" + EditorPrefs.GetInt(key);
			else if (valueType == EditorPrefsValueType.Float)
				value = "" + EditorPrefs.GetFloat(key);
			else
				value = EditorPrefs.GetString(key);
			string registry = EditorPrefs.GetString(REGISTRY_KEY, "");
			int indexOfKey = registry.IndexOf(key);
			if (indexOfKey != -1)
				registry = registry.RemoveStartEnd(indexOfKey, indexOfKey + registry.StartAfter(key).IndexOf(REGISTRY_SEPERATOR) + 1 + key.Length);
			EditorPrefs.SetString(REGISTRY_KEY, registry + key + REGISTRY_ENTRY_DATA_SEPARATOR + value + REGISTRY_ENTRY_DATA_SEPARATOR + valueType.ToString() + REGISTRY_SEPERATOR);
		}

		public static void DeregisterKey (string key)
		{
			string registry = EditorPrefs.GetString(REGISTRY_KEY, "");
			int indexOfKey = registry.IndexOf(key);
			if (indexOfKey != -1)
				registry = registry.RemoveStartEnd(indexOfKey, indexOfKey + registry.StartAfter(key).IndexOf(REGISTRY_SEPERATOR) + 1 + key.Length);
			EditorPrefs.SetString(REGISTRY_KEY, registry);
		}

		public static void DeleteKey (string key, bool deregisterKey = USE_REGISTRY)
		{
			EditorPrefs.DeleteKey(key);
			if (deregisterKey)
				DeregisterKey (key);
		}

		public enum EditorPrefsValueType
		{
			Bool,
			Int,
			Float,
			String
		}
	}
}
#endif