import http.server, socketserver

port = 8000
MAX_PORT = 8100

while port <= MAX_PORT:
	try:
		with socketserver.TCPServer(('', port), http.server.SimpleHTTPRequestHandler) as server:
			print('Serving at port' + port + '\nOpen localhost:' + port + '/index.html in your web browser to see the output')
			server.serve_forever()
		break
	except:
		port += 1
