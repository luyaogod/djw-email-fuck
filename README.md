# DJW邮件系统定时发送程序
- 支持配置工作历
- 支持每日定时任务

```shell
#   创建虚拟环境
python3 -m venv vnev

#   激活虚拟环境
source  vnev/bin/activate

#  安装依赖包
pip install requests

#   运行程序
nohup python3 task.py > djw_email.log 2>&1 &

#  查看进程
ps aux | grep task.py

#   停止进程
kill -9 xxx
```