import base64
import numpy as np
import requests


def main():
    with open("test.jpg", "rb") as f:
        image_base64 = base64.b64encode(f.read())
    response = requests.post(
        "http://http://127.0.0.1:8000/detectBase64",
        data={
            'image_base64_data': image_base64,
        },
        headers={"Content-Type": "application/json"},
    )
    print(response.status_code)


if __name__ == '__main__':
    main()
