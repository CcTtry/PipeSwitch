# Kill and restart
This folder contains code for kill-and-restart.

# Environment
You need to add the path to the repo to `PYTHONPATH`.
> 需要将kill_restart的路径添加到```PYTHONPATH```中。例如，添加到/etc/profile 中。
```shell
echo "export  PYTHONPATH=XX/PipeSwitch/kill_restart/:$PYTHONPATH" >> /etc/profile
```
# Usage
```
python kill_restart.py
```
# 解释
> baseline的代码，要启动一个新的模型处理推理任务，串行执行以下操作：
> 1. 停止当前的active_worker
> 2. 初始化启动当前请求所需要的推理模型
> 3. 执行推理任务，并返回推理结果