# syntax=docker/dockerfile:1.4
# -- frontend
FROM node:lts AS node

ENV CI=true

WORKDIR /code
COPY ./frontend/package.json /code/package.json
COPY ./frontend/package-lock.json /code/package-lock.json
RUN npm ci

COPY ./frontend /code

RUN npm run build # outputs /code/build

# -- backend

FROM python:3.11-alpine AS py

WORKDIR /code

COPY ./backend/requirements.txt /code
RUN pip3 install -r requirements.txt

COPY ./backend /code
COPY --from=node /code/build /super-ear/srv

FROM py AS prod

ENTRYPOINT ["python3"]
CMD ["app.py"]
