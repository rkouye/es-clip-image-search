FROM python:3.7 as build
RUN pip install pipenv
WORKDIR /build
COPY Pipfile /build/
RUN bash -c 'PIPENV_VENV_IN_PROJECT=1 pipenv install --skip-lock'

FROM python:3.7-slim as application
WORKDIR /app
COPY --from=build /build /app/
COPY . /app/
EXPOSE 80
CMD [ ".venv/bin/python", "-m", "sanic", "api.server.app", "--port=80", "--host=0.0.0.0"]