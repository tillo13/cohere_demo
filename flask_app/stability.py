import os
import base64
import io
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Set environment variables (you need to replace 'your-api-key' with your actual API key)
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
os.environ['STABILITY_KEY'] = 'sk-XBHFHCjydMK9VGYsYqopsl8WLronBr6HDpg8P81S6KrGq8Rq'  # Replace 'your-api-key' with your actual key

# Set up connection to the API
stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0",
)

# Initial generation parameters
answers = stability_api.generate(
    prompt="expansive landscape rolling greens with gargantuan yggdrasil, intricate world-spanning roots towering under a blue alien sky, masterful, ghibli",
    seed=4253978046,
    steps=50,
    cfg_scale=8.0,
    width=1024,
    height=1024,
    samples=1,
    sampler=generation.SAMPLER_K_DPMPP_2M
)

# Processing response
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            print("Content filter activated. Try a different prompt.")
        elif artifact.type == generation.ARTIFACT_IMAGE:
            # The image is received in binary format
            byte_data = artifact.binary

            # We convert the bytes to a base64 string
            base64_data = base64.b64encode(byte_data).decode()

            # Now we print the base64 string to the console
            print(base64_data)