using CSharpToPython;
using Microsoft.CodeAnalysis;
using System.Collections.Generic;
using Microsoft.CodeAnalysis.CSharp;
using SourceCodeKind = Microsoft.Scripting.SourceCodeKind;

public class UnityToUnreal : Translator 
{
	public new static Dictionary<string, string> typeConversionsDict = new Dictionary<string, string>() { { "Vector2" , "FVector2D" }, {"FFVector2DD" , "FVector2D"}, {"Transform" , "FTransform"}, {"FFTransform" , "FTransform"} };
	// public new static Dictionary<string, string> memberConversionsDict = new Dictionary<string, string>() { { "IndexOf", "Find"} };
	public static string pythonFileContents;
	public const string UNREAL_MODE_INDICATOR = "unreal=";
	public static List<string> mainClassNames = new List<string>();
	// static string BARE_UNREAL_PROJECT_PATH = "/UEBareDesktopMaxQual";
	static bool unrealMode;
	static string TEMPLATES_PATH = "Templates";
	static Stage stage;
	static string className;
	static int beginPlayMethodLine = -1;
	static Dictionary<string, List<string>> membersToAddDict = new Dictionary<string, List<string>>();
	static string[] METHOD_NAMES_EQUIVALENT_TO_BEGIN_PLAY = new string[] { "Awake", "Start", "OnEnable" };
	static string outputFilePath;
	static List<string> codeToSkip = new List<string>();
	static string mainClassName;
	const string REPLACE_INDICATOR = "ꗈ";
	const string PUBLIC_INDICATOR = "public ";
	const string PRIVATE_INDICATOR = "private ";
	const string PROTECTED_INDICATOR = "protected ";
	const string PUBLIC_HEADER_SECTION_INDICATOR = "public:";
	const string PRIVATE_HEADER_SECTION_INDICATOR = "private:";
	const string PROTECTED_HEADER_SECTION_INDICATOR = "protected:";
	const string BEGIN_PLAY_METHOD_INDICATOR = "::BeginPlay";

	public static void Main (string[] args)
	{
		instance = new UnityToUnreal();
		instance.Init (args);
		instance.Do ();
		File.WriteAllText(outputFolderPath + '/' + instance.GetStaticFileName(), instance.GetStaticFileContents());
		stage = Stage.Header;
	}

	public override void Init (string[] args)
	{
		foreach (string arg in args)
		{
			if (arg.StartsWith(UNREAL_MODE_INDICATOR))
				unrealMode = bool.Parse(arg.Substring(UNREAL_MODE_INDICATOR.Length));
		}
		if (unrealMode)
			typeConversionsDict.Add("List", "TArray");
		else
			typeConversionsDict.Add("List", "std::vector");
		Translator.typeConversionsDict = typeConversionsDict;
		Translator.typeConversionsDict = typeConversionsDict;
		Translator.memberConversionsDict = memberConversionsDict;
		Translator.removeTexts = removeTexts;
		// BARE_UNREAL_PROJECT_PATH = Environment.CurrentDirectory + BARE_UNREAL_PROJECT_PATH;
		base.Init (args);
		string[] filePaths = SystemExtensions.GetAllFilePathsInFolder(args[args.Length - 1], ".cs");
		foreach (string filePath in filePaths)
		{
			string mainClassName = filePath.Remove(filePath.LastIndexOf('.'));
			mainClassName = mainClassName.Substring(mainClassName.LastIndexOf('/') + 1);
			mainClassNames.Add(mainClassName);
		}
	}

	public override void Do ()
	{
		base.Do ();
		File.Copy(TEMPLATES_PATH + "/Utils.h", outputFolderPath + "/Utils.h", true);
		File.Copy(TEMPLATES_PATH + "/Utils.cpp", outputFolderPath + "/Utils.cpp", true);
		File.Copy(TEMPLATES_PATH + "/Prefab.h", outputFolderPath + "/Prefab.h", true);
		File.Copy(TEMPLATES_PATH + "/Prefab.cpp", outputFolderPath + "/Prefab.cpp", true);
	}

	public override string ConvertFile (string path)
	{
		stage = Stage.Header;
		string output = MakeHeader(path) + "\n";
		stage = Stage.Python;
		output += ConvertFileToPython(path);
		// stage = Stage.Cpp;
		// System.Diagnostics.Process process = new System.Diagnostics.Process();
		// System.Diagnostics.ProcessStartInfo startInfo = new System.Diagnostics.ProcessStartInfo();
		// startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
		// startInfo.FileName = "terminal";
		// startInfo.Arguments = "";
		// process.StartInfo = startInfo;
		// process.Start();
		return output;
	}

