FROM python:3.11-slim

RUN apt-get -y update; apt-get -y install curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY ./ ./

RUN poetry install

EXPOSE 5000

CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]