# rss-feed-translator

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

English | [中文说明](./README.zh-CN.md)

Translate your rss and atom feed in an easy way.

## Features

- RSS & Atom feed support
- Translate between many language
- Support custom translate api token for better experience
- Free translate endpoint by default to make it easy to have a try

## Installation

Docker image is available [here](https://github.com/Colin-XKL/rss-feed-translator/pkgs/container/rss-feed-translator)

```shell
sudo docker run -d --name rss-feed-translator -p 10050:5000 ghcr.io/colin-xkl/rss-feed-translator:v1.0.0
```
docker compose example

```yaml
version: '3.3'
services:
    rss-feed-translator:
        image: 'ghcr.io/colin-xkl/rss-feed-translator:v1.0.0'
        container_name: feed-translator
        ports:
            - '10050:5000'
        environment:
            - ALIYUN_ACCESS_KEY_ID=xxxxx
            - ALIYUN_ACCESS_KEY_SECRET=xxxxxx
        restart: always
```
## Run Locally

Clone the project, and run app.py

```shell
# update pip and install poetry
# ensure use python3
pip install -U pip setuptools
pip install poetry

# install dependencies
poetry install

# run
python3 app.py
```

## Used By

This project is used by the following projects:

- RSS Man X

## Currently supported translator

- DeelL (Free, slow)
- Aliyun (Token needed, fast, free tier available)

## Screenshots

![Compare: original feed and translated feed](https://blog-1301127393.file.myqcloud.com/BlogImgs/202305140149482.png)

![Compare: translated feed in Reeder app](https://blog-1301127393.file.myqcloud.com/BlogImgs/202305140149484.png)

![Homepage of the project](https://blog-1301127393.file.myqcloud.com/BlogImgs/202305140149485.png)

## Roadmap

- Additional translation backend support

- Add more support for easy setup

- More translation mode, such as inline translation

## License

[MIT](https://choosealicense.com/licenses/mit/)

