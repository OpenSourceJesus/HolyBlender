using TMPro;
using System;
using System.IO;
using UnityEngine;
using UnityEngine.UI;
using TriLibCore.SFB;
using System.Diagnostics;
using System.Collections.Generic;

namespace HolyBlender
{
	public class HolyBlender : SingletonMonoBehaviour<HolyBlender>
	{
		public TMP_InputField blenderPathInputField;
		public TMP_InputField blendFilePathInputField;
		public Toggle autoExitToggle;
		public static bool AutoExit
		{
			get
			{
				return SaveAndLoadManager.saveData.autoExit;
			}
			set
			{
				SaveAndLoadManager.saveData.autoExit = value;
			}
		}
#if UNITY_EDITOR
		static string HOLY_BLENDER_PATH = Application.dataPath + "/../..";
#else
		static string HOLY_BLENDER_PATH = Application.dataPath + "/..";
#endif
		static string APP_PATH = HOLY_BLENDER_PATH + "/dist/BlenderPlugin/BlenderPlugin";

		public void PickBlenderPath ()
		{
			IList<ItemWithStream> items = StandaloneFileBrowser.OpenFilePanel("Pick blender executable", Environment.SystemDirectory, "", false);
			foreach (ItemWithStream item in items)
			{
				FileStream fileStream = (FileStream) item.OpenStream();
				blenderPathInputField.text = fileStream.Name;
			}
		}

		public void PickBlendFilePath ()
		{
			IList<ItemWithStream> items = StandaloneFileBrowser.OpenFilePanel("Pick .blend file", Environment.SystemDirectory, "blend", false);
			foreach (ItemWithStream item in items)
			{
				FileStream fileStream = (FileStream) item.OpenStream();
				blendFilePathInputField.text = fileStream.Name;
			}
		}

		public void StartApp ()
		{
			Process app = new Process();
			app.StartInfo.UseShellExecute = false;
			app.StartInfo.FileName = APP_PATH;
			app.StartInfo.Arguments = '"' + blenderPathInputField.text + "\" \"" + blendFilePathInputField.text + '"';
			app.StartInfo.RedirectStandardOutput = true;
			app.StartInfo.RedirectStandardError = true;
			app.StartInfo.WorkingDirectory = HOLY_BLENDER_PATH;
			app.Start();
			// string ouptut = app.StandardOutput.ReadToEnd();  
			// string errors = app.StandardError.ReadToEnd();  
	  		// app.WaitForExit();
			// print("Output: " + ouptut);
			// print("Errors: " + errors);
			// if (!string.IsNullOrEmpty(errors))
			// {
			// 	GameManager.instance.DisplayNotification ("Errors: " + errors);
			// 	return;
			// }
			if (AutoExit)
				GameManager.instance.Quit ();
		}
	}
}