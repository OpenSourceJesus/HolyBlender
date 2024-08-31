extends Node
class_name SendAndRecieveClickEvents

func _input (inputEvent : InputEvent):
	if inputEvent is InputEventMouseButton && inputEvent.button_index == 1:
		var httpRequest = HTTPRequest.new()
		add_child(httpRequest)
		httpRequest.request_completed.connect(OnRequestDone)
		var error = httpRequest.request('https://localhost:8000/' + '')
		if error != OK:
			push_error('HTTP request error: ' + error_string(error))

func OnRequestDone (result, responseCode, headers, body):
	var json = JSON.new()
	json.parse(body.get_string_from_utf8())
	var response = json.get_data()
	print(response.headers['User-Agent'])