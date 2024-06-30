import bpy, subprocess, os, mathutils, sys

sys.path.append('/usr/lib/python3/dist-packages')
sys.path.append('/usr/local/lib/python3.12/dist-packages')
sys.path.append(os.path.expanduser('~/.local/lib/python3.12/site-packages'))
from pynput import *

def Run (filePath : str, obj):
	outputCode = 'self = bpy.data.objects[\'' + obj.name + '\']' + '''
mousePosition_ = mathutils.Vector()

def OnMouseMove (x, y):
	global mousePosition_
	mousePosition_.x = x
	mousePosition_.y = y
	print('Pointer moved to {0}'.format((x, y)))

def OnMouseClick (x, y, button, pressed):
	print('{0} at {1}'.format('Pressed' if pressed else 'Released',	(x, y)))
	if not pressed:
		return False # Stop listener

def OnMouseScroll (x, y, dx, dy):
	print('Scrolled {0} at {1}'.format('down' if dy < 0 else 'up', (x, y)))

listener_ = mouse.Listener(
	on_move=OnMouseMove,
	on_click=OnMouseClick,
	on_scroll=OnMouseScroll)
listener_.start()
'''
	outputCode += open(filePath, 'rb').read().decode('utf-8')
	# outputCode += '\nlistener_.stop()'
	# print(outputCode)

	exec(outputCode)