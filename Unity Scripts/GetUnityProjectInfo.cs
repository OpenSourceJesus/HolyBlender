using System;
using System.IO;
using UnityEngine;
using UnityEditor;
using Object = UnityEngine.Object;

public class GetUnityProjectInfo : MonoBehaviour
{
	public static void Do ()
	{
		string outputText = "";
		outputText += GetAssetsInfo(".fbx", typeof(Mesh));
		outputText += GetAssetsInfo(".mat", typeof(Material));
		File.WriteAllText("/tmp/HolyBlender Data (BlenderToUnity)", outputText);
	}

	static string GetAssetsInfo (string fileExtension, Type assetType)
	{
		string output = "";
		string[] args = Environment.GetCommandLineArgs();
		string[] filePaths = SystemExtensions.GetAllFilePathsInFolder(args[args.Length - 1], fileExtension);
		foreach (string filePath in filePaths)
		{
			int indexOfAssets = filePath.IndexOf("Assets");
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