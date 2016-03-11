
FROM gazebo:libgazebo6
MAINTAINER Masayoshi Nakamura mchmasa@gmail.com

# install packages
RUN apt-get update && apt-get install -q -y \
    build-essential \
    cmake \
    imagemagick \
    libboost-all-dev \
    libgts-dev \
    libjansson-dev \
    libtinyxml-dev \
    mercurial \
    nodejs \
    nodejs-legacy \
    npm \
    pkg-config \
    psmisc\
    && rm -rf /var/lib/apt/lists/*

# install gazebo packages
RUN apt-get update && apt-get install -q -y \
    libgazebo6-dev=6.5.1* \
    && rm -rf /var/lib/apt/lists/*

# clone gzweb
RUN hg clone https://bitbucket.org/osrf/gzweb ~/gzweb

# build gzweb
RUN cd ~/gzweb \
    && hg up default \
    && ./deploy.sh -m

# setup environment
EXPOSE 8080
EXPOSE 7681

#################################
#Brica and PyGazebo

RUN apt-get update && apt-get install -q -y \
    git \
    python-pip

RUN pip install numpy

RUN cd ~/ \
    && git clone https://github.com/masayoshi-nakamura/CognitiveArchitectureLecture.git

ENV GAZEBO_MODEL_PATH $HOME/CognitiveArchitectureLecture/models:$GAZEBO_MODEL_PATH

# pygazebo (Do not use version 3.0.0-2014.1)
RUN cd ~/ \
    && git clone https://github.com/jpieper/pygazebo.git \
    && cd pygazebo \
    && git checkout 3eaac84 \
    && pip install six --upgrade \
    && python setup.py install

# Nengo
RUN pip install nengo
RUN pip install nengo_gui

CMD [ "/bin/bash" ]