using System;
using System.Diagnostics;
using Microsoft.CodeAnalysis;
using System.Collections.Generic;
using Microsoft.CodeAnalysis.CSharp;

public class Unity2Many
{
	public static Unity2Many instance;
	public static Dictionary<string, string> typeConversionsDict = new Dictionary<string, string>();
	public static Dictionary<string, string> memberConversionsDict = new Dictionary<string, string>();
	public static string[] removeTexts = new string[] { TEMPORARY_INDICATOR };
	public static string startFromFilePath = "";
	public static bool resumeLastRun;
	public static string outputFolderPath;
	public static List<string> outputFileLines = new List<string>();
	public static List<string> inputFolderPaths = new List<string>();
	public static List<string> inputFilePaths = new List<string>();
	public static List<string> extensionMethodsClassPathAndMethodNames = new List<string>();
	public static List<string> methodNames = new List<string>();
	public static List<string> outputFilesPaths = new List<string>();
	public const string INCLUDE_FOLDER_INDICATOR = "includeFolder=";
	public const string INCLUDE_FILE_INDICATOR = "includeFile=";
	public const string RESUME_LAST_RUN_INDICATOR = "resume=";
	public const string OUTPUT_FOLDER_INDICATOR = "output=";
	public const string EXCLUDE_INDICATOR = "exclude=";
	public const string CLASS_INDICATOR = "class ";
	public const string STATIC_INDICATOR = "static ";
	public const string DICTIONARY_INDICATOR = "Dictionary";
	public const string WHILE_INDICATOR = "while (";
	public const string SAVE_FILE_NAME = "Save Data";
	public const string STATIC_CLASS_NAME = "Extensions";
	public const string TEMPORARY_INDICATOR = "🛕";
	public const string DEBUG_INDICATOR = "Debug: ";
	public static int lineAtLastRunEnd;
	public static List<string> excludeItemsPaths = new List<string>();
	static string inputFilePath;

	public virtual void Init (string[] args)
	{
		foreach (string arg in args)
		{
			if (arg.StartsWith(INCLUDE_FOLDER_INDICATOR))
				inputFolderPaths.Add(GetNewInputPath(arg.Substring(INCLUDE_FOLDER_INDICATOR.Length)));
			else if (arg.StartsWith(INCLUDE_FILE_INDICATOR))
				inputFilePaths.Add(GetNewInputPath(arg.Substring(INCLUDE_FILE_INDICATOR.Length)));
			else if (arg.StartsWith(RESUME_LAST_RUN_INDICATOR))
				resumeLastRun = bool.Parse(arg.Substring(RESUME_LAST_RUN_INDICATOR.Length));
			else if (arg.StartsWith(OUTPUT_FOLDER_INDICATOR))
				outputFolderPath = GetNewInputPath(arg.Substring(OUTPUT_FOLDER_INDICATOR.Length));
			else if (arg.StartsWith(EXCLUDE_INDICATOR))
				excludeItemsPaths.Add(GetNewInputPath(arg.Substring(EXCLUDE_INDICATOR.Length)));
		}
	}

	public virtual void Do ()
	{
		string saveFilePath = Environment.CurrentDirectory + '/' + SAVE_FILE_NAME;
		if (File.Exists(saveFilePath))
		{
			string[] savedLines = File.ReadAllLines(saveFilePath);
			startFromFilePath = savedLines[0];
			lineAtLastRunEnd = int.Parse(savedLines[1]);
		}
		for (int i = 0; i < inputFolderPaths.Count; i ++)
		{
			string inputFolderPath = inputFolderPaths[i];
			string[] inputFilePaths = SystemExtensions.GetAllFilePathsInFolder(inputFolderPath, ".cs");
			bool foundStartFile = !resumeLastRun || startFromFilePath == "";
			for (int i2 = 0; i2 < inputFilePaths.Length; i2 ++)
			{
				inputFilePath = inputFilePaths[i2];
				bool shouldConvertFile = true;
				foreach (string excludeItemPath in excludeItemsPaths)
				{
					if (inputFilePath.Contains(excludeItemPath))
					{
						shouldConvertFile = false;
						break;
					}
				}
				if (shouldConvertFile)
				{
					if (inputFilePath == startFromFilePath)
						foundStartFile = true;
					if (foundStartFile && !excludeItemsPaths.Contains(inputFilePath))
					{
						UpdateSaveFile ();
						ConvertFile (inputFilePath);
					}
				}
			}
		}
		foreach (string inputFilePath in inputFilePaths)
		{
			bool shouldConvertFile = true;
			foreach (string excludeItemPath in excludeItemsPaths)
			{
				Console.WriteLine("Exclude folder: " + excludeItemPath);
				if (inputFilePath.Contains(excludeItemPath))
				{
					shouldConvertFile = false;
					break;
				}
			}
			if (shouldConvertFile)
			{
				UpdateSaveFile ();
				ConvertFile (inputFilePath);
			}
		}
		PostProcessFiles ();
		File.WriteAllText(outputFolderPath + '/' + GetStaticFileName(), GetStaticFileContents());
	}

