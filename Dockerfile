FROM runpod/base:0.4.0-cuda12.1.0

RUN pip install runpod requests

ENV COMFYUI_PATH=/runpod-volume/runpod-slim/ComfyUI
ENV HF_HOME=/runpod-volume/.hf
ENV PYTHONUNBUFFERED=1

COPY handler.py /handler.py

CMD ["python", "/handler.py"]
