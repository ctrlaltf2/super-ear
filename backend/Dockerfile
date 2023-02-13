# syntax=docker/dockerfile:1.4
FROM python:3.11-alpine AS builder

WORKDIR /code

COPY requirements.txt /code
#RUN --mount=type=cache,target=/root/.cache/pip \
#    pip3 install -r requirements.txt
RUN pip3 install -r requirements.txt

COPY . /code

ENTRYPOINT ["python3"]
CMD ["app.py"]

FROM builder as dev-envs

RUN apk update
RUN apk add git bash

# setup vscode support
RUN addgroup -S docker
RUN adduser -S --shell /bin/bash --ingroup docker vscode

# install docker tools
COPY --from=gloursdocker/docker / /
