using System;
using System.IO;
using UnityEngine;
using UnityEditor;
using Object = UnityEngine.Object;

public class GetUnityProjectInfo : MonoBehaviour
{
	public static void Do ()
	{
		string[] args = Environment.GetCommandLineArgs();
		string outputText = "";
		string[] filePaths = SystemExtensions.GetAllFilePathsInFolder(args[args.Length - 1], ".fbx");
		foreach (string filePath in filePaths)
		{
			int indexOfAssets = filePath.IndexOf("Assets");
			string relativeFilePath = filePath.Substring(indexOfAssets);
			Object[] objects = AssetDatabase.LoadAllAssetsAtPath(relativeFilePath);
			foreach (Object obj in objects)
			{
				if (obj.GetType() == typeof(Mesh))
				{
					string guid;
					long fileId;
					if (AssetDatabase.TryGetGUIDAndLocalFileIdentifier(obj, out guid, out fileId))
						outputText += '-' + filePath + ' ' + fileId + ' ' + guid + '\n';
				}
			}
		}
		UnityEngine.Debug.Log(outputText);
		File.WriteAllText("/tmp/Unity2Many Data (BlenderToUnity)", outputText);
	}
}