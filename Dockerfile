FROM runpod/worker-comfyui:5.5.1-base

COPY handler.py /handler.py

ENV EXTRA_MODEL_PATHS=/comfyui/extra_model_paths.yaml

CMD ["python", "/handler.py"]
