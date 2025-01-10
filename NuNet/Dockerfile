# Use an official NVIDIA CUDA image
FROM nvidia/cuda:12.4.0-base-ubuntu20.04

# Set up environment variables for CUDA
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# Install Python 3.9 and pip
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3.9-distutils \
    curl \
    && apt-get clean \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Install pip using get-pip.py
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.9

# Set Python 3.9 as the default Python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1

# Install PyTorch and PyTorch Lightning
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
RUN pip install lightning

# Set the working directory and copy the project files into the container
WORKDIR /app
COPY . /app

RUN pip install torch==2.4.0 torchvision==0.19.0 torchaudio==2.4.0 --index-url https://download.pytorch.org/whl/cu124


# Install Python dependencies
RUN pip install -r requirements.txt

# Set the entry point to Python script
CMD ["python3", "main.py"]
