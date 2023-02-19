FROM ubuntu:20.04
# FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

# Install base utilities


ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && \
    apt-get install -y build-essential  && \
    apt-get install -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN apt-get update && apt-get install -y --no-install-recommends \
    pkg-config \
    libglvnd0 \
    libgl1 \
    libglx0 \
    libegl1 \
    libgles2 \
    libglvnd-dev \
    libgl1-mesa-dev \
    libegl1-mesa-dev \
    libgles2-mesa-dev \
    cmake \
    curl


# Install miniconda
ENV CONDA_DIR /opt/conda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
     /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

RUN mkdir DEEP3DFACERECON_PYTORCH

COPY ./ DEEP3DFACERECON_PYTORCH/

WORKDIR DEEP3DFACERECON_PYTORCH

COPY nvdiffrast/docker/10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility,graphics



RUN conda env create -f ENV_180223.yml
SHELL ["conda", "run", "-n", "deep3d_pytorch", "/bin/bash", "-c"]
# RUN conda activate deep3d_pytorch

RUN pip3 install streamlit==1.10.0



ENV CUDA_HOME=$CONDA_PREFIX
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64
ENV PATH=${CUDA_HOME}/bin:${PATH}


SHELL ["conda", "run", "-n", "deep3d_pytorch", "/bin/bash", "-c"]
RUN pip3 install nvdiffrast/


EXPOSE 8501

# SHELL ["conda", "run", "--no-capture-output", "-n", "deep3d_pytorch", "/bin/bash", "-c"]
# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0",  "--server.enableCORS=false"]    

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "deep3d_pytorch", "/bin/bash", "-c", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0",  "--server.enableCORS=false"]    
