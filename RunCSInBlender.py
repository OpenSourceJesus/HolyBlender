import bpy, ast

def Do (textBlockName : str):
	for textBlock in bpy.data.texts:
		if textBlock.name == textBlockName:
			tree = ast.parse(textBlock.as_string())
			Run (tree)

def Run (tree : ast.AST):
	