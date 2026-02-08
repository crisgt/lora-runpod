import runpod
import requests
import os
import json

COMFY_API = "http://127.0.0.1:8188/prompt"
MODEL_VOLUME = "/runpod-volume/models"


def load_workflow(workflow):
    return {"prompt": workflow}


def ensure_volume():
    if not os.path.exists(MODEL_VOLUME):
        raise RuntimeError(f"Network volume not mounted: {MODEL_VOLUME}")
    print(f"Using network models from: {MODEL_VOLUME}")


def handler(job):
    try:
        ensure_volume()

        workflow = job["input"]["workflow"]

        payload = load_workflow(workflow)

        response = requests.post(
            COMFY_API,
            json=payload,
            timeout=300
        )

        return {
            "status": "success",
            "comfy_response": response.json()
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


runpod.serverless.start({"handler": handler})
