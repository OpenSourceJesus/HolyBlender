using System;
using CSharpToPython;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

public class UnityInBlender : Translator 
{
	public static string outputFilePath;
	static Dictionary<string, List<string>> membersToAddDict = new Dictionary<string, List<string>>();
	static List<string> codeToSkip = new List<string>();

	public static void Main (string[] args)
	{
		instance = new UnityInBlender();
		instance.Init (args);
		instance.Do ();
		File.WriteAllText(outputFolderPath + '/' + instance.GetStaticFileName(), instance.GetStaticFileContents());
	}

	public virtual void Init (string[] args)
	{
		Translator.typeConversionsDict = typeConversionsDict;
		Translator.memberConversionsDict = memberConversionsDict;
		Translator.removeTexts = removeTexts;
		base.Init (args);
	}

	public override string ConvertFile (string path)
	{
		Console.WriteLine("File: " + path);
		string inputFileContents = File.ReadAllText(path);
		string outputFilePath = GetNewOutputPath(path);
		outputFilesPaths.Add(outputFilePath);
		EngineWrapper engineWrapper = new EngineWrapper();
		object result = Program.ConvertAndRunCode(engineWrapper, inputFileContents);
		File.WriteAllText(outputFilePath, pythonFileContents);
		return outputFilePath;
	}

	public override void PostProcessFiles ()
	{
		foreach (string outputFilePath in outputFilesPaths)
		{
			UnityInBlender.outputFilePath = outputFilePath;
			File.WriteAllText(outputFilePath, PostProcessCode(File.ReadAllText(outputFilePath)));
		}
	}

	public override string GetNewOutputPath (string path)
	{
		string output = outputFolderPath + path.Substring(path.LastIndexOf('/'));
		return output.Replace(".cs", ".py");
	}

	public override string GetStaticFileName ()
	{
		return STATIC_CLASS_NAME + ".py";
	}

	public override string GetStaticFileContents ()
	{
		return "";
	}

	public override string ConvertSyntaxNode (SyntaxNode node, int outputLineIndex = -1, int outputCharIndex = -1, int indents = 0, bool parsedMainClass = false)
	{
		string output = "" + node;
		if (node.IsKind(SyntaxKind.Block))
		{
			AddToMembersToAdd (output);
			indents ++;
			outputCharIndex = -1;
		}
		foreach (SyntaxNode childNode in node.ChildNodes())
			ConvertSyntaxNode (childNode, outputLineIndex, outputCharIndex, indents, parsedMainClass);
		if (node.IsKind(SyntaxKind.Block))
		{
			indents --;
			outputCharIndex = -1;
		}
		return output;
	}

	static void AddToMembersToAdd (string memberToAdd)
	{
		List<string> membersToAdd = new List<string>();
		if (membersToAddDict.TryGetValue(outputFilesPaths[outputFilesPaths.Count - 1], out membersToAdd))
		{
			membersToAdd.Add(memberToAdd);
			membersToAddDict[outputFilesPaths[outputFilesPaths.Count - 1]] = membersToAdd;
		}
		else
			membersToAddDict[outputFilesPaths[outputFilesPaths.Count - 1]] = new List<string>(new string[] { memberToAdd });
	}
}