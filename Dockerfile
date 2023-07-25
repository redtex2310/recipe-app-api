FROM python:3.9-alpine3.13
LABEL maintainer="redtex2310@gmail.com"

# Recommended when running python in a container
# Prevents python from buffering output
# Prevents output delay. Displays immediately on the 
# screen
ENV PYTHONBUFFERED 1 

# Copies local files and directory to container
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
# This is default directory where commands will run from
WORKDIR /app
# Allows access port 8000 to connect to django development server
EXPOSE 8000

# By default we're not running on development mode
ARG DEV=false
# Single run command to keep build more efficient
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Creates new virtual env to install app
# Adds to the PATH env
ENV PATH="/py/bin:$PATH"

# Best practice not to use root user
# Evrytime we run with the docker file it's going to run
# as user
USER django-user
