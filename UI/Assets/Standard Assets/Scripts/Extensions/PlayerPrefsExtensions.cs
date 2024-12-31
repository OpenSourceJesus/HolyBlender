using UnityEngine;
using System.Collections;
using System.Collections.Generic;

namespace Extensions
{
	public static class PlayerPrefsExtensions
	{
		public static bool GetBool (string key, bool defaultValue = false)
		{
			return PlayerPrefs.GetInt(key, defaultValue.GetHashCode()) == 1;
		}
		
		public static void SetBool (string key, bool value)
		{
			PlayerPrefs.SetInt(key, value.GetHashCode());
		}
		
		public static Color GetColor (string key)
		{
			return GetColor(key, Color.black.SetAlpha(0));
		}
		
		public static Color GetColor (string key, Color defaultValue)
		{
			return new Color(PlayerPrefs.GetFloat(key + ".r", defaultValue.r), PlayerPrefs.GetFloat(key + ".g", defaultValue.g), PlayerPrefs.GetFloat(key + ".b", defaultValue.b), PlayerPrefs.GetFloat(key + ".a", defaultValue.a));
		}
		
		public static void SetColor (string key, Color value)
		{
			PlayerPrefs.SetFloat(key + ".r", value.r);
			PlayerPrefs.SetFloat(key + ".g", value.g);
			PlayerPrefs.SetFloat(key + ".b", value.b);
			PlayerPrefs.SetFloat(key + ".a", value.a);
		}
		
		public static Vector2 GetVector2 (string key, Vector2 defaultValue = new Vector2())
		{
			return new Vector2(PlayerPrefs.GetFloat(key + ".x", defaultValue.x), PlayerPrefs.GetFloat(key + ".y", defaultValue.y));
		}
		
		public static void SetVector2 (string key, Vector2 value)
		{
			PlayerPrefs.SetFloat(key + ".x", value.x);
			PlayerPrefs.SetFloat(key + ".y", value.y);
		}
		
		public static float[] GetFloatArray (string key, float[] defaultValue = null)
		{
			List<float> output = new List<float>();
			int index = 0;
			while (PlayerPrefs.HasKey(key + "[" + index + "]"))
			{
				output.Add(PlayerPrefs.GetFloat(key + "[" + index + "]", defaultValue[index]));
				index ++;
			}
			return output.ToArray();
		}
		
		public static void SetFloatArray (string key, float[] value)
		{
			for (int i = 0; i < value.Length; i ++)
				PlayerPrefs.SetFloat(key + "[" + i + "]", value[i]);
		}
	}
}