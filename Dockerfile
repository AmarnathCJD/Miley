# We Are Using KaliLinux Here
FROM kalilinux/kali-rolling
# Set To Non Interactive Mode, So That It Doesn't Ask For Any Start-Up Configuration
ARG DEBIAN_FRONTEND=noninteractive
# Config Term - Xterm with support for 256 colors
ENV TERM xterm-256color
# Update System And Install Sudo
RUN apt-get update && apt upgrade -y && apt-get install sudo -y

# Install All Requirements
RUN apt-get install -y\
    apt-utils \
    git \
    postgresql \
    postgresql-client \
    postgresql-server-dev-all \
    wget \
    python3 \
    python3-pip \
    sqlite3 \
    ffmpeg
    
# Purge Unused Req.
RUN apt-get autoremove --purge
# Update PiP
RUN pip3 install --upgrade pip setuptools 
RUN pip3 install --upgrade pip
RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi 
RUN if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi 
# Clear Cache
RUN rm -r /root/.cache
# Git Clone Main Repo And Config As WorkDir
RUN git clone https://github.com/AmarnathCdj/Miley /root/Miley
RUN mkdir /root/Miley/bin/
WORKDIR /root/Miley/
RUN chmod +x /usr/local/bin/*
# Install All Req. in requirements File
RUN pip3 install -r requirements.txt
# Run Bot, (Run Bot) 
CMD ["python3","-m","Evie"]
