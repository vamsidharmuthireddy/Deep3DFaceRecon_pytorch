FROM nvidia/cuda:11.4.0-base-ubuntu20.04
# FROM nvidia/cuda:11.4.0-cudnn8-devel-ubuntu20.04
# FROM pytorch/pytorch:1.6.0-cuda10.1-cudnn7-runtime

# Install base utilities


ENV DEBIAN_FRONTEND noninteractive
RUN echo "en_US UTF-8" > /etc/locale.gen

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ENV TZ Europe/Paris
ENV DEBIAN_FRONTEND noninteractive
ENV LC_ALL C.UTF-8

# Install system requirements
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    wget \
    locales \
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
    curl \
    python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install python 3.6.15
RUN apt update -y && apt upgrade -y && \
    apt-get install -y wget build-essential checkinstall  libreadline-gplv2-dev  libncursesw5-dev  libssl-dev  libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev && \
    cd /usr/src && \
    wget https://www.python.org/ftp/python/3.6.15/Python-3.6.15.tgz && \
    tar xzf Python-3.6.15.tgz && \
    cd Python-3.6.15 && \
    ./configure --enable-optimizations && \
    make install





RUN mkdir DEEP3DFACERECON_PYTORCH

COPY ./ DEEP3DFACERECON_PYTORCH/

WORKDIR DEEP3DFACERECON_PYTORCH

COPY nvdiffrast/docker/10_nvidia.json /usr/share/glvnd/egl_vendor.d/10_nvidia.json

# nvidia-container-runtime
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility,graphics

ENV CUDA_HOME='/usr/local/cuda'
ENV LD_LIBRARY_PATH=${CUDA_HOME}/lib64
ENV PATH=${CUDA_HOME}/bin:${PATH}


RUN python3 -m pip install --upgrade pip

# # # RUN python3 get-pip.py
RUN pip3 install -r requirements.txt
RUN pip3 uninstall -y numpy
RUN pip3 install numpy==1.18.1

RUN pip3 install nvdiffrast/

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]



# # SHELL ["conda", "run", "--no-capture-output", "-n", "deep3d_pytorch", "/bin/bash", "-c"]
# ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0",  "--server.enableCORS=false"]    

# ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "deep3d_pytorch", "/bin/bash", "-c", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0",  "--server.enableCORS=false"]    
