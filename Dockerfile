FROM python:3.8-slim-buster

ARG USER='python'

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --requirement requirements.txt

RUN useradd "${USER}"

USER "${USER}"

COPY . .

CMD ["python", "/usr/src/app/drone-slack-file/main.py"]
