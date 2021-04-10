FROM python:3.7 as build
RUN pip install pipenv
WORKDIR /build
COPY Pipfile /build/
RUN bash -c 'PIPENV_VENV_IN_PROJECT=1 pipenv install --skip-lock'

FROM alpine AS get_model
ARG MODEL_URL="https://openaipublic.azureedge.net/clip/models/40d365715913c9da98579312b702a82c18be219cc2a73407c4526f58eba950af/ViT-B-32.pt"
RUN wget ${MODEL_URL} -O model.pt

FROM python:3.7-slim as application
ENV CLIP_MODEL_NAME=/model.pt
COPY --from=get_model model.pt ${CLIP_MODEL_NAME}
WORKDIR /app
COPY --from=build /build /app/
COPY . /app/
EXPOSE 80
CMD [ ".venv/bin/python", "-m", "sanic", "api.server.app", "--port=80", "--host=0.0.0.0"]