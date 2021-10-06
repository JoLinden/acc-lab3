FROM ubuntu
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y git
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install celery
RUN pip3 install flask
RUN git clone https://github.com/JoLinden/acc-lab3
WORKDIR acc-lab3
EXPOSE 5000
CMD ["python3","app.py"]