# Use the specified base image
FROM nvidia/cuda:11.7.1-cudnn8-devel-ubuntu22.04

# Set the working directory inside the container
WORKDIR /app

# ARG WHEEL_DIR=./Dev/wheels

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip libgl1 libglib2.0-0 passwd sudo && \
    rm -rf /var/lib/apt/lists/*

# Create a symbolic link so 'python' points to 'python3'
RUN ln -s /usr/bin/python3 /usr/bin/python    

# Create a non-root user with a specific UID and GID
RUN groupadd -g 10001 appgroup && \
    useradd -u 10000 -g appgroup -m appuser 

RUN echo "root:password" | chpasswd
RUN echo "appuser:password" | chpasswd

# Change ownership of the application directory
RUN chown appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Copy the requirements file and set ownership
COPY --chown=appuser:appgroup requirements.txt /app/

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the wheel file and set ownership, given that docker buildx is available
COPY --chown=appuser:appgroup --from=wheels flash_attn-2.3.5+cu117torch1.13cxx11abiTRUE-cp310-cp310-linux_x86_64.whl /app/
# Uncomment the line below if docker buildx is not available
#COPY --chown=appuser:appgroup ./Dev/wheels/flash_attn-2.3.5+cu117torch1.13cxx11abiTRUE-cp310-cp310-linux_x86_64.whl /app/

# Install the flash_attn package, uncomment this line if docker buildx is not available
RUN pip3 install --no-cache-dir flash_attn-2.3.5+cu117torch1.13cxx11abiTRUE-cp310-cp310-linux_x86_64.whl

# Copy the rest of the application code and set ownership
COPY --chown=appuser:appgroup . /app/

# Expose the port your application will run on (if applicable)
# EXPOSE 8080

# Keep the container running by default
CMD ["tail", "-f", "/dev/null"]