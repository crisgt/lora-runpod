import runpod
import os
import json

MODEL_VOLUME = "/runpod-volume/models"
EXTRA_PATH_FILE = "/comfyui/extra_model_paths.yaml"


# ----------------------------
# Register Network Volume
# ----------------------------
def register_model_paths():
    if not os.path.exists(MODEL_VOLUME):
        raise RuntimeError("Network volume missing at /runpod-volume/models")

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

    print("Model paths registered.")


# ----------------------------
# Inject LoRA Automatically
# ----------------------------
def inject_flux_lora(workflow, lora_name="flux-lora.safetensors", strength=1.2):

    has_lora = any(
        node.get("class_type") == "LoraLoader"
        for node in workflow.values()
    )

    if has_lora:
        return workflow

    # find model node
    model_node_id = None
    for node_id, node in workflow.items():
        if node.get("class_type") in ["UNETLoader", "CheckpointLoaderSimple"]:
            model_node_id = node_id
            break

    if model_node_id is None:
        return workflow

    lora_node_id = str(max(map(int, workflow.keys())) + 1)

    workflow[lora_node_id] = {
        "class_type": "LoraLoader",
        "inputs": {
            "model": [model_node_id, 0],
            "clip": [model_node_id, 1] if "1" else None,
            "lora_name": lora_name,
            "strength_model": strength,
            "strength_clip": strength
        }
    }

    print("LoRA auto injected.")
    return workflow


# ----------------------------
# Main Handler
# ----------------------------
def handler(job):

    register_model_paths()

    workflow = job["input"]["workflow"]

    workflow = inject_flux_lora(workflow)

    return {
        "status": "queued",
        "nodes": len(workflow)
    }


runpod.serverless.start({"handler": handler})
