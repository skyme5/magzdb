FROM python:3.10-slim-bullseye

RUN pip install -U magzdb

RUN apt update && \
    apt install wget --yes && \
    apt-get clean autoclean && \
    apt-get autoremove --yes

WORKDIR /tmp

ENTRYPOINT [ "magzdb", "--downloader", "wget" ]