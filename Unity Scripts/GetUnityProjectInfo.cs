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
		string outputText = "";
		outputText += GetAssetsInfo(".glb", typeof(Mesh));
		outputText += GetAssetsInfo(".mat", typeof(Material));
		File.WriteAllText("/tmp/HolyBlender Data (BlenderToUnity)", outputText);
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

	static string GetAssetsInfo (string fileExtension, Type assetType)
	{
		string output = "";
		string[] args = Environment.GetCommandLineArgs();
		string[] filePaths = SystemExtensions.GetAllFilePathsInFolder(args[args.Length - 1], fileExtension);
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