	string MakeHeader (string path)
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
		for (int i = 0; i < outputFileLines.Count; i ++)
		{
			string line = outputFileLines[i];
			if (line == "};")
			{
				outputFileLines.RemoveAt(i);
				break;
			}
		}
		outputFileLines.Add("};");
		File.WriteAllLines(outputFilePath, outputFileLines.ToArray());
		outputFileLines.Clear();
		return outputFilePath;
	}

	string ConvertFileToPython (string path)
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
			UnityToUnreal.outputFilePath = outputFilePath;
			File.WriteAllText(outputFilePath, PostProcessCode(File.ReadAllText(outputFilePath)));
		}
	}

	public override string GetNewOutputPath (string path)
	{
		Console.WriteLine(DEBUG_INDICATOR + '1' + path);
		Console.WriteLine(DEBUG_INDICATOR + '2' + outputFolderPath);
		string output = outputFolderPath + path.Substring(path.LastIndexOf('/'));
		// string intersection = path.GetIntersection(outputFolderPath, 0, path.Length);
		// if (intersection != "")
		// 	path = path.Substring(intersection.Length);
		// output += '/' + path;
		Console.WriteLine(DEBUG_INDICATOR + output);
		if (stage == Stage.Header)
			return output.Replace(".cs", ".h");
		else if (stage == Stage.Python)
			return output.Replace(".cs", ".py");
		else if (stage == Stage.Cpp)
			return output.Replace(".cs", ".cpp");
		else
			return output;
	}

	public override string GetStaticFileName ()
	{
		if (stage == Stage.Header)
			return STATIC_CLASS_NAME + ".h";
		else if (stage == Stage.Python)
			return STATIC_CLASS_NAME + ".py";
		else
			return STATIC_CLASS_NAME + ".cpp";
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
			string baseClassAndInterfacesNames = ""; //TODO: Convert to the matching Unreal class name if one exists
			bool isMainClass = mainClassName == null;
			if (indexOfColon != -1)
			{
				className = output.SubstringStartEnd(indexOfClass + CLASS_INDICATOR.Length, indexOfColon);
				className = className.TrimEnd();
				if (isMainClass)
					mainClassName = className;
				baseClassAndInterfacesNames = output.SubstringStartEnd(indexOfColon + 1, classNameEndIndex);
			}
			else
			{
				className = output.SubstringStartEnd(indexOfClass + CLASS_INDICATOR.Length, classNameEndIndex);
				if (isMainClass)
					mainClassName = className;
			}
			if (unrealMode)
			{
				if (isMainClass)
				{
					className = 'A' + className;
					string templateExtension;
					if (stage == Stage.Header)
						templateExtension = ".h";
					else
						templateExtension = ".cpp";
					string[] fileLines = File.ReadAllLines(TEMPLATES_PATH + "/Actor" + templateExtension);
					output = string.Join("\n", fileLines);
					output = output.Replace(REPLACE_INDICATOR + '0', className.Substring(1));
					output = output.Replace(REPLACE_INDICATOR + '1', className);
					InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
					outputLineIndex += fileLines.Length;
				}
			}
			else
			{
				if (isMainClass)
				{
					output = "#include <vector>\n\nclass " + className + "\n{";
					InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
					outputLineIndex += 5;
				}
			}
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.MethodDeclaration))
		{
			string methodName = GetMethodName(output);
			if (stage == Stage.Header)
			{
				if (unrealMode && (METHOD_NAMES_EQUIVALENT_TO_BEGIN_PLAY.Contains(methodName) || methodName == "Update"))
					return "";
				int indexOfNewLine = output.IndexOf('\n');
				if (indexOfNewLine != -1)
					output = output.Remove(indexOfNewLine);
				output = '\t' + output + ';';
				if (unrealMode)
				{
					if (output.Contains(PUBLIC_INDICATOR))
						InsertInOutputFileLines (PUBLIC_HEADER_SECTION_INDICATOR);
					else if (output.Contains(PROTECTED_INDICATOR))
						InsertInOutputFileLines (PROTECTED_HEADER_SECTION_INDICATOR);
					else
						InsertInOutputFileLines (PRIVATE_HEADER_SECTION_INDICATOR);
					outputLineIndex ++;
				}
				InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
				outputLineIndex ++;
				outputCharIndex = -1;
			}
			else
			{
				if (METHOD_NAMES_EQUIVALENT_TO_BEGIN_PLAY.Contains(methodName))
				{
					for (int i = 0; i < outputFileLines.Count; i ++)
					{
						string fileLine = outputFileLines[i];
						if (fileLine.Contains(BEGIN_PLAY_METHOD_INDICATOR))
						{
							beginPlayMethodLine = i;
							break;
						}
					}
					outputLineIndex = beginPlayMethodLine + 2;
					outputCharIndex = -1;
					indents ++;
				}
				else
				{
					int indexOfLeftParenthesis = output.IndexOf('(');
					if (indexOfLeftParenthesis != -1)	
						output = output.Remove(indexOfLeftParenthesis);
					int indexOfMethodName = output.IndexOf(methodName);
					output = output.Insert(indexOfMethodName, className + "::");
					AddToMembersToAdd (output);
					outputCharIndex = output.Length;
				}
			}
		}
		else if (node.IsKind(SyntaxKind.ParameterList) && stage != Stage.Header)
		{
			if (!IsNodeInEquivalentMethodToBeginPlay(node))
			{
				AddToMembersToAdd (output);
				outputLineIndex ++;
			}
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.ArgumentList) && stage != Stage.Header && !codeToSkip.Contains(output))
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
			if (!IsNodeInEquivalentMethodToBeginPlay(node))
				AddToMembersToAdd (output);
			else
				InsertInOutputFileLines (output, outputLineIndex, outputFileLines[outputLineIndex].Length, indents);
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.ExpressionStatement) && stage != Stage.Header)
		{
			int indexOfLeftParenthesis = output.IndexOf('(');
			if (indexOfLeftParenthesis != -1)
				output = output.Remove(indexOfLeftParenthesis);
			if (!IsNodeInEquivalentMethodToBeginPlay(node))
				AddToMembersToAdd (output);
			else
				InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			outputCharIndex = output.Length;
		}
		else if (node.IsKind(SyntaxKind.LocalDeclarationStatement) || node.IsKind(SyntaxKind.FieldDeclaration)) //TODO: Handle multi-dimensional arrays
																												//TODO: Handle multi-dimensional lists
		{
			if (stage == Stage.Header && node.IsKind(SyntaxKind.FieldDeclaration))
			{
				int indexOfEquals = output.IndexOf('=');
				if (indexOfEquals != -1)
					output = output.Remove(indexOfEquals) + ';';
				output = output.Replace(PUBLIC_INDICATOR, PUBLIC_HEADER_SECTION_INDICATOR + "\n\t");
			}
			foreach (string mainClassName in mainClassNames)
			{
				if (mainClassName.Length > 0)
				{
					int indexOfMainClassName = -1;
					do
					{
						indexOfMainClassName = output.IndexOf(mainClassName, indexOfMainClassName + 1);
						if (indexOfMainClassName != -1 && !output.IsInChar(indexOfMainClassName) && !output.IsInString(indexOfMainClassName))
						{
							output = output.Insert(indexOfMainClassName, "A");
							InsertInOutputFileLines ("#include \"" + mainClassName + ".h\"", 0);
							indexOfMainClassName ++;
						}
					} while (indexOfMainClassName != -1);
				}
			}
			int indexOfLeftParenthesis = output.IndexOf('(');
			if (indexOfLeftParenthesis != -1 && !output.IsInChar(indexOfLeftParenthesis) && !output.IsInString(indexOfLeftParenthesis))
			{
				int indexOfMatchingParenthesis = output.GetIndexOfMatchingRightParenthesis(indexOfLeftParenthesis);
				string expression = output.SubstringStartEnd(indexOfLeftParenthesis, indexOfMatchingParenthesis + 1);
				SyntaxTree tree = CSharpSyntaxTree.ParseText(expression);
				ConvertSyntaxNode (tree.GetRoot(), outputLineIndex, outputCharIndex, indents, parsedMainClass);
				codeToSkip.Add("" + node);
			}
			if (!IsNodeInEquivalentMethodToBeginPlay(node) && stage != Stage.Header)
				AddToMembersToAdd (output);
			else
				InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.Block) && stage != Stage.Header)
		{
			if (!IsNodeInEquivalentMethodToBeginPlay(node))
			{
				AddToMembersToAdd (output);
				indents ++;
			}
			outputCharIndex = -1;
		}
		foreach (SyntaxNode childNode in node.ChildNodes())
			ConvertSyntaxNode (childNode, outputLineIndex, outputCharIndex, indents, parsedMainClass);
		if (node.IsKind(SyntaxKind.Block) && stage != Stage.Header)
		{
			if (!IsNodeInEquivalentMethodToBeginPlay(node))
			{
				indents --;
				AddToMembersToAdd (output);
			}
			outputCharIndex = -1;
		}
		return output;
	}

	public override string PostProcessCode (string text)
	{
		List<string> lines;
		if (membersToAddDict.TryGetValue(outputFilePath, out lines))
		{
			text = text.Remove(text.Length - 3);
			for (int i = 0; i < lines.Count; i ++)
			{
				string line = lines[i];
				text += '\n' + line;
			}
			text += "};";
			Console.WriteLine(DEBUG_INDICATOR + text);
		}
		return base.PostProcessCode(text);
	}

	static string GetMethodName (string str)
	{
		int indexOfLeftParenthesis = str.IndexOf('(');
		int indexOfSpace = str.LastIndexOf(' ', indexOfLeftParenthesis - 2);
		return str.SubstringStartEnd(indexOfSpace + 1, indexOfLeftParenthesis - 1);
	}

	static bool IsNodeInEquivalentMethodToBeginPlay (SyntaxNode node)
	{
		SyntaxNode methodNode = GetSyntaxNodeOfKindInParents(node, SyntaxKind.MethodDeclaration);
		if (methodNode != null)
		{
			string methodNodeText = "" + methodNode;
			string methodName = GetMethodName(methodNodeText);
			if (METHOD_NAMES_EQUIVALENT_TO_BEGIN_PLAY.Contains(methodName))
				return true;
		}
		return false;
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

	enum Stage
	{
		Header,
		Python,
		Cpp,
		Unreal
	}
}