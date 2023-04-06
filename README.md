# FlyBot

FlyBot是一个可以部署在[fly.io](https://fly.io)上的Telegram机器人，通过FlyBot你可以直接在Telegram使用chatGPT。另外FlyBot也提供了Web API，可以基于Web API开发自己的chatGPT应用，可以通过fly.io做一次网络中转，避免因openai的地域限制而无法使用chatGPT服务。


# 快速部署

## 1、准备工作
首先，注册一个[fly.io](https://fly.io)帐号，建议通过GitHub登录，可以直接通过fly.io部署，十分便捷。

然后，通过Telegram的BotFather创建一个机器，保存好token，并且准备好你的openai的api key。

## 2、准备源码
直接fork本项目到你的GitHub。

## 3、通过Web Cli部署

fly.io目前提供了Web Cli部署功能，可以直接在浏览器内完成部署。[点击这里](https://fly.io/terminal)进入Web Cli，直接选择你fork的到GitHub上的FlyBot项目即可。

当Web Cli准备完成后，直接点击右侧的**flyctl launch**按钮即可。

之后会提示输入如下内容：
```
? App Name (leave blank to use an auto-generated name):
? Select organization: Mark Ericksen (personal)
? Select region: lax (Los Angeles, California (US))
Created app weathered-wave-1020 in organization personal
Wrote config file fly.toml
? Would you like to deploy now? (y/N)
```

- App Name，应用名字，如果不介意随机名字可以留空
- Select organization，默认即可 
- Select region，这里推荐选美国，日本，新加坡等地区
- deploy，不要立刻部署，还需要配置一些内容才能保证FlyBot正常运行

> 注意，如果在Web Cli没有显示FlyBot项目，则可以直接点击左侧底部的**Launch Web Cli**按钮，进入终端后，执行如下命令手动触发部署操作:

```
git clone https://github.com/sunbooshi/FlyBot.git
cd FlyBot
flyctl launch
```

## 4、配置变量

为了确保用户安全使用，一些关键的信息，比如openai的api key，Telegram机器人的token等都是通过fly.io的secrets来配置，尽可能的避免信息泄露。

需要配置的变量有如下几个：

- OPENAI_API_KEY，openai的api key
- TEL_BOT_TOKEN，Telegram机器人的token
- ADMIN_UID，管理员的Telegram user id，只有管理员才能同机器人聊天
- WEB_TOKEN，Web API的请求鉴权token，可以设置一些随机字符，不要太短
- GPT_MODEL，chatGPT模型，可以不设置，默认是gpt-3.5-turbo，如果是plus可以设置为gpt-4，其它模型暂不支持

可以通过如下命令来配置以上变量，以配置OPENAI_API_KEY，openai的api key为例：

```
flyctl secrets set OPENAI_API_KEY="sk-abcdef1234567890"
```
将**sk-abcdef1234567890**替换成你的api key即可。

其他变量也需要依次设置
```
flyctl secrets set TEL_BOT_TOKEN="替换为你的机器人Token"
flyctl secrets set ADMIN_UID="替换为你的user id"
flyctl secrets set WEB_TOKEN="替换为你的web token"
```

## 5、部署、启动应用

直接执行如下命令就可以部署了

```
fly deploy
```

# 使用指南

## 机器人
向机器人直接提问就可以使用chatGPT了。

机器人目前提供了以下几个命令：
- /help，显示机器人所有命令
- /chatid，获取当前的会话id
- /uid，获取用户user id

## Web API

### /api/status
#### 功能
> 获取运行状态，目前只是返回OK，用于判断FlyBot是否已经成功部署且正常运行。

#### method
> GET

#### 参数
> 无

### /api/chat
#### 功能
> 
#### method
> POST

#### 参数
- Token，需要放到Header中，即之前设置的WEB_TOKEN，用于验证请求是否合法
- text, json参数，即向chatGPT发起的问题

#### 返回
```
{
    "status": 0,
    "msg": "OK",
    "result": {
        "response": ""
    }
}
```
当status不为0时，说明请求出错。

response即chatGPT返回的内容。

#### 示例
```
curl -d '{"text":"推荐一首歌"}'  -H "Token: your-web-token" -H "Content-Type: application/json" -X POST http://your-app-name.fly.dev/api/chat
```

# TODO

- [ ] 增加配置功能
- [ ] 增加开发说明

# FAQ
1、如何获取Telegram user id？
> 打开Telegram，在搜索栏搜索 **@userinfobot**，然后点击**start**即可获取自己的user id。

2、支持多人使用吗？
> 机器人暂不支持多人使用，web api没有限制，只要确保请求的header中携带正确的Token即可。

3、如何反馈问题、提需求？
> 你可以直接提issue，也可以加入[Discord频道](https://discord.gg/vPQKQvaXTt)进行反馈。
