import http.server, socketserver

PORT = 8000

with socketserver.TCPServer(('', PORT), http.server.SimpleHTTPRequestHandler) as server:
	print('Serving at port ' + str(PORT) + '\nOpen localhost:' + str(PORT) + '/index.html in your web browser to see the output')
	server.serve_forever()