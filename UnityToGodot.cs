using CSharpToPython;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

public class UnityToGodot : Translator
{
	public new static Dictionary<string, string> typeConversionsDict = new Dictionary<string, string>() { { "string", "String" }, { "char", "String" }, { "double", "float" }, { "decimal", "float" }, { "File.ReadAllText", STATIC_CLASS_NAME + ".ReadFileText" }, { "File.WriteAllLines", STATIC_CLASS_NAME + ".WriteFileLines" }, { "File.WriteAllText", STATIC_CLASS_NAME + ".WriteFileText" }, { "Console.WriteLine", "print" }, { "Console.Write", "printraw" }, { "Math.Min", "min" }, { "Mathf.Min", "min" }, { "Math.Max", "max" }, { "Mathf.Max", "max" }, { "Math.Clamp", "clamp" }, { "Mathf.Clamp", "clamp" }, { "Mathf.Infinity", "INF" }, { "Mathf.NegativeInfinity", "-INF" }, { "base", "super" } };
	public new static Dictionary<string, string> memberConversionsDict = new Dictionary<string, string>() { { "SubString(", "substr(" }, { "AddRange", "append_array" }, { "Add", "append" }, { "RemoveAt", "remove_at" }, { "Remove(", "erase(" }, { "Insert", "insert" }, { "Count", "size()" }, { "Length", "size()" }, { "IndexOf", "find" }, { "Replace", "replace" }, { "EndsWith", "ends_with" }, { "StartsWith", "begins_with" }, { "Clear", "clear" }, { "Split", "split" }, { "LastIndexOf", "rfind" } };
	public new static string[] removeTexts = new string[] { TEMPORARY_INDICATOR, ".ToArray()" };
	public static string pythonFileContents;
	static string[] METHOD_NAMES_EQUIVALENT_TO_READY = new string[] { "Awake", "Start", "OnEnable" };
	static List<string> addToReadyMethodContents = new List<string>();
	static int readyMethodLine = -1;
	static int unusedVariableNameCount;
	static string classPath;
	const string KEY_VALUE_PAIR_INDICATOR = "KeyValuePair";
	const string CONSTANT_INDICATOR = "const ";
	const string THIS_INDICATOR = "this";
	const string UNUSED_VARIABLE_NAME = "ꗈ";
	const string READY_METHOD_INDICATOR = "_ready";

	public static void Main (string[] args)
	{
		UnityToGodot instance = new UnityToGodot();
		instance.Init (args);
		instance.Do ();
	}

	public override void Init (string[] args)
	{
		Translator.typeConversionsDict = typeConversionsDict;
		Translator.memberConversionsDict = memberConversionsDict;
		Translator.removeTexts = removeTexts;
		base.Init (args);
	}

	public override string GetNewOutputPath (string path)
	{
		string output = outputFolderPath;
		string intersection = path.GetIntersection(outputFolderPath, 0, path.Length);
		if (intersection != "")
			path = path.Replace(intersection, "");
		output += '/' + path;
		int lastIndexOfCurrentFolderPath = output.LastIndexOf(Environment.CurrentDirectory);
		int indexOfCurrentFolderPath = output.IndexOf(Environment.CurrentDirectory);
		if (indexOfCurrentFolderPath != lastIndexOfCurrentFolderPath)
			output = output.Remove(lastIndexOfCurrentFolderPath, Environment.CurrentDirectory.Length);
		return output.Replace(".cs", ".gd");
	}

	public override string GetStaticFileName ()
	{
		return STATIC_CLASS_NAME + ".gd";
	}

	public override string GetStaticFileContents ()
	{
		return "class_name " + STATIC_CLASS_NAME + @"

static func ReadFileText (path : String):
	var file = FileAccess.open(path, FileAccess.READ)
	var content = file.get_as_text()
	return content

static func WriteFileText (path : String, text : String):
	var file = FileAccess.open(path, FileAccess.WRITE)
	file.store_string(text)

static func WriteFileLines (path : String, lines : Array[String]):
	var file = FileAccess.open(path, FileAccess.WRITE)
	for line in lines:
		file.store_line(line)

static func LastIndexOfAny (str : String, findStrings : Array[String]):
	var output = -1
	for findStr in findStrings:
		output = maxi(str.find(findStr), output)
	return output

class KeyValuePair:
	var key
	var value

	func New (key, value):
		var output = KeyValuePair.new()
		output.key = key
		output.value = value
		return output";
	}

