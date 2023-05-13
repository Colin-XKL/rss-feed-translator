# 阿里云翻译API 配置指南

## 准备工作

1. 申请阿里云账号
2. 进入控制台, 右上角搜索翻译, 进入翻译控制台, 第一次使用, 按流程开通翻译服务(按使用量后付费模式,
   每月免费额度一百万字符)
3. 控制台右上角头像进入AccessKey管理
4. (不推荐)直接复制账户的AccessKey ID和AccessKey Secret 备用

(推荐) 创建专用的子用户
AccessKey管理页(页面标题为访问控制), 选择用户选项卡新建用户
示例: 新建名为translate的新子账户, 验证身份后确定即可创建完成. 新建的用户建议勾选仅API访问
在用户列表页, 选择刚才新建的用户, 点击添加权限, 在弹出的窗口中, 定位到搜索框, 搜索翻译关键词, 勾选所有相关角色, 确定保存
接下来复制新创建的子账户的AccessKey ID和AccessKey Secret

## 使用方法

将`AccessKey ID`和`AccessKey Secret`填入环境变量, 并且指定translator为`aliyun`即可

## 传送门

- [阿里云RAM访问控制页](https://ram.console.aliyun.com/users)

## 附录

- [机器翻译通用版文档](https://help.aliyun.com/document_detail/158244.html)
- [阿里云翻译服务管理面板](https://mt.console.aliyun.com/automl/project/list)

