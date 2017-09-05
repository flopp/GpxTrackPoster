FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY src ./src
COPY create_poster.py ./
RUN pip install --no-cache-dir -r requirements.txt