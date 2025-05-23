# DJW邮件系统定时发送程序
- 支持配置工作历
- 支持每日定时任务
- 无依赖

```shell
nohup python task.py > djw_email.log 2>&1 &

ps aux | grep task.py

kill -9 xxx
```