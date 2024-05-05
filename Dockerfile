FROM python:3.12.3-slim-bullseye

WORKDIR /usr/src/app

RUN --mount=type=bind,source=requirements.txt,target=requirements.txt \
    --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY ./src .

CMD ["sh", "-c", "while true; do python ./main.py; sleep 86400; done"]
