FROM gitpod/workspace-full-vnc
RUN sudo apt-get update && \
    sudo apt-get install -y libgtk-3-dev && \
    sudo apt-get install -y openjdk-17-jdk && \
    sudo rm -rf /var/lib/apt/lists/*