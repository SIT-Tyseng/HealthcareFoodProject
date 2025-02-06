# Use the specified base image
FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

# Set the working directory inside the container
WORKDIR /app

# ARG WHEEL_DIR=./Dev/wheels

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user with a specific UID and GID
RUN groupadd -g 10001 appgroup && \
    useradd -u 10000 -g appgroup -m appuser

# Switch to the non-root user
USER appuser

# Copy the requirements file and set ownership
COPY --chown=appuser:appgroup requirements.txt /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the wheel file and set ownership
COPY --chown=appuser:appgroup ./Dev/wheels/flash_attn-2.3.5+cu117torch1.13cxx11abiTRUE-cp310-cp310-linux_x86_64.whl /app/

# Install the flash_attn package
RUN pip3 install --no-cache-dir flash_attn-2.3.5+cu117torch1.13cxx11abiTRUE-cp310-cp310-linux_x86_64.whl

# Copy the rest of the application code and set ownership
COPY --chown=appuser:appgroup . /app/

# Expose the port your application will run on (if applicable)
# EXPOSE 8080

# Keep the container running by default
CMD ["tail", "-f", "/dev/null"]