import ray
from ray import serve

ray.init("ray://ray-node-master:10001", namespace="serve")
serve.start(detached=True, http_options={"host": "0.0.0.0"})


@serve.deployment
def hello(request):
    return "Hello"


hello.deploy()

print(serve.list_deployments())
