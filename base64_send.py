import base64
import numpy as np
import requests


def main():
    with open("test_data/zidane.jpg", "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
    response = requests.post(
        "http://127.0.0.1:8000/detectBase64",
        json={
            'image_base64_data': image_base64,
        },
    )
    # print(response.content)
    print(response.status_code)


if __name__ == '__main__':
    main()
