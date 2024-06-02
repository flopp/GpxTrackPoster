FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY ./ /usr/src/app/

RUN pip install --upgrade pip wheel && \
    pip install --upgrade -r requirements.txt && \
    pip install .

RUN \
    rm -rf /usr/src/app/.git* && \
    rm -rf /usr/src/app/examples && \
    rm -rf /usr/src/app/venv

RUN apt-get purge -y \
        make \
        gcc &&\
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    apt-get clean all
