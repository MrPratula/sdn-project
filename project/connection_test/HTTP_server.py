
import http.server
import socketserver


def main():
    # Define the port number you want to use
    PORT = 8000

    # Set up a simple HTTP request handler
    class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
        pass

    # Create a TCP server
    with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
        print("Server started at localhost:" + str(PORT))

        # Start serving HTTP requests
        httpd.serve_forever()


if __name__ == "__main__":
    main()
