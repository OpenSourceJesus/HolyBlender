using System.IO;
using System.Collections.Generic;

public static class SystemExtensions
{
	public static string[] GetAllFilePathsInFolder (string folderPath, string fileExtension)
	{
		List<string> output = new List<string>();
		List<string> folderPathsRemaining = new List<string>(new string[] { folderPath });
		while (folderPathsRemaining.Count > 0)
		{
			string _folderPath = folderPathsRemaining[0];
			folderPathsRemaining.AddRange(Directory.GetDirectories(_folderPath));
			List<string> filePaths = new List<string>(Directory.GetFiles(_folderPath));
			for (int i = 0; i < filePaths.Count; i ++)
			{
				string filePath = filePaths[i];
				if (!filePath.EndsWith(fileExtension))
				{
					filePaths.RemoveAt(i);
					i --;
				}
			}
			output.AddRange(filePaths);
			folderPathsRemaining.RemoveAt(0);
		}
		return output.ToArray();
	}
}