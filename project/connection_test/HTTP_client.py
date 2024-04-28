
import sys
import requests


if len(sys.argv) != 3:
    print("Usage: python3 HTTP_client.py <ip_address> <port>")
    sys.exit(1)

ip = sys.argv[1]
port = int(sys.argv[2])

url = "http://{}:{}".format(ip, port)

try:
    # Send a GET request to the server
    response = requests.get(url)

    # Print the response status code
    print("Response status code:", response.status_code)

    # Print the response content (HTML page)
    print("Response content:")
    print(response.text)

except requests.exceptions.RequestException as e:
    print("Error:", e)
