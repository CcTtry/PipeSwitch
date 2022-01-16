# Client

This folder contains codes for clients.
> 这个文件夹包含了一些客户端的代码

# Files

- client_inference.py: In each iteration, send an inferece request, wait for the reply and record the latency without switching.
  > client_inference.py: 在每次迭代中，发送一个推断请求，等待应答并记录等待时间，而不切换。(同步，需要阻塞的推理)
- client_switching.py: In each iteration, send a training request, then send an inference request to record the latency with switching.
  > client_switching.py: 在每个迭代中，发送一个训练请求，然后发送一个推理请求来记录切换的延迟。

# Environment
You need to add the path to the repo to `PYTHONPATH`.
> 需要将client的路径添加到```PYTHONPATH```中。例如，添加到/etc/profile 中。
```shell
echo "export  PYTHONPATH=XX/PipeSwitch/client/:$PYTHONPATH" >> /etc/profile
```
# Usage 用法

## client_inference

```
python client_inference.py [model_name] [batch_size]
```
`model_name` can be `resnet152`, `inception_v3` or `bert_base`.

Example:

```
python client_inference.py resnet152 8
```

## client_switching

```
python client_switching.py [model_name] [batch_size]
```
`model_name` can be `resnet152`, `inception_v3` or `bert_base`.

Example:

```
python client_switching.py resnet152 8
```