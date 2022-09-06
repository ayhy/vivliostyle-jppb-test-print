FROM node:16-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
  git \
  curl \
  build-essential \
  libgtk2.0 \
  libnss3-dev \
  libatk-bridge2.0-0 \
  libdrm-dev \
  libxkbcommon-dev \
  libgbm-dev \
  libasound-dev \
  fonts-ipaexfont \
 && apt-get clean \
 && apt purge pandoc \
 && wget https://github.com/jgm/pandoc/releases/download/2.19.2/pandoc-2.19.2-1-amd64.deb \
 && dpkg -x pandoc-2.19.2-1-amd64.deb $HOME \
 && rm -rf /var/lib/apt/lists/*

COPY book/package.json .
COPY book/yarn.lock .
RUN yarn