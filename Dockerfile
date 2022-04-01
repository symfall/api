FROM python:3.9.7-slim

ENV PYTHONUNBUFFERED 1
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

RUN apt-get update && \
    apt-get install gcc -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd -m user
USER user

WORKDIR /home/user
ENV PATH=/home/user/.local/bin:${PATH}

WORKDIR /home/user/app
COPY --chown=user:user . .

RUN pip install --upgrade pip virtualenv && \
    pip install --user poetry==1.1.13 && \
    poetry config virtualenvs.create false && \
    poetry export --without-hashes | poetry run pip install -r /dev/stdin
