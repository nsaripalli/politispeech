FROM python:3.7.3-slim-stretch

RUN apt-get -y update && apt-get -y install gcc
RUN pip3 --no-cache-dir install tensorflow==1.15.2 gpt-2-simple starlette uvicorn ujson
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /
COPY app.py /
COPY checkpoint /checkpoint

# Make changes to the requirements/app here.
# This Dockerfile order allows Docker to cache the checkpoint layer
# and improve build times if making changes.
# Clean up APT when done.

ENTRYPOINT ["python3", "-X", "utf8", "app.py"]