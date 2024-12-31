using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
#if UNITY_EDITOR
using UnityEditor;
#endif
using System.Reflection;
using System;
using Extensions;
using UnityEngine.UI;

namespace HolyBlender
{
	//[ExecuteInEditMode]
	public class ConfigurationManager : SingletonMonoBehaviour<ConfigurationManager>
	{
		[HideInInspector]
		public string configFilePath;
		public List<MonoBehaviour> configurableMonobehaviours;
		List<IConfigurable> configurables = new List<IConfigurable>();
		public Dictionary<IConfigurable, string> configurableCatergories = new Dictionary<IConfigurable, string>();
		public const string INDENT = " - ";
		public const string VALUE_SEPERATOR = ", ";
		public const string OBJECT_SEPERATOR = "----------";
		public const string CATEGORY_SEPERATOR = "------------------------------";
		static StreamReader fileReader;
		static StreamWriter fileWriter;
		public Canvas canvas;
		
		#if UNITY_EDITOR
		public override void Awake ()
		{
			base.Awake ();
			// configurableCatergories.Clear();
			configFilePath = Application.dataPath + "/.config";
			int initConfigurablesCount = configurableMonobehaviours.Count;
			for (int i = 0; i < initConfigurablesCount; i ++)
			{
				IConfigurable configurable = configurableMonobehaviours[i] as IConfigurable;
				configurables.Add(configurable);
				configurableCatergories.Add(configurable, configurable.Category);
			}
		}
		#endif
		
		public void _MakeConfigFile ()
		{
			MakeConfigFile ();
		}
		
		public void _ApplyConfigFile ()
		{
			ApplyConfigFile ();
		}
		
		#if UNITY_EDITOR
		[MenuItem("Configuration/Make Config File")]
		#endif
		public static void MakeConfigFile ()
		{
			if (File.Exists(ConfigurationManager.Instance.configFilePath))
				File.Delete(ConfigurationManager.Instance.configFilePath);
			fileWriter = File.CreateText(ConfigurationManager.Instance.configFilePath);
			string[] config;
			List<string> finishedCategories = new List<string>();
			foreach (string category in ConfigurationManager.Instance.configurableCatergories.Values)
			{
				if (!finishedCategories.Contains(category))
				{
					fileWriter.WriteLine(CATEGORY_SEPERATOR + category + CATEGORY_SEPERATOR);
					foreach (IConfigurable configurable in ConfigurationManager.Instance.configurableCatergories.Keys)
					{
						if (configurable.Category == category)
						{
							fileWriter.WriteLine(OBJECT_SEPERATOR + configurable.Name);
							config = GetConfiguration(configurable);
							foreach (string value in config)
								fileWriter.WriteLine(value);
						}
					}
					finishedCategories.Add(category);
				}
			}
			fileWriter.Close();
		}
			
		#if UNITY_EDITOR
		[MenuItem("Configuration/Apply Config File")]
		#endif
		public static void ApplyConfigFile ()
		{
			fileReader = File.OpenText(ConfigurationManager.Instance.configFilePath);
			foreach (string category in ConfigurationManager.Instance.configurableCatergories.Values)
			{
				fileReader.ReadLine();
				foreach (IConfigurable configurable in ConfigurationManager.Instance.configurableCatergories.Keys)
				{
					if (configurable.Category == category)
					{
						fileReader.ReadLine();
						SetConfiguration (configurable);
					}
				}
			}
			fileReader.Close();
		}
		
		public static string[] GetConfiguration (IConfigurable configurable)
		{
			List<string> output = new List<string>();
			PropertyInfo[] properties = configurable.GetType().GetProperties();
			for (int i = 0; i < properties.Length; i ++)
			{
				PropertyInfo property = properties[i];
				MakeConfigurable makeConfigurable = Attribute.GetCustomAttribute(property, typeof(MakeConfigurable)) as MakeConfigurable;
				if (makeConfigurable != null)
				{
					if (property.PropertyType.IsArray)
					{
						string outputEntry = property.Name + ": ";
						Array array = (Array) property.GetValue(configurable, null);
						for (int i2 = 0; i2 < array.Length; i2 ++)
							outputEntry += ((object) array.GetValue(i2)).ToString() + VALUE_SEPERATOR;
						output.Add(outputEntry);
					}
					else
					{
						output.Add(property.Name + ": " + property.GetValue(configurable, null).ToString());
					}
				}
			}
			FieldInfo[] fields = configurable.GetType().GetFields();
			for (int i = 0; i < fields.Length; i ++)
			{
				FieldInfo field = fields[i];
				MakeConfigurable makeConfigurable = Attribute.GetCustomAttribute(field, typeof(MakeConfigurable)) as MakeConfigurable;
				if (makeConfigurable != null)
				{
					if (field.FieldType.IsArray)
					{
						string outputEntry = field.Name + ": ";
						Array array = (Array) field.GetValue(configurable);
						for (int i2 = 0; i2 < array.Length; i2 ++)
							outputEntry += ((object) array.GetValue(i2)).ToString() + VALUE_SEPERATOR;
						output.Add(outputEntry);
					}
					else
					{
						output.Add(field.Name + ": " + field.GetValue(configurable).ToString());
					}
				}
			}
			return output.ToArray();
		}
		
