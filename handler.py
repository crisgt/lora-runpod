import runpod
import os

MODEL_VOLUME = "/runpod-volume/models"


def mount_network_models():
    if not os.path.exists(MODEL_VOLUME):
        raise RuntimeError("Network volume not mounted at /runpod-volume/models")

    extra_paths = "/comfyui/extra_model_paths.yaml"

    yaml_content = f"""
loras:
  - {MODEL_VOLUME}/loras
vae:
  - {MODEL_VOLUME}/vae
clip:
  - {MODEL_VOLUME}/clip
text_encoders:
  - {MODEL_VOLUME}/text_encoders
diffusion_models:
  - {MODEL_VOLUME}/diffusion_models
"""

    with open(extra_paths, "w") as f:
        f.write(yaml_content)

    print("Network model paths registered.")


def handler(job):
    try:
        mount_network_models()

        workflow = job["input"]["workflow"]

        return {
            "status": "success",
            "workflow_received": True,
            "nodes": len(workflow)
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


runpod.serverless.start({"handler": handler})
