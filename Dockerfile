# clean base image containing only comfyui, comfy-cli and comfyui-manager
FROM runpod/worker-comfyui:5.5.1-base

# install custom nodes into comfyui (first node with --mode remote to fetch updated cache)
RUN comfy node install --exit-on-fail ComfyUI_Comfyroll_CustomNodes --mode remote
# Could not resolve unknown custom node 'Reroute' (no aux_id provided) - skipped

# download models into comfyui
RUN comfy model download --url https://huggingface.co/black-forest-labs/FLUX.1-schnell/resolve/main/ae.safetensors --relative-path models/vae --filename ae.safetensors
RUN comfy model download --url https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors --relative-path models/text_encoders --filename t5xxl_fp8_e4m3fn.safetensors
RUN comfy model download --url https://huggingface.co/Comfy-Org/stable-diffusion-3.5-fp8/resolve/main/text_encoders/clip_l.safetensors --relative-path models/clip --filename clip_l.safetensors
RUN comfy model download --url https://huggingface.co/bstungnguyen/Flux/blob/main/flux1-dev.safetensors --relative-path models/diffusion_models --filename flux1-dev.safetensors
RUN comfy model download --url https://huggingface.co/CRIS2223/michi/blob/main/flux-lora.safetensors --relative-path models/loras --filename flux-lora.safetensors
# RUN # Could not find URL for flux-lora.safetensors

# copy all input data (like images or videos) into comfyui (uncomment and adjust if needed)
# COPY input/ /comfyui/input/
