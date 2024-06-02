FROM python:3

WORKDIR /usr/src/app
COPY requirements.txt ./
COPY ./ /usr/src/app/

RUN pip install --no-cache-dir --upgrade pip wheel && \
    pip install --no-cache-dir --upgrade -r requirements.txt && \
    pip install .

RUN \
    rm -rf /usr/share/man/* && \
    rm -rf /root/.cache/pip/ && \
    rm -rf /usr/src/app/.git* && \
    rm -rf /usr/src/app/examples && \
    rm -rf /usr/src/app/venv

RUN apt-get purge -y \
        make \
        git \
        wget \
        unzip \
        perl \
        gcc && \
    apt-get autoremove -y && \
    apt-get autoclean -y && \
    apt-get clean all


CMD ["/bin/bash"]
