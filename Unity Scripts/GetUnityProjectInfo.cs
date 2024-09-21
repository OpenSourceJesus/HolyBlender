using System;
using System.IO;
using UnityEngine;
using UnityEditor;
using UnityEditor.PackageManager;
using UnityEditor.PackageManager.Requests;
using Object = UnityEngine.Object;

public class GetUnityProjectInfo : MonoBehaviour
{
	public static void Do ()
	{
		string filePath = "/tmp/HolyBlender Data (BlenderToUnity)";
		string[] lines = File.ReadAllLines(filePath);
		string outputText = "";
		foreach (string line in lines)
			outputText += GetAssetsInfo(line, typeof(Object));
		outputText += GetAssetsInfoWithFileExtension(".fbx", typeof(Mesh));
		outputText += GetAssetsInfoWithFileExtension(".mat", typeof(Material));
		File.WriteAllText(filePath, outputText);
		AddPackage ("com.unity.mathematics");
		AddPackage ("com.unity.nuget.newtonsoft-json");
		AddPackage ("com.unity.shadergraph");
		AddPackage ("com.unity.test-framework");
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

	static string GetAssetsInfoWithFileExtension (string fileExtension, Type assetType)
	{
		string output = "";
		string[] args = Environment.GetCommandLineArgs();
		string[] filePaths = SystemExtensions.GetAllFilePathsInFolder(args[args.Length - 1], fileExtension);
		foreach (string filePath in filePaths)
			output += GetAssetsInfo(filePath, assetType);;
		return output;
	}

	static string GetAssetsInfo (string filePath, Type assetType)
	{
		string output = "";
		int indexOfAssets = filePath.IndexOf("Assets");
		if (indexOfAssets != -1)
		{
			string relativeFilePath = filePath.Substring(indexOfAssets);
			Object[] objects = AssetDatabase.LoadAllAssetsAtPath(relativeFilePath);
			foreach (Object obj in objects)
			{
				if (obj.GetType() == assetType)
				{
					string guid;
					long fileId;
					if (AssetDatabase.TryGetGUIDAndLocalFileIdentifier(obj, out guid, out fileId))
						output += '-' + filePath + ' ' + fileId + ' ' + guid;
				}
			}
		}
		return output;
	}
}