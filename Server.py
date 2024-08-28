import http.server, socketserver

PORT = 8000
with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as server:
    print("Serving at port", PORT)
    server.serve_forever()
