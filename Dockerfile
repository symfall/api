FROM python:3.6

# Copy source code of the project
WORKDIR /code
COPY . .

# Install needs libraries
RUN apt-get update && \
    apt-get -y install entr && \
    pip install pipenv && \
    pipenv install -v --system --deploy --dev
