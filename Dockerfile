FROM osgeo/gdal:ubuntu-small-3.0.3

ARG DEBIAN_FRONTEND=noninteractive

USER root

COPY . /nrn-app

WORKDIR /

# System update and install the required dependencies.
RUN apt-get update

RUN apt-get install -y wget \
    build-essential \
    zlib1g-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libpq-dev \ 
    libssl-dev \
    libreadline-dev \
    libffi-dev \ 
    gnupg2 \
    binutils \ 
    postgresql \ 
    postgresql-contrib \ 
    postgis \
    python-psycopg2

# Install Python 3.6 from source.
RUN wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz

RUN tar -xf Python-3.6.3.tgz

WORKDIR /Python-3.6.3

RUN ./configure && make -j 8 && make altinstall

# Install pip3.
RUN apt-get install -y python3-pip

WORKDIR /nrn-app

# Install Python packages needed to execute data processing.
RUN pip3 install -r requirements.txt

# Test modules with import script.
RUN python3 tests/modules.py
