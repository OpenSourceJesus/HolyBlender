using System;
using CSharpToPython;
using Microsoft.CodeAnalysis;
using System.Collections.Generic;
using Microsoft.CodeAnalysis.CSharp;

public class CSToPython : Translator 
{
	public static void Main (string[] args)
	{
		instance = new CSToPython();
		instance.Init (args);
		instance.Do ();
	}

	public override string ConvertFile (string path)
	{
		string inputFileContents = File.ReadAllText(path);
		string outputFilePath = GetNewOutputPath(path);
		SyntaxTree tree = CSharpSyntaxTree.ParseText(inputFileContents);
		ConvertSyntaxNode (tree.GetRoot(), 0);
		Directory.CreateDirectory(outputFolderPath);
		EngineWrapper engineWrapper = new EngineWrapper();
		object result = Program.ConvertAndRunCode(engineWrapper, inputFileContents);
		File.WriteAllText(outputFilePath, pythonFileContents);
		return outputFilePath;
	}

	public override string GetNewOutputPath (string path)
	{
		string output = outputFolderPath + path.Substring(path.LastIndexOf('/'));
		return output.Replace(".cs", ".py");
	}

	public override string PostProcessCode (string text)
	{
		return text;
	}

	public override string GetStaticFileName ()
	{
		return "Utils.cs";
	}

	public override string GetStaticFileContents ()
	{
		return "";
	}

	public override string ConvertSyntaxNode (SyntaxNode node, int outputLineIndex = -1, int outputCharIndex = -1, int indents = 0, bool parsedMainClass = false)
	{
		return "" + node;
	}
}