FROM ubuntu:latest

MAINTAINER Guillermo Jimenez "geonexus@gmail.com", Noel Ruiz ""
RUN apt-get update -y && apt-get install -y python3.11  python3.11-dev python3-pip
WORKDIR /app
COPY ble-lan-server /app
ENV PORT 80
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["run.py"]
