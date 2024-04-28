
import http.server
import socketserver
import sys

if len(sys.argv) != 2:
    print("Usage: python3 HTTP_server.py <port>")
    sys.exit(1)

port = int(sys.argv[1])

# Set up a simple HTTP request handler
class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    pass


# Create a TCP server
with socketserver.TCPServer(("", port), MyHttpRequestHandler) as httpd:
    print("Server started at localhost:" + str(port))

    # Start serving HTTP requests
    httpd.serve_forever()
