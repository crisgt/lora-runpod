import os
import runpod
import subprocess
import requests

COMFY_PATH = os.getenv("COMFYUI_PATH")

def start_comfy():
    subprocess.Popen(
    ["python","main.py","--listen","0.0.0.0","--port","8188","--force-fp16"],
    cwd=os.environ["COMFYUI_PATH"]
    )

start_comfy()

def handler(job):
    workflow = job["input"]["workflow"]

    r = requests.post(
        "http://127.0.0.1:8188/prompt",
        json={"prompt": workflow},
        timeout=600,
    )

    return r.json()

runpod.serverless.start({"handler": handler})
