FROM python:3.11-slim as base
RUN apt-get -y update; apt-get -y install curl
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
COPY . .
RUN poetry install
COPY ./fixtures ./fixtures
COPY ./todo_app ./todo_app

FROM base as production
EXPOSE 80
CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:80", "todo_app.app:create_app()"]

FROM base as development
EXPOSE 5000
CMD ["poetry", "run", "flask", "run", "--host", "0.0.0.0"]