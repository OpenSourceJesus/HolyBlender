using System;
using System.IO;
using UnityEngine;
using UnityEditor;
using UnityEditor.PackageManager;
using UnityEditor.PackageManager.Requests;
using Object = UnityEngine.Object;

public class GetUnityProjectInfo : MonoBehaviour
{
	static string projectPath;

	public static void Do ()
	{
		AddPackage ("com.unity.mathematics");
		AddPackage ("com.unity.nuget.newtonsoft-json");
		AddPackage ("com.unity.shadergraph");
		AddPackage ("com.unity.test-framework");
		AddPackage ("com.unity.inputsystem");
		AddPackage ("com.unity.2d.tilemap");
		string[] args = Environment.GetCommandLineArgs();
		projectPath = args[args.Length - 1];
		string projectSettingsPath = projectPath + "/ProjectSettings/ProjectSettings.asset";
		string[] fileLines = File.ReadAllLines(projectSettingsPath);
		for (int i = 0; i < fileLines.Length; i ++)
		{
			string fileLine = fileLines[i];
			string inputModeIndicator = "activeInputHandler: ";
			if (fileLine.StartsWith(inputModeIndicator))
				fileLines[i] = inputModeIndicator + '2';
		}
		File.WriteAllLines(projectSettingsPath, fileLines);
		string tagManagerPath = projectPath + "/ProjectSettings/TagManager.asset";
		fileLines = File.ReadAllLines(tagManagerPath);
		bool foundThirdLayer = false;
		byte layer = 3;
		for (int i = 0; i < fileLines.Length; i ++)
		{
			string line = fileLines[i];
			if (line == "  - ")
			{
				foundThirdLayer = true;
				fileLines[i] += "" + layer;
			}
			if (foundThirdLayer)
				layer ++;
		}
		File.WriteAllLines(tagManagerPath, fileLines);
		string outputPath = "/tmp/HolyBlender Data (BlenderToUnity)";
		fileLines = File.ReadAllLines(outputPath);
		for (int i = 0; i < 32; i ++)
		{
			for (int i2 = 0; i2 < 32; i2 ++)
			{
				string fileLine = fileLines[i + i2 * 32];
				Physics2D.IgnoreLayerCollision(i, i2, fileLine != "True");
			}
		}
		string outputText = "";
		outputText += GetAssetsInfo(".glb", typeof(Mesh));
		outputText += GetAssetsInfo(".mat", typeof(Material));
		File.WriteAllText(outputPath, outputText);
	}

	static void AddPackage (string name)
	{
		AddRequest addRequest = Client.Add(name);
		while (!addRequest.IsCompleted)
		{
		}
		if (addRequest.Error == null)
			print("Package " + name + " added");
		else
			print(addRequest.Error);
	}

	static string GetAssetsInfo (string fileExtension, Type assetType)
	{
		string output = "";
		string[] filePaths = SystemExtensions.GetAllFilePathsInFolder(projectPath, fileExtension);
		foreach (string filePath in filePaths)
		{
			int indexOfAssets = filePath.IndexOf("Assets");
			if (indexOfAssets != -1)
			{
				string relativeFilePath = filePath.Substring(indexOfAssets);
				Object[] objects = AssetDatabase.LoadAllAssetsAtPath(relativeFilePath);
				foreach (Object obj in objects)
				{
					if (obj != null)
					{
						Type objType = obj.GetType();
						if (objType == assetType || objType.IsSubclassOf(assetType))
						{
							string guid;
							long fileId;
							if (AssetDatabase.TryGetGUIDAndLocalFileIdentifier(obj, out guid, out fileId))
								output += '-' + filePath + ' ' + fileId + ' ' + guid;
						}
					}
				}
			}
		}
		return output;
	}
}