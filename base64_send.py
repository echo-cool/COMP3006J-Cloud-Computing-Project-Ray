import base64
import numpy as np
import requests

image_data_list = [
    "zidane.jpg",
    "mzx-1.jpg",
    "mzx-2.jpg",
    "mzx-3.jpg",
    "mzx-4.jpg",
    "mzx-5.jpg",
]


def main():
    for image_name in image_data_list:
        with open(f"test_data/{image_name}", "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")
        response = requests.post(
            "http://ray-node-master:8001/detectBase64",
            json={
                'image_base64_data': image_base64,
            },
        )
        # print(response.content)
        print(response.status_code)
        with open(f"test_data/{image_name}_result.jpg", "wb") as f:
            f.write(response.content)


if __name__ == '__main__':
    while True:
        main()
