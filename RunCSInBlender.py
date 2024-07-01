import bpy, subprocess, os, mathutils, sys

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/local/lib/python3.12/dist-packages')
sys.path.append(os.path.expanduser('~/.local/lib/python3.12/site-packages'))
from pynput import *

mouseButtonsPressed_ = []
keysPressed_ = []

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

def Dehomogenize (v):
	ret = mathutils.Vector((v[0] / v[3], v[1] / v[3], v[2] / v[3]))
	return ret

def InverseMatrix (m):
	output = mathutils.Matrix([[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]])
	determinant = m.determinant()
	for i in range(4):
		for j in range(4):
			temp = mathutils.Matrix([[0,0,0], [0,0,0], [0,0,0]])
			col = 0
			for x in range(4):
				if x != i:
					row = 0
					for y in range(4):
						if y != j:
							temp[col][row] = m[x][y]
							row += 1
					col += 1
			tempDeterminant = temp.determinant()
			total = i + j
			if total % 2:
				sign = -1
			else:
				sign = 1
			output[j][i] = (sign * tempDeterminant) / determinant
	return output

def ScreenToWorldPoint (screenPoint):
	region = bpy.context.region
	regionCenter = mathutils.Vector((region.x + region.width / 2, region.y + region.height / 2))
	output = mathutils.Vector((2 * (screenPoint.x - regionCenter.x) / region.width,
		2 * (screenPoint.y - regionCenter.y) / region.height,
		2 * screenPoint.z - 1,
		1))
	inversePerspectiveMatrix = InverseMatrix(bpy.context.space_data.region_3d.perspective_matrix)
	output = inversePerspectiveMatrix @ output 
	output = Dehomogenize(output)
	return output

def Run (filePath : str, obj):
	global mouseButtonsPressed_
	outputCode = 'self = bpy.data.objects[\'' + obj.name + '\']' + '''
mouseController_ = mouse.Controller()
mousePosition_ = mathutils.Vector((mouseController_.position[0], mouseController_.position[1]))'''
	outputCode += open(filePath, 'rb').read().decode('utf-8')
	print(outputCode)

	exec(outputCode)