extends Node
class_name AddMeshCollision

func _ready ():
	var collisionShape = CollisionShape3D.new()
	add_child(collisionShape)
	var meshInstance = get_parent().get_child(0) as MeshInstance3D
	#var concavePolygonShape = ConcavePolygonShape3D.new()
	#var faces = meshInstance.mesh.get_faces()
	#for i in range(len(faces)):
		#faces[i] *= 10000
	#concavePolygonShape.set_faces(faces)
	#collisionShape.shape = concavePolygonShape
	collisionShape.shape = meshInstance.mesh.create_trimesh_shape()
	collisionShape.shape.backface_collision = true