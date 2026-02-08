FROM runpod/worker-comfyui:5.5.1-base

ENV COMFYUI_PATH=/runpod-volume/runpod-slim/ComfyUI
ENV PYTHONUNBUFFERED=1
ENV CUDA_VISIBLE_DEVICES=0
ENV HF_HOME=/runpod-volume/.hf

WORKDIR /

COPY handler.py /handler.py

CMD ["python", "/handler.py"]