	public virtual string ConvertFile (string path)
	{
		Console.WriteLine("File: " + path);
		string inputFileContents = File.ReadAllText(path);
		if (resumeLastRun && lineAtLastRunEnd > 0)
		{
			int indexOfNewLine = -1;
			for (int i = 0; i < lineAtLastRunEnd; i ++)
				indexOfNewLine = inputFileContents.IndexOf('\n', indexOfNewLine + 1);
			inputFileContents = inputFileContents.Substring(indexOfNewLine);
		}
		string outputFilePath = GetNewOutputPath(path);
		outputFilesPaths.Add(outputFilePath);
		SyntaxTree tree = CSharpSyntaxTree.ParseText(inputFileContents);
		ConvertSyntaxNode (tree.GetRoot(), 0);
		Directory.CreateDirectory(outputFilePath.Remove(outputFilePath.LastIndexOf('/')));
		File.WriteAllLines(outputFilePath, outputFileLines.ToArray());
		outputFileLines.Clear();
		return outputFilePath;
	}

	public virtual void PostProcessFiles ()
	{
		foreach (string outputFilePath in outputFilesPaths)
			File.WriteAllText(outputFilePath, PostProcessCode(File.ReadAllText(outputFilePath)));
	}

	static void UpdateSaveFile ()
	{
		string saveFilePath = outputFolderPath + '/' + SAVE_FILE_NAME;
		string saveFileText = inputFilePath + "\n0";
		// File.WriteAllText(saveFilePath, saveFileText);
	}

	public virtual string GetNewOutputPath (string path)
	{
		throw new NotImplementedException();
	}

	public virtual string GetStaticFileName ()
	{
		throw new NotImplementedException();
	}

	public virtual string GetStaticFileContents ()
	{
		throw new NotImplementedException();
	}

	public virtual string ConvertSyntaxNode (SyntaxNode node, int outputLineIndex = -1, int outputCharIndex = -1, int indents = 0, bool parsedMainClass = false)
	{
		throw new NotImplementedException();
	}

	public static string InsertInOutputFileLines (string str, int lineIndex = -1, int charIndex = -1, int indents = 0)
	{
		if (lineIndex == -1)
			lineIndex = outputFileLines.Count;
		else
			lineIndex = Math.Clamp(lineIndex, 0, outputFileLines.Count);
		string[] lines = str.Split('\n');
		str = "";
		for (int i = 0; i < lines.Length; i ++)
		{
			string line = lines[i];
			if (charIndex == -1)
			{
				for (int i2 = 0; i2 < indents; i2 ++)
					line = "\t" + line;
				if (lineIndex == outputFileLines.Count)
					outputFileLines.Add(line);
				else
					outputFileLines.Insert(lineIndex + i, line);
			}
			else
			{
				if (outputFileLines.Count > 0)
					lineIndex = Math.Clamp(lineIndex, 0, outputFileLines.Count - 1);
				string lastOutputFileLine = outputFileLines[lineIndex];
				charIndex = Math.Clamp(charIndex, 0, lastOutputFileLine.Length);
				if (charIndex == outputFileLines.Count)
					outputFileLines[lineIndex] = lastOutputFileLine + line;
				else
					outputFileLines[lineIndex] = lastOutputFileLine.Insert(charIndex, line);
			}
			charIndex = -1;
			str += line + '\n';
		}
		return str;
	}

