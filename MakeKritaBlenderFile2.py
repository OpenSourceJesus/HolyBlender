import bpy, os
from mathutils import *

data = open('/tmp/Krita Data', 'rb').read().decode('utf-8')
bpy.ops.wm.read_homefile(app_template='2D_Animation')
for pointsString in data.split('\n'):
	greasePencilData = bpy.data.grease_pencils.new('GPencil')
	greasePencil = bpy.data.objects.new(greasePencilData.name, greasePencilData)
	bpy.context.collection.objects.link(greasePencil)
	layer = greasePencilData.layers.new('lines')
	frame = layer.frames.new(bpy.context.scene.frame_current)
	stroke = frame.strokes.new()
	stroke.line_width = 12
	stroke.start_cap_mode = 'FLAT'
	stroke.end_cap_mode = 'FLAT'
	stroke.use_cyclic = True
	pointsStrings = pointsString.split(', ')
	stroke.points.add(len(pointsStrings))
	imagePath = os.path.expanduser('~/bomb-game/Assets/Art/Textures/Slime.png')
	bpy.ops.image.open(filepath=imagePath)
	image = bpy.data.images[-1]
	material = bpy.data.materials.new(name='GPencil Material')
	greasePencil.data.materials.append(material)
	bpy.data.materials.create_gpencil_data(material)
	material.grease_pencil.fill_style = 'TEXTURE'
	material.grease_pencil.show_fill = True
	material.grease_pencil.fill_image = image
	material.grease_pencil.color = (0, 0, 0, 1)
	material.grease_pencil.mix_factor = 0
	uvSize = Vector((image.size[0], -image.size[1]))
	uvSize /= 4
	material.grease_pencil.texture_scale = uvSize
	material.grease_pencil.texture_offset = uvSize / 2
	i = 0
	for pointString in pointsStrings:
		indexOfPlus = pointString.find('+')
		x = float(pointString[1 : indexOfPlus])
		y = float(pointString[indexOfPlus + 1 : -2])
		point = Vector((x, y))
		stroke.points[i].co = [point.x, point.y, 0]
		stroke.points[i].uv_fill = point
		stroke.points[i].pressure = 10
		stroke.points[i].vertex_color = (0.0, 0.0, 0.0, 1.0)
		i += 1
bpy.ops.wm.save_mainfile()