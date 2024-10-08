# Use the Ubuntu 22.04 base image
FROM ubuntu:22.04

# Add Python 3.8 to the image
FROM python:3.9


RUN apt-get update

RUN wget https://dl-ssl.google.com/linux/linux_signing_key.pub -O /tmp/google.pub

RUN gpg --no-default-keyring --keyring /etc/apt/keyrings/google-chrome.gpg --import /tmp/google.pub

RUN echo 'deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list

RUN apt-get update 

RUN apt-get install google-chrome-stable -y

WORKDIR /src

COPY ./src/requirements.txt /src

RUN pip install -r requirements.txt

COPY ./src/ /src

CMD ["python", "main.py"]

