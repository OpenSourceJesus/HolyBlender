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
		string outputPath = "/tmp/HolyBlender Data (BlenderToUnity)";
		string[] lines = File.ReadAllLines(outputPath);
		foreach (string line in lines)
		{
			string[] data = line.Split(", ");
			Quaternion rotation = Quaternion.Euler(float.Parse(data[1]), float.Parse(data[2]), float.Parse(data[3]));
			outputText += '\n' + data[0] + ", " + rotation.x + ", " + rotation.y + ", " + rotation.z + ", " + rotation.w;
		}
		File.WriteAllText(outputPath, outputText);
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