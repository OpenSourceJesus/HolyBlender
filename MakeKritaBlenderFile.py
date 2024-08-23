import os, sys, subprocess

sys.path.append(os.path.expanduser('~/HolyBlender/svg.path'))
sys.path.append(os.path.expanduser('~/HolyBlender/svg.path/src'))
sys.path.append(os.path.expanduser('~/HolyBlender/svg.path/src/svg'))
sys.path.append(os.path.expanduser('~/HolyBlender/svg.path/src/svg/path'))
from svg.path import *

from krita import *

# RESOURCES_PATH = os.path.expanduser('~/.local/share/krita')
SAMPLE_COUNT = 30

# [print([a.objectName(), a.text()]) for a in Krita.instance().actions()]
# Krita.instance().action('python_scripter').trigger()

# def GetInfo (item):
#     [print(member) for member in inspect.getmembers(item) if not member[0].startswith('_')]

# GetInfo (Krita.instance().action('python_scripter'))
doc = Krita.instance().activeDocument()
root = doc.rootNode()
pathsStrings = []
for layer in root.childNodes():
	# print(str(layer.type()) + ' ' + str(layer.name()))
	if str(layer.type()) == "vectorlayer":
		for shape in layer.shapes():
			svg = shape.toSvg()
			print(svg)
			indexOfCommandsStart = svg.find(' d="') + 4
			indexOfCommandsEnd = svg.find('"', indexOfCommandsStart)
			pathData = svg[indexOfCommandsStart : indexOfCommandsEnd]
			path = parse_path(pathData)
			normalizedSampleDistance = 0
			pointsStrings = []
			while normalizedSampleDistance <= 1:
				point = path.point(normalizedSampleDistance)
				pointsStrings.append(str(point))
				normalizedSampleDistance += 1.0 / SAMPLE_COUNT
			pathsStrings.append(', '.join(pointsStrings))
open('/tmp/Krita Data', 'wb').write('\n'.join(pathsStrings).encode('utf-8'))
command = [ 'blender', '--python', 'MakeKritaBlenderFile2.py' ]
print(command)

subprocess.check_call(command)