# rss-feed-translator

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

[English](./README.md) | 中文说明

一个翻译RSS和ATOM类型的信息源的简易工具

## 特性

- 支持 RSS 和 ATOM 类型的feed ([什么是RSS - 知乎](https://www.zhihu.com/question/384290217))
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

打开项目主页(默认绑定到`5000`端口, 本地运行地址为`http://localhost:5000`), 输入待翻译的feed 地址,点击按钮即可自动生成翻译后的feed的链接.
链接默认访问自身的api接口去获取和翻译 feed 内容

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

## 如何参与开发与贡献

下文以windows系统为例讲解如何参与本项目的开发

### 本地开发环境

安装好Python3 环境, 建议的版本Python >=3.9

根据实际情况, 配置pip镜像源以避免下载速度太慢  [清华pypi镜像传送门](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/)

命令行运行命令时如果需要配置代理可参考[这篇文章](https://juejin.cn/post/7130206938919927838)

Idea, PyCharm 配置代理可[参考这里](https://learnku.com/articles/47061)

#### 1. 安装poetry (包管理工具)

#### 1.a 直接安装

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

如果你使用的是应用商店版的python ,  `py` 更换为 `python`

#### 1.b 通过scoop 安装poetry [推荐]

scoop 是一款windows 上的包管理工具, 可以像Linux 的apt/yum 和Mac 上的brew一样便捷地安装所需的软件包及其依赖

[官方文档安装scoop](https://github.com/ScoopInstaller/Install#readme)

[中文安装scoop教程](https://sspai.com/post/52496)

```shell
# 启用远程安装软件包的权限
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

irm get.scoop.sh | iex
# 如果在墙内速度太慢可以手动指定代理
irm get.scoop.sh -Proxy 'http://<ip:port>' | iex
```

(可选) 安装aria2 组件来启用并行下载, 加速软件包安装

```shell
scoop install aria2
```

安装poetry组件

```shell
scoop install poetry
```

### 2. 安装依赖的软件包

```shell
# 下载本项目
git clone https://github.com/Colin-XKL/rss-feed-translator.git

cd rss-feed-translator

poetry install
```

### 3. 运行项目

```shell
python3 ./app.py
```

### 4. 配置环境变量和翻译平台的Token

部分翻译平台(如阿里云)需要提供AccessKey ID 和AccessKey Secret 才可访问API.
可以参考[阿里云翻译配置说明](docs/config_translators/aliyun.md)

在项目根目录新建`.env`文件, 填入相关配置项即可

```dotenv
ALIYUN_ACCESS_KEY_ID="xxxxx"
ALIYUN_ACCESS_KEY_SECRET="xxxxxx"
```


一些可用来测试的feed:
- https://feeds.feedburner.com/visualcapitalist
- https://pytorch.org/feed.xml
## 协议

[MIT](https://choosealicense.com/licenses/mit/)

