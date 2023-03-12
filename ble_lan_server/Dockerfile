FROM ubuntu:latest

MAINTAINER Guillermo Jimenez "geonexus@gmail.com", Noel Ruiz "noelrl@gmail.com"
RUN apt-get update -y && apt-get install -y python3.11  python3.11-dev python3-pip
COPY ble_lan_server /app/ble_lan_server
ENV PYTHONPATH /app
#WORKDIR /app/ble_lan_server
WORKDIR /app/
RUN ls /app
ENV PORT 80
RUN pip3 install -r ble_lan_server/requirements.txt

## NGINX
# Download and Install Nginx
RUN apt-get install -y nginx
# Remove the default Nginx configuration file
RUN rm -v /etc/nginx/nginx.conf
# Copy a configuration file from the current directory
ADD nginx.conf /etc/nginx


ENTRYPOINT ["python3"]
CMD ["ble_lan_server/run.py"]