		public static void SetConfiguration (IConfigurable configurable)
		{
			PropertyInfo[] properties = configurable.GetType().GetProperties();
			for (int i = 0; i < properties.Length; i ++)
			{
				PropertyInfo property = properties[i];
				MakeConfigurable makeConfigurable = Attribute.GetCustomAttribute(property, typeof(MakeConfigurable)) as MakeConfigurable;
				if (makeConfigurable != null)
				{
					if (property.PropertyType.IsArray)
					{
						string value = fileReader.ReadLine();
						value = value.RemoveEach(property.Name + ": ");
						Array array = (Array) property.GetValue(configurable, null);
						for (int i2 = 0; i2 < array.Length; i2 ++)
						{
							if (array.GetValue(i2) is float)
								property.SetValue(configurable, float.Parse(value.Substring(0, value.IndexOf(", "))), new object[] { i2 });
							else if (array.GetValue(i2) is int)
								property.SetValue(configurable, int.Parse(value), new object[] { i2 });
							else if (array.GetValue(i2) is bool)
								property.SetValue(configurable, bool.Parse(value), new object[] { i2 });
							value = value.Remove(0, value.IndexOf(", "));
						}
					}
					else
					{
						string value = fileReader.ReadLine();
						value = value.RemoveEach(property.Name + ": ");
						if (property.PropertyType == typeof(float))
							property.SetValue(configurable, float.Parse(value), null);
						else if (property.PropertyType == typeof(int))
							property.SetValue(configurable, int.Parse(value), null);
						else if (property.PropertyType == typeof(bool))
							property.SetValue(configurable, bool.Parse(value), null);
					}
					
				}
			}
			FieldInfo[] fields = configurable.GetType().GetFields();
			for (int i = 0; i < fields.Length; i ++)
			{
				FieldInfo field = fields[i];
				MakeConfigurable makeConfigurable = Attribute.GetCustomAttribute(field, typeof(MakeConfigurable)) as MakeConfigurable;
				if (makeConfigurable != null)
				{
					if (field.FieldType.IsArray)
					{
						string value = fileReader.ReadLine();
						value = value.RemoveEach(field.Name + ": ");
						if (field.GetValue(configurable) is float[])
						{
							List<float> values = new List<float>();
							while (value.Contains(VALUE_SEPERATOR))
							{
								values.Add(float.Parse(value.Substring(0, value.IndexOf(VALUE_SEPERATOR))));
								value = value.Remove(0, value.IndexOf(VALUE_SEPERATOR) + VALUE_SEPERATOR.Length);
							}
							field.SetValue(configurable, values.ToArray());
						}
						else if (field.GetValue(configurable) is int[])
						{
							List<int> values = new List<int>();
							while (value.Contains(VALUE_SEPERATOR))
							{
								values.Add(int.Parse(value.Substring(0, value.IndexOf(VALUE_SEPERATOR))));
								value = value.Remove(0, value.IndexOf(VALUE_SEPERATOR) + VALUE_SEPERATOR.Length);
							}
							field.SetValue(configurable, values.ToArray());
						}
						else if (field.GetValue(configurable) is bool[])
						{
							List<bool> values = new List<bool>();
							while (value.Contains(VALUE_SEPERATOR))
							{
								values.Add(bool.Parse(value.Substring(0, value.IndexOf(VALUE_SEPERATOR))));
								value = value.Remove(0, value.IndexOf(VALUE_SEPERATOR) + VALUE_SEPERATOR.Length);
							}
							field.SetValue(configurable, values.ToArray());
						}
					}
					else
					{
						string value = fileReader.ReadLine();
						value = value.RemoveEach(field.Name + ": ");
						if (field.FieldType == typeof(float))
							field.SetValue(configurable, float.Parse(value));
						else if (field.FieldType == typeof(int))
							field.SetValue(configurable, int.Parse(value));
						else if (field.FieldType == typeof(bool))
							field.SetValue(configurable, bool.Parse(value));
					}
				}
			}
		}
	}
}