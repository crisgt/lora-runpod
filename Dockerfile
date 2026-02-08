FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy handler
COPY handler.py .

# The network volume will be mounted at runtime at /runpod-volume
# No need to copy models into the image

CMD ["python", "-u", "handler.py"]
```

**requirements.txt:**
```
runpod
transformers
torch
# Add your other dependencies
