# syntax=docker/dockerfile:1.4
# -- frontend
FROM node:lts AS node

ENV CI=true

WORKDIR /code
COPY ./frontend/package.json /code/package.json
COPY ./frontend/package-lock.json /code/package-lock.json
RUN npm ci

COPY ./frontend /code

# Why does python:3.11-alpine not resolve domains lol
RUN wget "https://raw.githubusercontent.com/vishnubob/wait-for-it/81b1373f17855a4dc21156cfe1694c31d7d1792e/wait-for-it.sh"

RUN npm run build # outputs /code/build

# -- backend

FROM python:3.11-alpine AS prod

WORKDIR /code


COPY ./backend/requirements.txt /code
RUN pip3 install -r requirements.txt

COPY ./backend /code
COPY --from=node /code/build /super-ear/srv
COPY --from=node /code/wait-for-it.sh /bin/wait-for-it.sh
RUN chmod +x /bin/wait-for-it.sh
RUN apk add --no-cache bash

# FROM py AS prod

# ENTRYPOINT ["python3"]
# CMD ["main.py"]
