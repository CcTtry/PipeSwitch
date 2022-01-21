<!-- TOC -->

- [Client](#client)
- [Files](#files)
- [Environment](#environment)
- [Usage 用法](#usage-用法)
  - [client_inference](#client_inference)
  - [client_switching](#client_switching)
- [疑问](#疑问)

<!-- /TOC -->
# Client

This folder contains codes for clients.
> 这个文件夹包含了一些客户端的代码

# Files

- client_inference.py: In each iteration, send an inferece request, wait for the reply and record the latency without switching.
  > client_inference.py: 在每次迭代中，发送一个推断请求，等待应答并记录等待时间，而不切换。(同步，需要阻塞的推理)，客户端一共发送100个推理任务的请求。
- client_switching.py: In each iteration, send a training request, then send an inference request to record the latency with switching.
  > client_switching.py: 在每个迭代中，发送一个训练请求，然后发送一个推理请求来记录切换的延迟，客户端一共发送25个推理任务的请求。
  > throughout.py 和 throughout_ready.py的衡量标准是**吞吐量**，而不是**时间**，与上面两个文件（client_inference.py和client_switching.py）相区别。
  > throughout_ready.py表示的文章中图6中的虚线部分


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

# 疑问

1. <font color = "red"> 图6(a)中scheduling_cycle 变化时，为何pipeswitch和MPS的吞吐量几乎保持不变？
</font>
2. <font color = "red"> 图6(b)中，横坐标表示的是，从0开始到$x$ s之后，每个推理任务的平均处理时延？
</font>