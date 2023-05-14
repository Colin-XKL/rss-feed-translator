# rss-feed-translator

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

[English](./README.md) | 中文说明

一个翻译RSS和ATOM类型的信息源的简易工具

## 特性

- 支持RSS 和 ATOM类型的feed
- 支持多种语言间的互相翻译
- 支持自定义翻译平台的密钥, 以便获得更好的翻译体验
- 默认调用免费的翻译平台接口, 你可以快速上手试用

## 安装

Docker 镜像正在开发中...

## 本地运行

克隆本项目, 运行 `app.py`

```shell
# 更新 pip, 安装包管理器 poetry
# 确保使用的是 python3
pip install -U pip setuptools
pip install poetry

# 安装依赖
poetry install

# 运行
python3 app.py
```

## 当前支持的翻译平台

- DeelL (免费, 较慢)
- 阿里云 (需要密钥, 快, 每月有免费额度可用)

## 项目截图

原feed和翻译后feed的对比图
![Compare: original feed and translated feed](https://blog-1301127393.file.myqcloud.com/BlogImgs/202305140149482.png)
reeder app中查看翻译后的feed
![Compare: translated feed in Reeder app](https://blog-1301127393.file.myqcloud.com/BlogImgs/202305140149484.png)
本项目首页的页面, 可以输入一个feed url, 快速生成一个可以直接访问到翻译后feed 的新url
![Homepage of the project](https://blog-1301127393.file.myqcloud.com/BlogImgs/202305140149485.png)

## 接下来的计划

- 支持更多翻译平台接口

- 完善文档和周边工具等以便可以更轻松的使用本项目

- 支持更多翻译模式, 比如原文和译文分段穿插

## 协议

[MIT](https://choosealicense.com/licenses/mit/)

