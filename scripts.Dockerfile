FROM python:3.7 as build
RUN pip install pipenv
WORKDIR /build
COPY Pipfile /build/
RUN bash -c 'PIPENV_VENV_IN_PROJECT=1 pipenv install --skip-lock'

FROM python:3.7-slim as application
WORKDIR /app
COPY --from=build /build /app/
COPY ./scripts/ /app/scripts/
EXPOSE 80
ENTRYPOINT [ ".venv/bin/python", "-m", "scripts.commands"]