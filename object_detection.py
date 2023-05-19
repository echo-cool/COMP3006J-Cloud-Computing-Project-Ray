import base64

import torch
from PIL import Image
import numpy as np
from io import BytesIO
from fastapi.responses import Response
from fastapi import FastAPI
from pydantic import BaseModel, Field
from ray import serve

app = FastAPI()


class ImageData(BaseModel):
    image_base64_data: str


@serve.deployment(num_replicas=2, route_prefix="/")
@serve.ingress(app)
class APIIngress:
    def __init__(self, object_detection_handle) -> None:
        self.handle = object_detection_handle

    @app.post(
        "/detectBase64",
        responses={200: {"content": {"image/jpeg": {}}}},
        response_class=Response,
    )
    async def detectBase64(self, image_data: ImageData):
        image_ref = await self.handle.detectBase64.remote(image_data.image_base64_data)
        image = await image_ref
        file_stream = BytesIO()
        image.save(file_stream, "jpeg")
        return Response(content=file_stream.getvalue(), media_type="image/jpeg")

    @app.get(
        "/detect",
        responses={200: {"content": {"image/jpeg": {}}}},
        response_class=Response,
    )
    async def detect(self, image_url: str):
        image_ref = await self.handle.detect.remote(image_url)
        image = await image_ref
        file_stream = BytesIO()
        image.save(file_stream, "jpeg")
        return Response(content=file_stream.getvalue(), media_type="image/jpeg")


@serve.deployment(
    ray_actor_options={"num_cpus": 1, "num_gpus": 0.25},
    num_replicas=4,
    # autoscaling_config={"min_replicas": 1, "max_replicas": 10},
)
class ObjectDetection:
    def __init__(self):
        # self.model =
        self.model = torch.hub.load('yolov5/', 'custom', 'yolov5s.pt', source='local')  # local repo
        # self.model = torch.hub.load("yolov5/", "yolov5s", source="local", pretrained=True)
        self.model.cuda()

    def detectBase64(self, image_base64: str):
        image = Image.open(BytesIO(base64.b64decode(image_base64)))
        result_im = self.model(image)
        return Image.fromarray(result_im.render()[0].astype(np.uint8))

    def detect(self, image_url: str):
        result_im = self.model(image_url)
        return Image.fromarray(result_im.render()[0].astype(np.uint8))


entrypoint = APIIngress.bind(ObjectDetection.bind())
