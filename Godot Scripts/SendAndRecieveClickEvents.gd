extends Node3D
class_name SendAndRecieveClickEvents

const RAY_CAST_LENGTH = 99999
var rayCast : RayCast3D

func _ready ():
	rayCast = RayCast3D.new()
	add_child(rayCast)
	rayCast.enabled = false
	rayCast.collision_mask = pow(2, 31)

func _input (inputEvent : InputEvent):
	if inputEvent is InputEventMouseButton && inputEvent.button_index == 1 && inputEvent.pressed:
		var camera = get_viewport().get_camera_3d()
		var mousePosition = get_viewport().get_mouse_position()
		rayCast.global_position = camera.project_ray_origin(mousePosition)
		rayCast.target_position = camera.project_ray_normal(mousePosition) * RAY_CAST_LENGTH
		rayCast.force_raycast_update()
		if rayCast.is_colliding():
			var httpRequest = HTTPRequest.new()
			httpRequest.use_threads = true
			add_child(httpRequest)
			httpRequest.request_completed.connect(OnRequestDone)
			var error = httpRequest.request('http://localhost:8000/' + rayCast.get_collider().get_parent().name)
			if error != OK:
				push_error('HTTP request error: ' + error_string(error))

func OnRequestDone (result, responseCode, headers, body):
	print(body.get_string_from_utf8())