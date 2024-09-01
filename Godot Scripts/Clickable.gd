extends Node
class_name Clickable

func _ready ():
	var collisionShape = CollisionShape3D.new()
	add_child(collisionShape)
	var concavePolygonShape = ConcavePolygonShape3D.new()
	var meshInstance = get_parent().get_child(0) as MeshInstance3D
	var faces = meshInstance.mesh.get_faces()
	for i in range(len(faces)):
		faces[i] *= 10000
	concavePolygonShape.set_faces(faces)
	collisionShape.shape = concavePolygonShape