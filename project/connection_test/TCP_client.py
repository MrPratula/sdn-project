import urllib.request
import requests


def main():
    url = 'http://localhost:8000'

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


def test0():
    contents = urllib.request.urlopen("https://info.cern.ch/").read()
    print(contents)


if __name__ == "__main__":
    main()
