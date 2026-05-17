FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       bash \
       ca-certificates \
       minimap2 \
       python3 \
       samtools \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
