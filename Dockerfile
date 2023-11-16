FROM python:3.10-slim-buster


# Install Debian packages
RUN apt-get -qq update && apt-get -qq -y install curl git

# Expose ports
EXPOSE 5000

# Tell Python to not generate .pyc
ENV PYTHONDONTWRITEBYTECODE 1

# Turn off buffering
ENV PYTHONUNBUFFERED 1

# Set working directory and addour Flask API files
RUN mkdir /src
WORKDIR /src

ENV PYTHONPATH "${PYTHONPATH}:/src:/src/api"

# Install requirements using poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml requirements.txt /src/
RUN poetry install -n --no-root --no-dev

