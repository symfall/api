FROM python:3.9.6
ENV PYTHONUNBUFFERED 1

RUN useradd -m user
USER user
WORKDIR /home/user

ENV PATH=/home/user/.local/bin:${PATH}
COPY --chown=user:user . .

RUN pip install --upgrade pip && pip install --user poetry && \
    poetry config virtualenvs.create false && \
    poetry export --without-hashes | poetry run pip install -r /dev/stdin
