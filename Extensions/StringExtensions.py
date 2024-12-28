def IndexOfAny (string : str, findAny : list[str], startIndex = 0):
	output = len(string)
	for find in findAny:
		indexOfFind = string.find(find, startIndex)
		if indexOfFind != -1:
			output = min(indexOfFind, output)
	if output == len(string):
		return -1
	return output

def LastIndexOfAny (string : str, findAny : list[str], startIndex = -1):
	output = -1
	if startIndex == -1:
		startIndex = len(string) - 1
	for find in findAny:
		indexOfFind = string.rfind(find, 0, startIndex)
		if indexOfFind != -1:
			output = max(indexOfFind, output)
	return output

def IndexOfMatchingRightCurlyBrace (string : str, charIndex : int):
	curlyBraceTier = 1
	indexOfCurlyBrace = charIndex
	while indexOfCurlyBrace != -1:
		indexOfCurlyBrace = IndexOfAny(string, [ '{', '}' ], indexOfCurlyBrace + 1)
		if indexOfCurlyBrace != -1:
			if string[indexOfCurlyBrace] == '{':
				curlyBraceTier += 1
			else:
				curlyBraceTier -= 1
				if curlyBraceTier == 0:
					return indexOfCurlyBrace
	return -1

def IndexOfMatchingRightParenthesis (string : str, charIndex : int):
	parenthesisTier = 1
	indexOfParenthesis = charIndex
	while indexOfParenthesis != -1:
		indexOfParenthesis = IndexOfAny(string, [ '(', ')' ], indexOfParenthesis + 1)
		if indexOfParenthesis != -1:
			if string[indexOfParenthesis] == '(':
				parenthesisTier += 1
			else:
				parenthesisTier -= 1
				if parenthesisTier == 0:
					return indexOfParenthesis
	return -1

def IndexOfMatchingLeftParenthesis (string : str, charIndex : int):
	parenthesisTier = 1
	indexOfParenthesis = charIndex
	while indexOfParenthesis != -1:
		indexOfParenthesis = LastIndexOfAny(string, [ '(', ')' ], indexOfParenthesis - 1)
		if indexOfParenthesis != -1:
			if string[indexOfParenthesis] == '(':
				parenthesisTier -= 1
				if parenthesisTier == 0:
					return indexOfParenthesis
			else:
				parenthesisTier += 1
	return -1

def IsInString_CS (string : str, charIndex : int):
	if charIndex == 0 or charIndex == len(string) - 1:
		return False
	output = False
	indexOfDoubleQuote = -1
	while True:
		indexOfDoubleQuote = string.find('\"', indexOfDoubleQuote + 1)
		if indexOfDoubleQuote > charIndex:
			return output
		elif indexOfDoubleQuote != -1:
			output = not output
		else:
			return output

def IsInChar (string : str, charIndex : int):
	if charIndex == 0 or charIndex == len(string) - 1:
		return False
	else:
		return string[charIndex - 1] == '\'' and string[charIndex + 1] == '\''

def Remove (string : str, startIndex : int, count : int):
	return string[: startIndex] + string[startIndex + count :]

def RemoveStartEnd (string : str, startIndex : int, endIndex : int):
	return Remove(string, startIndex, endIndex - startIndex)

def GetCountAtStart (string : str, find : str, startIndex : int = 0):
	output = 0
	while string.startswith(find):
		string = string[len(find) :]
		output += 1
	return output

def GetCountOfAnyAtStart (string : str, findAny : list[str], startIndex : int = 0):
	output = 0
	while True:
		found = False
		for find in findAny:
			if string.startswith(find):
				string = string[len(find) :]
				output += 1
				found = True
		if not found:
			break
	return output

def IsInComment_CS (string : str, charIndex : int):
	indexOfComment = string.rfind('//')
	indexOfNewLine = string.find('\n', indexOfComment)
	return charIndex > indexOfComment and charIndex < indexOfNewLine

def IsNumber (value : str) -> bool:
	try:
		float(value)
	except ValueError:
		return False
	return True
