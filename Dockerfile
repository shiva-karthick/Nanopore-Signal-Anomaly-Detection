# Development Dockerfile for Nanopore Signal Processing

FROM python:3.11-slim

# Set the default working directory
WORKDIR /app

# Install system dependencies for signal processing and development
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ffmpeg \
    libsndfile1 \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries for signal processing and data science
RUN pip install --no-cache-dir \
    numpy \
    scipy \
    matplotlib \
    pandas \
    edlib \
    scikit-learn \
    jupyterlab \
    h5py \
    seaborn

# Copy your project files (optional, for production)
# COPY . /app

# Use bash as the default command for interactive development
CMD ["bash"]

# Example usage:
# docker build -t nanopore_signal_processing-dev .
# docker run -it --rm -v $(pwd):/app nanopore_signal_processing-dev
# docker run -it --rm -v $(pwd):/app nanopore_signal_processing-dev python3 src/main.py