	public virtual string PostProcessCode (string text)
	{
		text = text.Replace("++", "+= 1.0");
		text = text.Replace("--", "-= 1.0");
		foreach (KeyValuePair<string, string> keyValuePair in typeConversionsDict)
			text = text.Replace(keyValuePair.Key, keyValuePair.Value);
		foreach (KeyValuePair<string, string> keyValuePair in memberConversionsDict)
			text = text.Replace('.' + keyValuePair.Key, '.' + keyValuePair.Value);
		foreach (string removeText in removeTexts)
			text = text.Replace(removeText, "");
		text = text.Replace(").0", ")");
		foreach (string extensionMethodClassPathAndMethodName in extensionMethodsClassPathAndMethodNames)
		{
			int indexOfMethodName = extensionMethodClassPathAndMethodName.LastIndexOf('.');
			string methodName = extensionMethodClassPathAndMethodName.Substring(indexOfMethodName);
			int indexOfMethodCall = -1;
			do
			{
				indexOfMethodCall = text.IndexOf(methodName, indexOfMethodCall + 1);
				if (indexOfMethodCall != -1)
				{
					int indexOfFirstArgument = text.LastIndexOfAny(new char[] { ' ', '\t', '\n', '(' }, indexOfMethodCall) + 1;
					string firstArgument = text.SubstringStartEnd(indexOfFirstArgument, indexOfMethodCall);
					text = text.Replace(firstArgument + methodName + '(', extensionMethodClassPathAndMethodName + '(' + firstArgument + ", ");
					indexOfMethodCall += indexOfMethodName + 2;
				}
			}
			while (indexOfMethodCall != -1);
		}
		int indexOfMultilineString = -1;
		do
		{
			indexOfMultilineString = text.IndexOf("@\"", indexOfMultilineString + 1);
			if (indexOfMultilineString != -1)
			{
				int indexOfNewLineBeforeMultilineString = text.LastIndexOf('\n', indexOfMultilineString);
				if (indexOfNewLineBeforeMultilineString != -1)
				{
					string textBeforeNewLineBeforeMultilineString = text.SubstringStartEnd(indexOfNewLineBeforeMultilineString + 1, indexOfMultilineString);
					int indents = textBeforeNewLineBeforeMultilineString.Length - textBeforeNewLineBeforeMultilineString.TrimStart('\t').Length;
					string multilineString = text.SubstringStartEnd(indexOfMultilineString, text.IndexOf('\"', indexOfMultilineString + 2));
					string[] stringLines = multilineString.Split('\n');
					string newMultilineString = "";
					for (int i = 0; i < stringLines.Length; i ++)
					{
						string stringLine = stringLines[i];
						if (i > 0)
						{
							indexOfMultilineString -= indents;
							if (indents >= stringLine.Length)
								continue;
							stringLine = stringLine.Substring(indents);
						}
						newMultilineString += stringLine + '\n';
					}
					newMultilineString = newMultilineString.Remove(newMultilineString.Length - 1);
					newMultilineString = newMultilineString.Replace("@", "\"\"");
					newMultilineString += "\"\"";
					text = text.Replace(multilineString, newMultilineString);
				}
			}
		} while (indexOfMultilineString != -1);
		return text;
	}

	public static SyntaxNode GetSyntaxNodeOfKindInParents (SyntaxNode node, SyntaxKind kind)
	{
		while (node.Parent != null)
		{
			node = node.Parent;
			if (node.IsKind(kind))
				return node;
		}
		return null;
	}

	public static SyntaxNode GetSyntaxNodeOfKindInAllChildren (SyntaxNode node, SyntaxKind kind)
	{
		List<SyntaxNode> nodesRemaining = new List<SyntaxNode>(new SyntaxNode[] { node });
		while (nodesRemaining.Count > 0)
		{
			node = nodesRemaining[0];
			if (node.IsKind(kind))
				return node;
			nodesRemaining.RemoveAt(0);
			nodesRemaining.AddRange(node.ChildNodes());
		}
		return null;
	}

	public static string ConvertNumberString (string str)
	{
		string output = str.TrimEnd('f');
		float f;
		if (!float.TryParse(output, out f))
			return str;
		if (!output.Contains('.'))
			output += ".0";
		return output;
	}

	static string GetNewInputPath (string path)
	{
		string output = path.Replace('\\', '/');
		if (output == ".")
			output = Environment.CurrentDirectory;
		else if (output.StartsWith("./"))
			output = Environment.CurrentDirectory + '/' + output.Substring(2);
		return output;
	}
}