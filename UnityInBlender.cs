using System;
using CSharpToPython;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

public class UnityInBlender : Translator 
{
	// public new static Dictionary<string, string> typeConversionsDict = new Dictionary<string, string>() { { "Console.Write" , "printf" } };
	// public new static Dictionary<string, string> memberConversionsDict = new Dictionary<string, string>() { { "IndexOf", "Find"} };
	public static string outputFilePath;
	static string className;
	static Dictionary<string, List<string>> membersToAddDict = new Dictionary<string, List<string>>();
	static List<string> codeToSkip = new List<string>();
	const string REPLACE_INDICATOR = "ꗈ";

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
		string output = path.Substring(path.LastIndexOf('/') + 1);
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
		Console.WriteLine(node.ToString().Replace(DEBUG_INDICATOR, ""));
		Console.WriteLine("Type: " + node.Kind());
		string output = "" + node;
		if (node.IsKind(SyntaxKind.ClassDeclaration))
		{
			int indexOfClass = output.IndexOf(CLASS_INDICATOR);
			int classNameEndIndex = output.IndexOfAny(new char[] { '{', '\n' }, indexOfClass);
			int indexOfColon = output.LastIndexOf(':', classNameEndIndex);
			if (indexOfColon != -1)
				className = output.SubstringStartEnd(indexOfClass + CLASS_INDICATOR.Length, indexOfColon);
			else
				className = output.SubstringStartEnd(indexOfClass + CLASS_INDICATOR.Length, classNameEndIndex);
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.MethodDeclaration))
		{
			AddToMembersToAdd (output);
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.ParameterList))
		{
			AddToMembersToAdd (output);
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.ArgumentList) && !codeToSkip.Contains(output))
		{
			if (output.Length > 2)
			{
				SyntaxNode arrayCreationExpressionNode = GetSyntaxNodeOfKindInAllChildren(node, SyntaxKind.ArrayCreationExpression);
				if (arrayCreationExpressionNode != null)
					return output;
				string[] arguments = output.Split(", ");
				output = "";
				for (int i = 0; i < arguments.Length; i ++)
				{
					string argument = arguments[i];
					argument = ConvertNumberString(argument);
					argument = argument.Insert(1, TEMPORARY_INDICATOR);
					output += argument + ", ";
				}
				output = output.Remove(output.Length - 2);
			}
			outputLineIndex = Math.Clamp(outputLineIndex, 0, outputFileLines.Count - 1);
			AddToMembersToAdd (output);
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.ExpressionStatement))
		{
			AddToMembersToAdd (output);
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.LocalDeclarationStatement) || node.IsKind(SyntaxKind.FieldDeclaration)) //TODO: Handle multi-dimensional arrays
																												//TODO: Handle multi-dimensional lists
		{
			int indexOfLeftParenthesis = output.IndexOf('(');
			if (indexOfLeftParenthesis != -1 && !output.IsInChar(indexOfLeftParenthesis) && !output.IsInString(indexOfLeftParenthesis))
			{
				int indexOfMatchingParenthesis = output.IndexOfMatchingRightParenthesis(indexOfLeftParenthesis);
				string expression = output.SubstringStartEnd(indexOfLeftParenthesis, indexOfMatchingParenthesis + 1);
				SyntaxTree tree = CSharpSyntaxTree.ParseText(expression);
				ConvertSyntaxNode (tree.GetRoot(), outputLineIndex, outputCharIndex, indents, parsedMainClass);
				codeToSkip.Add("" + node);
			}
			AddToMembersToAdd (output);
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.Block))
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
			AddToMembersToAdd (output);
			outputCharIndex = -1;
		}
		return output;
	}

	public override string PostProcessCode (string text)
	{
		List<string> lines;
		if (membersToAddDict.TryGetValue(outputFilePath, out lines))
		{
			Console.WriteLine(DEBUG_INDICATOR + outputFilePath);
			for (int i = 0; i < lines.Count; i ++)
			{
				string line = lines[i];
				text += '\n' + line;
			}
		}
		return base.PostProcessCode(text);
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