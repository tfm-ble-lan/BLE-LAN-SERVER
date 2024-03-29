FROM ubuntu:latest

MAINTAINER Guillermo Jimenez "geonexus@gmail.com", Noel Ruiz "noelrl@gmail.com"
RUN apt-get update -y && apt-get install -y python3.11  python3.11-dev python3-pip gcc openssh-server
RUN systemctl enable ssh

COPY ble_lan_server /app/ble_lan_server
ENV PYTHONPATH /app
#WORKDIR /app/ble_lan_server
WORKDIR /app/
RUN ls /app
ENV PORT 80
#COPY ble_lan_server/requirements.txt /app
RUN pip3 install -r ble_lan_server/requirements.txt
COPY .flake8 /app
RUN flake8 ble_lan_server

ENTRYPOINT ["python3"]
CMD ["ble_lan_server/app.py"]