	public override string PostProcessCode (string text)
	{
		return base.PostProcessCode(text.Replace("//", "#"));
	}

	public override string ConvertSyntaxNode (SyntaxNode node, int outputLineIndex = -1, int outputCharIndex = -1, int indents = 0, bool parsedMainClass = false)
	{
		Console.WriteLine(node);
		Console.WriteLine("Type: " + node.Kind());
		string output = "" + node;
		//if (node.IsKind(SyntaxKind.NamespaceDeclaration))
		//{
		//	int indexOfNamespaceNameEnd = output.IndexOfAny([ '{', '\n' ]);
		//	output = output.Remove(indexOfNamespaceNameEnd);
		//	InsertInOutputFileLines (output, outputLineIndex, outputLineIndex, outputCharIndex, indents);
		//}
		if (node.IsKind(SyntaxKind.ClassDeclaration)) //TODO: Handle interfaces
		{
			int indexOfClass = output.IndexOf(CLASS_INDICATOR);
			int classNameEndIndex = output.IndexOfAny(new char[] { '{', '\n' }, indexOfClass);
			int indexOfColon = output.LastIndexOf(':', classNameEndIndex);
			string className;
			string baseClassAndInterfacesNames = ""; //TODO: Convert to the matching Godot class name if one exists
			if (indexOfColon != -1)
			{
				className = output.SubstringStartEnd(indexOfClass + CLASS_INDICATOR.Length, indexOfColon);
				baseClassAndInterfacesNames = output.SubstringStartEnd(indexOfColon + 1, classNameEndIndex);
			}
			else
				className = output.SubstringStartEnd(indexOfClass + CLASS_INDICATOR.Length, classNameEndIndex);
			bool wasClassPathEmpty = classPath == "";
			classPath += className + '.';
			if (wasClassPathEmpty)
				classPath = classPath.Replace(".", "") + '.';
			if (parsedMainClass)
			{
				output = CLASS_INDICATOR + className;
				if (indexOfColon != -1)
					output += " extends " + baseClassAndInterfacesNames;
				output += ':';
			}
			else
			{
				if (indexOfColon != -1)
					InsertInOutputFileLines ("extends " + baseClassAndInterfacesNames, outputLineIndex, outputCharIndex, indents);
				else
					InsertInOutputFileLines ("extends Node", outputLineIndex, outputCharIndex, indents);
				outputLineIndex ++;
				outputCharIndex = -1;
				output = "class_name " + className;
			}
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			outputLineIndex ++;
			outputCharIndex = -1;
			if (parsedMainClass)
				indents ++;
			parsedMainClass = true;
		}
		else if (node.IsKind(SyntaxKind.MethodDeclaration))
		{
			string methodName = GetMethodName(ref output);
			int indexOfMethodName = output.IndexOf(methodName);
			int indexOfMethodContents = output.IndexOf('{', indexOfMethodName);
			string methodContents = output.SubstringStartEnd(indexOfMethodContents + 1, output.LastIndexOf('}'));
			if (METHOD_NAMES_EQUIVALENT_TO_READY.Contains(methodName))
			{
				output = output.Replace(methodName, READY_METHOD_INDICATOR);
				methodName = READY_METHOD_INDICATOR;
				if (readyMethodLine == -1)
				{
					for (int i = 0; i < outputFileLines.Count; i ++)
					{
						string outputFileLine = outputFileLines[i];
						if (outputFileLine.Contains(READY_METHOD_INDICATOR))
						{
							readyMethodLine = i;
							break;
						}
					}
					if (readyMethodLine == -1)
						readyMethodLine = outputLineIndex;
				}
				outputLineIndex = readyMethodLine + 1;
				for (int i = 0; i < addToReadyMethodContents.Count; i ++)
				{
					string line = addToReadyMethodContents[i];
					InsertInOutputFileLines (line, outputLineIndex, outputCharIndex, indents);
					outputLineIndex ++;
				}
				addToReadyMethodContents.Clear();
			}
			else
			{
				while (methodNames.Contains(methodName))
				{
					output = output.Insert(indexOfMethodName + methodName.Length, UNUSED_VARIABLE_NAME);
					methodName += UNUSED_VARIABLE_NAME;
				}
			}
			int indexOfType = output.LastIndexOf(' ', indexOfMethodName - 2) + 1;
			output = output.RemoveStartEnd(indexOfType, indexOfMethodName);
			methodNames.Add(methodName);
			int indexOfNewLine = output.IndexOf('\n');
			if (indexOfNewLine != -1)
				output = output.Remove(indexOfNewLine);
			output = "func " + output.Remove(output.LastIndexOf('('));
			output = output.Replace("func static ", "static func ");
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			if (methodContents.Trim() == "")
			{
				indents ++;
				outputLineIndex ++;
				outputCharIndex = -1;
				InsertInOutputFileLines ("pass", outputLineIndex, outputCharIndex, indents);
				indents --;
				outputLineIndex --;
				outputCharIndex = outputFileLines[outputLineIndex].Length;
			}
			else
				outputCharIndex = outputFileLines[outputFileLines.Count - 1].Length;
		}
		else if (node.IsKind(SyntaxKind.ParameterList))
		{
			if (output.Length > 2)
			{
				string[] parameters = output.Substring(1, output.Length - 2).Split(", ");
				output = "(";
				for (int i = 0; i < parameters.Length; i ++)
				{
					string parameter = parameters[i];
					int indexOfSpace = parameter.IndexOf(' ');
					if (indexOfSpace == -1)
						continue;
					string parameterType = parameter.Remove(indexOfSpace);
					if (i == 0)
					{
						if (parameter.Remove(indexOfSpace) == THIS_INDICATOR)
						{
							SyntaxNode methodNode = GetSyntaxNodeOfKindInParents(node, SyntaxKind.MethodDeclaration);
							if (methodNode != null)
							{
								string methodText = "" + methodNode;
								string extensionMethodClassPathAndMethodName = classPath + GetMethodName(ref methodText);
								if (!extensionMethodsClassPathAndMethodNames.Contains(extensionMethodClassPathAndMethodName))
									extensionMethodsClassPathAndMethodNames.Add(extensionMethodClassPathAndMethodName);
							}
							parameter = parameter.Substring(THIS_INDICATOR.Length + 1);
							indexOfSpace = parameter.IndexOf(' ');
							if (indexOfSpace != -1)
								parameterType = parameter.Remove(indexOfSpace);
						}
					}
					int indexOfLeftSquareBrace = parameterType.IndexOf('[');
					if (indexOfLeftSquareBrace != -1)
						parameterType = "Array[" + parameterType.Remove(indexOfLeftSquareBrace) + "]";
					int indexOfEquals = parameter.IndexOf('=');
					if (indexOfEquals != -1)
					{
						string[] clauses = parameter.Split(' ');
						output += clauses[1] + " : " + parameterType + " = " + parameter.Substring(parameter.IndexOf(clauses[3]));
					}
					else
						output += parameter.Substring(indexOfSpace + 1) + " : " + parameterType;
					if (i < parameters.Length - 1)
						output += ", ";
				}
				output += ')';
			}
			output += ':';
			InsertInOutputFileLines (output, outputLineIndex, outputFileLines[outputFileLines.Count - 1].Length, indents);
			outputLineIndex ++;
			outputCharIndex = -1;
			indents ++;
		}
		else if (node.IsKind(SyntaxKind.ArgumentList))
		{
			if (output.Length > 2)
			{
				string[] arguments = output.Split(", ");
				output = "";
				for (int i = 0; i < arguments.Length; i ++)
				{
					string argument = arguments[i];
					argument = ConvertNumberString(argument);
					argument = argument.Insert(argument.Length - 1, TEMPORARY_INDICATOR);
					output += argument + ", ";
				}
				output = output.Remove(output.Length - 2);
			}
			InsertInOutputFileLines (output, outputLineIndex, outputFileLines[outputFileLines.Count - 1].Length, indents);
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.ExpressionStatement))
		{
			int indexOfLeftParenthesis = output.IndexOf('(');
			if (indexOfLeftParenthesis != -1)
				output = output.Remove(indexOfLeftParenthesis);
			int indexOfPeriod = output.IndexOf('.');
			if (indexOfPeriod != -1)
			{
				bool shouldInsertTemporaryIndicator = true;
				foreach (KeyValuePair<string, string> keyValuePair in typeConversionsDict)
				{
					if (keyValuePair.Key.StartsWith(output.Remove(indexOfPeriod)))
					{
						shouldInsertTemporaryIndicator = false;
						break;
					}
				}
				if (shouldInsertTemporaryIndicator)
					output = output.Insert(1, TEMPORARY_INDICATOR);
			}
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
		}
		else if (node.IsKind(SyntaxKind.ForStatement))
		{
			int indexOfNewLine = output.IndexOf('\n');
			if (indexOfNewLine != -1)
				output = output.Remove(indexOfNewLine);
			output = output.Remove(output.LastIndexOf(')'));
			output = "for " + output.Substring(output.IndexOf('(') + 1);
			string variableType = "";
			string variableName = "";
			string startValue;
			string endValue;
			string _operator;
			string increment = "";
			string inequality;
			string[] forClauses = output.Split("; ");
			string[] forClauseWords = forClauses[0].Split(' ', StringSplitOptions.RemoveEmptyEntries);
			if (forClauseWords.Length == 1)
				startValue = "0";
			else
			{
				int addToForClauseWordIndex = 0;
				if (forClauseWords.Length < 5)
					addToForClauseWordIndex = -1;
				else
					variableType = forClauseWords[1];
				variableName = forClauseWords[2 + addToForClauseWordIndex].Insert(1, TEMPORARY_INDICATOR);
				startValue = forClauseWords[4 + addToForClauseWordIndex];
			}
			forClauseWords = forClauses[1].Split(' ', StringSplitOptions.RemoveEmptyEntries);
			if (forClauseWords.Length == 0)
			{
				endValue = "INF";
				inequality = "<";
			}
			else
			{
				endValue = forClauseWords[2];
				inequality = forClauseWords[1];
			}
			forClauseWords = forClauses[2].Split(' ', StringSplitOptions.RemoveEmptyEntries);
			if (forClauseWords.Length > 2)
			{
				increment = forClauseWords[2];
				_operator = forClauseWords[1];
			}
			else if (forClauseWords.Length > 1)
				_operator = forClauseWords[1];
			else
			{
				_operator = forClauseWords[0];
				int indexOfOperator = _operator.LastIndexOfAny(new char[] {  '+', '-' });
				if (indexOfOperator != -1)
				{
					increment = _operator.Remove(indexOfOperator);
					_operator = _operator.Substring(indexOfOperator);
				}
			}
			if (_operator == "++")
				increment = "1";
			else if (_operator == "--")
				increment = "-1";
			else if (_operator.StartsWith("+="))
				increment = _operator.Substring(2);
			else if (_operator.StartsWith("-="))
				increment = "-" + _operator.Substring(2);
			if (variableType == "int")
			{
				if (inequality == "<=")
					endValue += " + 1";
				else if (inequality == ">=")
					endValue += " - 1";
				int indexOfRightParenthesis = output.IndexOf(inequality) + inequality.Length;
				string suffix = output.Substring(indexOfRightParenthesis + 1);
				output = "for " + variableName + " in range(" + startValue + ", " + endValue + ", " + increment + "):";
				if (suffix.Length > 0 && !suffix.IsInNumber(0))
					output += suffix;
			}
			else if (variableType == "float" || variableType == "double" || variableType == "decimal")
			{
				startValue = ConvertNumberString(startValue);
				endValue = endValue.TrimEnd(';');
				endValue = ConvertNumberString(endValue);
				increment = ConvertNumberString(increment);
				output = "var " + variableName + " = " + startValue;
				InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
				outputLineIndex ++;
				output = "while " + variableName + ' ' + inequality + ' ' + endValue + ':';
				InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
				output = variableName + " " + _operator + " " + increment;
				indents ++;
				outputLineIndex ++;
			}
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			outputLineIndex ++;
			outputCharIndex = -1;
			if (variableType == "int")
				indents ++;
		}
		else if (node.IsKind(SyntaxKind.ForEachStatement))
		{
			int indexOfNewLine = output.IndexOf('\n');
			if (indexOfNewLine != -1)
				output = output.Remove(indexOfNewLine);
			int indexOfInClause = output.IndexOf(" in ");
			string startFromInClause = output.Substring(indexOfInClause);
			int indexOfVariableName = output.LastIndexOf(' ', indexOfInClause - 1);
			output = "for" + output.SubstringStartEnd(indexOfVariableName, indexOfInClause) + startFromInClause;
			output = output.Remove(output.LastIndexOf(')')) + ':';
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			indents ++;
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.WhileStatement))
		{
			int indexOfNewLine = output.IndexOf('\n');
			if (indexOfNewLine != -1)
				output = output.Remove(indexOfNewLine);
			int indexOfLeftParenthesis = output.IndexOf('(');
			int indexOfMatchingParenthesis = output.GetIndexOfMatchingParenthesis(indexOfLeftParenthesis);
			output = "while " + output.SubstringStartEnd(indexOfLeftParenthesis + 1, indexOfMatchingParenthesis) + ':' + output.Substring(indexOfMatchingParenthesis + 1);
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			indents ++;
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.DoStatement))
		{
			IEnumerator<SyntaxNode> children = node.ChildNodes().GetEnumerator();
			children.MoveNext();
			ConvertSyntaxNode (children.Current, outputLineIndex, outputCharIndex, indents, parsedMainClass);
			int indexOfWhile = output.IndexOf(WHILE_INDICATOR);
			string condition = output.SubstringStartEnd(indexOfWhile + WHILE_INDICATOR.Length, output.GetIndexOfMatchingParenthesis(indexOfWhile + WHILE_INDICATOR.Length - 1));
			int indexOfNewLine = output.IndexOf('\n');
			if (indexOfNewLine != -1)
				output = output.Remove(indexOfNewLine);
			InsertInOutputFileLines ("while " + condition + ':', outputLineIndex, outputCharIndex, indents);
			indents ++;
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.IfStatement))
		{
			int indexOfNewLine = output.IndexOf('\n');
			if (indexOfNewLine != -1)
				output = output.Remove(indexOfNewLine);
			int indexOfLeftParenthesis = output.IndexOf('(');
			int indexOfMatchingRightParenthesis = output.GetIndexOfMatchingParenthesis(indexOfLeftParenthesis);
			output = "if " + output.SubstringStartEnd(indexOfLeftParenthesis + 1, indexOfMatchingRightParenthesis) + ':' + output.Substring(indexOfMatchingRightParenthesis + 1);
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			indents ++;
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.ElseClause))
		{
			int indexOfNewLine = output.IndexOf('\n');
			if (indexOfNewLine != -1)
				output = output.Remove(indexOfNewLine);
			indents --;
			InsertInOutputFileLines ("else:", outputLineIndex, outputCharIndex, indents);
			indents ++;
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.LocalDeclarationStatement) || node.IsKind(SyntaxKind.FieldDeclaration)) //TODO: Handle multi-dimensional arrays
																												//TODO: Handle multi-dimensional lists
		{
			output = output.TrimEnd(';');
			output = output.Replace("public ", "");
			output = output.Replace("private ", "");
			output = output.Replace("protected ", "");
			output = output.Replace("internal ", "");
			output = output.Replace("new ", "");
			output = output.Replace("SortedDictionary", DICTIONARY_INDICATOR);
			output = output.Replace("SortedList", DICTIONARY_INDICATOR);
			output = output.Replace(KEY_VALUE_PAIR_INDICATOR, GetStaticFileName() + '.' + KEY_VALUE_PAIR_INDICATOR);
			bool isStatic = output.StartsWith(STATIC_INDICATOR);
			if (isStatic)
				output = output.Substring(STATIC_INDICATOR.Length);
			int indexOfLeftCurlyBrace = output.IndexOf('{');
			string initializer = "";
			if (indexOfLeftCurlyBrace != -1 && !output.IsInChar(indexOfLeftCurlyBrace) && !output.IsInString(indexOfLeftCurlyBrace))
			{
				initializer = output.Substring(indexOfLeftCurlyBrace);
				output = output.Remove(indexOfLeftCurlyBrace);
			}
			string variableType;
			string variableName;
			int indexOfEquals = output.IndexOf('=');
			if (indexOfEquals != -1)
			{
				int lastIndexOfSpace = output.LastIndexOf(' ', indexOfEquals - 2);
				variableType = output.Remove(indexOfEquals - 1);
				variableName = output.SubstringStartEnd(lastIndexOfSpace + 1, indexOfEquals - 1);
			}
			else
			{
				int lastIndexOfSpace = output.LastIndexOf(' ');
				variableType = output.Remove(lastIndexOfSpace);
				variableName = output.Substring(lastIndexOfSpace);
			}
			if (variableType.StartsWith(DICTIONARY_INDICATOR))
				variableType = DICTIONARY_INDICATOR;
			else
			{
				int indexOfLeftGenericSymbol = output.IndexOf('<');
				if (indexOfLeftGenericSymbol != -1 && output.IsInGenerics(indexOfLeftGenericSymbol) && !output.IsInChar(indexOfLeftGenericSymbol) && !output.IsInString(indexOfLeftGenericSymbol))
					variableType = "Array[" + output.SubstringStartEnd(indexOfLeftGenericSymbol + 1, output.GetIndexOfMatchingGenericSymbol(indexOfLeftGenericSymbol)) + ']';
				while (indexOfLeftGenericSymbol != -1)
				{
					int indexOfMatchingGenericSymbol = output.GetIndexOfMatchingGenericSymbol(indexOfLeftGenericSymbol);
					if (indexOfMatchingGenericSymbol != -1)
						output = output.RemoveStartEnd(indexOfLeftGenericSymbol, indexOfMatchingGenericSymbol + 1);
					indexOfLeftGenericSymbol = output.IndexOf('<', indexOfLeftGenericSymbol + 1);
				}
			}
			variableName = variableName.Insert(1, TEMPORARY_INDICATOR);
			string sizeSetter = "";
			string[] clauses = output.Split(' ', StringSplitOptions.RemoveEmptyEntries);
			int indexOfLeftSquareBrace = variableType.LastIndexOf('[');
			if (indexOfLeftSquareBrace != -1)
			{
				string elementType = variableType.Remove(indexOfLeftSquareBrace);
				variableType = "Array[" + elementType + "]";
				if (initializer == "")
				{
					string lastClause = clauses[clauses.Length - 1];
					indexOfLeftSquareBrace = lastClause.IndexOf('[');
					if (indexOfLeftSquareBrace != -1)
					{
						string size = lastClause.Substring(indexOfLeftSquareBrace + 1).TrimEnd(';').TrimEnd(']');
						if (size != "")
						{
							string sizeVariable = UNUSED_VARIABLE_NAME + unusedVariableNameCount;
							sizeSetter = "var " + sizeVariable + " = " + size;
							unusedVariableNameCount ++;
							sizeSetter += "\nfor " + UNUSED_VARIABLE_NAME + unusedVariableNameCount + " in range(" + sizeVariable + "):";
							unusedVariableNameCount ++;
							string defaultValue;
							if (elementType == "int" || elementType == "float" || elementType == "double" || elementType == "decimal")
								defaultValue = "0";
							else if (elementType == "string")
								defaultValue = "null";
							else if (elementType == "bool")
								defaultValue = "false";
							else if (elementType == "char")
								defaultValue = 'c' + TEMPORARY_INDICATOR + "har(0)";
							else
								defaultValue = elementType + ".new()";
							sizeSetter += "\n\t" + variableName + ".append(" + defaultValue + ')';
						}
					}
				}
			}
			if (output.StartsWith(CONSTANT_INDICATOR))
			{
				variableName = clauses[2].Insert(1, TEMPORARY_INDICATOR);
				output = CONSTANT_INDICATOR + variableName + " = " + output.Substring(output.IndexOf(clauses[4]));
				output = output.Replace(clauses[1], "");
			}
			else
			{
				output = "var " + variableName;
				if (initializer == "")
				{
					indexOfEquals = output.IndexOf('=');
					if (indexOfEquals != -1)
						initializer = output.Substring(indexOfEquals + 1);
					else
						output += " : " + variableType;
				}
			}
			if (initializer != "")
			{
				if (variableType.StartsWith("Array"))
				{
					bool startsWithLeftCurlyBrace = initializer.StartsWith('{');
					if (startsWithLeftCurlyBrace)
					{
						initializer = initializer.TrimStart('{').TrimEnd('}');
						initializer = '[' + initializer + ']';
					}
					initializer = initializer.Replace("})", "");
				}
				else if (variableType == DICTIONARY_INDICATOR)
				{
					initializer = initializer.Replace("},", "}" + UNUSED_VARIABLE_NAME);
					initializer = initializer.Replace(", ", " : ");
					initializer = initializer.Replace(UNUSED_VARIABLE_NAME, ",");
					initializer = initializer.Replace("{", "");
					initializer = initializer.Replace("}", "");
					initializer = '{' + initializer + '}';
				}
				output += " = " + initializer;
			}
			if (isStatic)
				output = STATIC_INDICATOR + output;
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			outputLineIndex ++;
			outputCharIndex = -1;
			if (sizeSetter != "")
			{
				SyntaxNode methodNode = GetSyntaxNodeOfKindInParents(node, SyntaxKind.MethodDeclaration);
				if (methodNode == null)
					addToReadyMethodContents.AddRange(sizeSetter.Split('\n'));
				else
				{
					InsertInOutputFileLines(sizeSetter, outputLineIndex, outputCharIndex, indents);
					outputLineIndex += sizeSetter.Split('\n').Length;
				}
			}
		}
		else if (node.IsKind(SyntaxKind.ContinueStatement) || node.IsKind(SyntaxKind.BreakStatement) || node.IsKind(SyntaxKind.ReturnStatement))
		{
			InsertInOutputFileLines (output, outputLineIndex, outputCharIndex, indents);
			outputLineIndex ++;
			outputCharIndex = -1;
		}
		else if (node.IsKind(SyntaxKind.CastExpression))
		{
			string initOutput = output;
			output = output.TrimStart('(');
			int indexOfRightParenthesis = output.IndexOf(')');
			output = output.Remove(indexOfRightParenthesis, 1);
			output = output.Insert(indexOfRightParenthesis, "(");
			output += ')';
			typeConversionsDict[initOutput] = output;
		}
		// Console.WriteLine("-Output-");
		// foreach (string line in outputFileLines)
		// 	Console.WriteLine(line);
		// Console.WriteLine("-End output-");
		foreach (SyntaxNode childNode in node.ChildNodes())
			ConvertSyntaxNode (childNode, outputLineIndex, outputCharIndex, indents, parsedMainClass);
		return output;
	}

	static string GetMethodName (ref string str)
	{
		str = str.Replace("public ", "");
		str = str.Replace("private ", "");
		str = str.Replace("protected ", "");
		str = str.Replace("internal ", "");
		str = str.Replace("extern ", "");
		str = str.Replace("virtual ", "");
		str = str.Replace("override ", "");
		str = str.Replace("unsafe ", "");
		str = str.Replace("new ", "");
		int indexOfStatic = str.IndexOf(STATIC_INDICATOR);
		string output = str;
		if (indexOfStatic != -1)
			output = str.Remove(indexOfStatic, STATIC_INDICATOR.Length);
		int indexOfNewLine = output.IndexOf('\n');
		int indexOfLeftParenthesis;
		if (indexOfNewLine != -1)
			indexOfLeftParenthesis = output.LastIndexOf('(', indexOfNewLine);
		else
			indexOfLeftParenthesis = output.IndexOf('(');
		return output.SubstringStartEnd(output.LastIndexOf(' ', indexOfLeftParenthesis - 2) + 1, indexOfLeftParenthesis - 1);
	}
}