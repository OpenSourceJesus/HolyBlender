extends Node
class_name Clickable

func _ready ():
	var collisionShape = CollisionShape3D.new()
	add_child(collisionShape)
	var concavePolygonShape = ConcavePolygonShape3D.new()
	var meshInstance = get_parent() as MeshInstance3D
	concavePolygonShape.set_faces(meshInstance.mesh.get_faces())
	collisionShape.shape = concavePolygonShape