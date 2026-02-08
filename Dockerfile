FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

WORKDIR /app

RUN pip install --no-cache-dir \
    runpod \
    diffusers \
    transformers \
    accelerate \
    safetensors \
    sentencepiece \
    protobuf

COPY handler.py .

ENV TRANSFORMERS_CACHE=/runpod-volume/models
ENV HF_HOME=/runpod-volume/models
ENV HF_HUB_OFFLINE=1

CMD ["python", "-u", "handler.py"]
