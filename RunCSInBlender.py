import bpy, subprocess, os, mathutils, sys, math, time

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/local/lib/python3.12/dist-packages')
sys.path.append(os.path.expanduser('~/.local/lib/python3.12/site-packages'))
from pynput import *

mouseButtonsPressed_ = []
keysPressed_ = []
startTime_ = time.perf_counter()

def OnMouseClick (x, y, button, pressed):
	global mouseButtonsPressed_
	if pressed:
		mouseButtonsPressed_.append(button.name)
	else:
		mouseButtonsPressed_.remove(button.name)

mouseListener = mouse.Listener(on_click=OnMouseClick)
mouseListener.start()

def OnKeyPress (key):
	global keysPressed_
	try:
		keysPressed_.append(key.char)
	except AttributeError:
		keysPressed_.append(key)

def OnKeyRelease (key):
	global keysPressed_
	try:
		keysPressed_.remove(key.char)
	except AttributeError:
		keysPressed_.remove(key)

keyboardListener = keyboard.Listener(on_press=OnKeyPress, on_release=OnKeyRelease)
keyboardListener.start()

def Dehomogenize (vector):
	output = mathutils.Vector((vector[0] / vector[3], vector[1] / vector[3], vector[2] / vector[3]))
	return output

def InverseMatrix (matrix):
	output = mathutils.Matrix([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
	determinant = matrix.determinant()
	for i in range(4):
		for j in range(4):
			temp = mathutils.Matrix([[0,0,0], [0,0,0], [0,0,0]])
			column = 0
			for x in range(4):
				if x != i:
					row = 0
					for y in range(4):
						if y != j:
							temp[column][row] = matrix[x][y]
							row += 1
					column += 1
			tempDeterminant = temp.determinant()
			total = i + j
			if total % 2:
				sign = -1
			else:
				sign = 1
			output[j][i] = (sign * tempDeterminant) / determinant
	return output

def ScreenToWorldPoint (screenPoint):
	screenPoint = Cast(screenPoint, 'Vector3')
	region = bpy.context.region
	regionCenter = mathutils.Vector((region.x + region.width / 2, region.y + region.height / 2))
	output = mathutils.Vector((2 * (screenPoint.x - regionCenter.x) / region.width,
		2 * (screenPoint.y - regionCenter.y) / region.height,
		2 * screenPoint.z - 1,
		1))
	inversePerspectiveMatrix = InverseMatrix(bpy.context.space_data.region_3d.perspective_matrix)
	output = inversePerspectiveMatrix @ output 
	output = Dehomogenize(output)
	output.z *= -1
	if os.path.expanduser('~') == '/home/gilead':
		bpy.context.scene.cursor.location = (output.x, output.y, output.z)
	return output

def Cast (value, typeString : str):
	fromTypeString = str(type(value))
	if fromTypeString == "<class 'Vector'>":
		if typeString == 'Vector2':
			return value.to_2d()
		elif typeString == 'Vector3':
			return value.to_3d()
		elif typeString == 'Vector4':
			return value.to_4d()
	raise RuntimeError('Could not cast ' + str(value) + ' to ' + typeString)

def Run (filePath : str, obj):
	global mouseButtonsPressed_
	outputCode = 'self = bpy.data.objects[\'' + obj.name + '\']' + '''
mouseController_ = mouse.Controller()
mousePosition_ = mathutils.Vector((mouseController_.position[0], mouseController_.position[1]))
'''
	outputCode += open(filePath, 'rb').read().decode('utf-8')
	print(outputCode)

	exec(outputCode)