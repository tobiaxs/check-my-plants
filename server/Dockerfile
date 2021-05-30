FROM python:3.9.4-slim-buster

WORKDIR /app

# Set env variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1

# Add poetry path variable
ENV PATH="$POETRY_HOME/bin:$PATH"

# Install necessary soft
RUN apt-get update \
  && apt-get install -y netcat curl make gcc postgresql python3-dev libpq-dev \
  && apt-get clean

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Configure poetry
RUN poetry config virtualenvs.create false

# Copy & install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

COPY . .

ENTRYPOINT ["bash" , "entrypoint.sh"]
