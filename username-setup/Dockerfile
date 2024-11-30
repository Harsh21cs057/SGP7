# Use Ubuntu as the base image
FROM ubuntu:20.04

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt-get update && apt-get install -y \
    software-properties-common \
    git \
    curl \
    wget \
    bash && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3.10-venv python3.10-distutils && \
    apt-get clean

# Set Python 3.10 as the default Python version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1 && \
    update-alternatives --config python3

# Install pip for Python 3.10
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3

# Set the working directory
WORKDIR /app

# Install Maigret in a virtual environment
RUN git clone https://github.com/soxoj/maigret && \
    cd maigret && \
    python3 -m venv venv && \
    bash -c "source venv/bin/activate && pip3 install . && deactivate" && \
    cd ..


RUN git clone https://github.com/sherlock-project/sherlock && \
    cd sherlock && \
    python3 -m venv venv && \
    bash -c "source venv/bin/activate && pip3 install . && deactivate" && \
    echo 'export PATH=/app/sherlock/venv/bin:$PATH' >> ~/.bashrc && \
    cd ..


# Install Socialscan in a virtual environment
RUN git clone https://github.com/iojw/socialscan.git && \
    cd socialscan && \
    python3 -m venv venv && \
    bash -c "source venv/bin/activate && pip3 install . && deactivate" && \
    cd ..

# Install Blackbird in a virtual environment
RUN git clone https://github.com/p1ngul1n0/blackbird && \
    cd blackbird && \
    python3 -m venv venv && \
    bash -c "source venv/bin/activate && pip3 install -r requirements.txt && deactivate" && \
    cd ..

# Copy the scripts and any required files into the container
COPY ScriptP3.py ./ScriptP3.py
COPY final_op2.py ./final_op2.py
COPY finalScript.py ./finalScript.py

# Create required directories
RUN mkdir -p ./combined_output

# Set the entrypoint to execute the final script
ENTRYPOINT ["python3", "./finalScript.py"]



# for build this docker image
# docker build -t username-setup .    

#for run this docker image
#   docker run --rm -it -v C:\Users\sacha\OneDrive\Desktop\SGP7\username-setup\username_op:/app/combined_output username-setup

