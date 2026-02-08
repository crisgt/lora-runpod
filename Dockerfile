FROM runpod/worker-comfyui:5.5.1-base

ENV COMFYUI_PATH=/runpod-volume/runpod-slim/ComfyUI
ENV PYTHONUNBUFFERED=1
ENV HF_HOME=/runpod-volume/.hf

COPY handler.py /handler.py

CMD ["python", "/handler.py"]
