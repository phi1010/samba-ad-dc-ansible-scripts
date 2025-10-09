FROM docker.io/ubuntu:latest
RUN apt update && apt install  openssh-server sudo -y
RUN useradd -rm -d /home/ansible -s /bin/bash -g root -G sudo ansible
RUN  echo 'ansible:logmein' | chpasswd
# This keeps the host key the same across container restarts
RUN service ssh start
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
WORKDIR /home/ansible/
EXPOSE 22
CMD ["/usr/sbin/sshd","-D"]