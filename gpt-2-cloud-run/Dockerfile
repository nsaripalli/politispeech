FROM tiangolo/uvicorn-gunicorn:python3.7

RUN apt-get -y update && apt-get -y install gcc

WORKDIR /app
COPY checkpoint /app/checkpoint

# Make changes to the requirements/app here.
# This Dockerfile order allows Docker to cache the checkpoint layer
# and improve build times if making changes.
#RUN pip3 --no-cache-dir install tensorflow==1.* gpt-2-simple starlette ujson
RUN pip install starlette
COPY test.py /app/main.py

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*