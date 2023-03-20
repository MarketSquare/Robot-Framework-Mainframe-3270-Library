FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive

ENV TERM=xterm

USER root

RUN apt-get update && apt-get upgrade -y && \
	apt-get install -y --no-install-recommends \
	python3 \
	python3-pip \
	s3270 \
	xauth \
	xvfb \
	x3270 && \
	rm -rf /var/lib/apt/lists/*

COPY entrypoint.sh entrypoint.sh

RUN chmod a+x entrypoint.sh && \
	useradd --create-home --shell /bin/bash mfuser

USER mfuser
ENV PATH="/home/mfuser/.local/bin:$PATH"

RUN pip3 install --user --no-cache-dir robotframework-mainframe3270
WORKDIR /home/mfuser

ENTRYPOINT [ "/entrypoint.sh" ]
