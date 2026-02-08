import runpod
import os
import random

MODEL_VOLUME = "/runpod-volume/models"
EXTRA_PATH_FILE = "/comfyui/extra_model_paths.yaml"


def register_paths():
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
    with open(EXTRA_PATH_FILE, "w") as f:
        f.write(yaml_content)


def build_flux_workflow(prompt, lora=None, width=1024, height=1024):

    workflow = {
        "11": {
            "class_type": "DualCLIPLoader",
            "inputs": {
                "clip_name1": "t5xxl_fp8_e4m3fn.safetensors",
                "clip_name2": "clip_l.safetensors",
                "type": "flux"
            }
        },
        "12": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {
                "ckpt_name": "flux1-dev.safetensors"
            }
        },
        "13": {
            "class_type": "EmptySD3LatentImage",
            "inputs": {
                "width": width,
                "height": height,
                "batch_size": 1
            }
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "text": prompt,
                "clip": ["11", 0]
            }
        },
        "15": {
            "class_type": "FluxGuidance",
            "inputs": {
                "guidance": 4,
                "conditioning": ["6", 0]
            }
        },
        "20": {
            "class_type": "KSampler",
            "inputs": {
                "seed": random.randint(1,999999999),
                "steps": 20,
                "cfg": 1,
                "sampler_name": "euler",
                "scheduler": "simple",
                "denoise": 1,
                "model": ["12", 0],
                "positive": ["15", 0],
                "negative": ["6", 0],
                "latent_image": ["13", 0]
            }
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["20", 0],
                "vae": ["12", 2]
            }
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "flux",
                "images": ["8", 0]
            }
        }
    }

    if lora:
        workflow["30"] = {
            "class_type": "LoraLoader",
            "inputs": {
                "model": ["12", 0],
                "clip": ["11", 0],
                "lora_name": lora,
                "strength_model": 1.2,
                "strength_clip": 1.2
            }
        }
        workflow["20"]["inputs"]["model"] = ["30", 0]

    return workflow


def handler(job):

    register_paths()

    prompt = job["input"].get("prompt", "masterpiece")
    lora = job["input"].get("lora", None)

    workflow = build_flux_workflow(prompt, lora)

    return {
        "workflow": workflow,
        "status": "queued"
    }


runpod.serverless.start({"handler": handler})
