<!-- TOC -->

- [说明](#说明)
- [1. Introduction 引言](#1-introduction-引言)
- [2. Contents 内容](#2-contents-内容)
- [3. Brief usage  简要用法](#3-brief-usage--简要用法)
- [4. Scripts to reproduce figures in our paper. 复现我们论文中的数据的脚本](#4-scripts-to-reproduce-figures-in-our-paper-复现我们论文中的数据的脚本)
- [5. Contact 联系](#5-contact-联系)
- [学习过程记录](#学习过程记录)
  - [路径添加](#路径添加)
  - [根据端口查询任务](#根据端口查询任务)
    - [查询对应端口的信息，获取其PID](#查询对应端口的信息获取其pid)
    - [kill某进程](#kill某进程)
  - [尝试运行](#尝试运行)
    - [执行步骤](#执行步骤)
    - [遇到如下问题](#遇到如下问题)
      - [问题1 执行client_inference.py失败](#问题1-执行client_inferencepy失败)
        - [问题描述](#问题描述)
        - [解决办法](#解决办法)
      - [问题2 执行kill_restart.py失败](#问题2-执行kill_restartpy失败)
        - [问题描述](#问题描述-1)
        - [解决办法 【待探究，后续可以在运行的容器中，执行命令，观察结果】](#解决办法-待探究后续可以在运行的容器中执行命令观察结果)
      - [问题3 构建镜像时，无法git clone的问题](#问题3-构建镜像时无法git-clone的问题)
        - [问题描述](#问题描述-2)
        - [解决办法](#解决办法-1)
      - [问题4 构建pipeswitch:pipeswitch 镜像时，出现问题](#问题4-构建pipeswitchpipeswitch-镜像时出现问题)
        - [问题描述](#问题描述-3)
        - [解决办法](#解决办法-2)
        - [构造 mps镜像](#构造-mps镜像)
      - [构造ready_model镜像](#构造ready_model镜像)
      - [清理所有创建失败的镜像](#清理所有创建失败的镜像)
      - [问题5 如何利用 构建的docker镜像，并运行](#问题5-如何利用-构建的docker镜像并运行)
        - [执行过程](#执行过程)
        - [遇到问题](#遇到问题)
        - [解决办法](#解决办法-3)

<!-- /TOC -->
# 说明
本人持以学习的目的，对源仓库进行中文翻译 && 学习。
# 1. Introduction 引言

This repository contains the source code for our OSDI'20 paper ["PipeSwitch: Fast Pipelined Context Switching for Deep Learning Applications"](https://www.usenix.org/conference/osdi20/presentation/bai). In addition, it contains some codes for systems which are compared with our system.

> 这个存储库包含了的OSDI’20论文的源代码 [“PipeSwitch: Fast Pipelined Context Switching for Deep Learning Applications”](https://www.usenix.org/conference/osdi20/presentation/bai)。此外，它还包含了一些系统的代码，并与我们的系统进行了比较。

# 2. Contents 内容

- [PipeSwitch](https://github.com/netx-repo/PipeSwitch/tree/main/pipeswitch): Our proposed system. 

  > 我们提出的系统。

- [Ready model](https://github.com/netx-repo/PipeSwitch/tree/main/ready_model): The process with the required model is already loaded in the GPU. This solution provides the lower bound, which is the lowest latency we can achieve for an inference task.

  > 具有所需模型的进程已经加载到GPU中。此解决方案提供了下界，即我们可以为推理任务实现的最低延迟。

- [Kill and restart](https://github.com/netx-repo/PipeSwitch/tree/main/kill_restart): It stops the training task in the GPU, and then starts the inference task. 

  > 它停止GPU中的训练任务，然后启动推理任务。

- [PyTorch plugins](https://github.com/netx-repo/PipeSwitch/tree/main/pytorch_plugin): Modified PyTorch files, which are necessary for running PipeSwitch.

  >  修改了PyTorch相关文件，这是运行PipeSwitch所必需的文件。

- [Tasks](https://github.com/netx-repo/PipeSwitch/tree/main/task): Models used for our evaluations.  

  > 用于我们评估的模型。

- [Util](https://github.com/netx-repo/PipeSwitch/tree/main/util): Some common functions. For example, establishing TCP connections.

  > 一些常见的功能，例如:建立TCP连接。

- [Clients](https://github.com/netx-repo/PipeSwitch/tree/main/client): Clients for sending requests.

  > 发送请求的客户端。

# 3. Brief usage  简要用法
0. Compile PyTorch for PipeSwitch. Ready-model and kill-and-restart could use original PyTorch.

    > 为PipeSwitch编译PyTorch。Ready-model和kill-and-restart可以使用原生的PyTorch。
1. Start the server you are interested, which can be PipeSwitch, ready-model or kill-and-restart.

   > 启动您感兴趣的服务器，可以是PipeSwitch、ready-model或kill-and-restart。
2. Start the client to send requests.

   > 启动客户端发送请求。

More details are included in README under folders for each system.
更多细节包含在每个系统的文件夹下的README文档。

# 4. Scripts to reproduce figures in our paper. 复现我们论文中的数据的脚本

For the convenience, we implemented some scripts to reproduce our results reported in our paper.We assume that you are using a host machine to do experiments in a remote server.Thus, before using our scripts, you need to configure passwordless ssh access to the remote server.We also expect you install python and docker on both the host and the remote machine.By default, we use a server with NVIDIA V100 GPU with 16G GPU memory, such as AWS EC2 p3.2xlarge instances.

> 为了方便起见，我们实现了一些脚本来重现我们在论文中报告的结果。我们假设您正在使用一台主机在远程服务器上进行实验。因此，在使用我们的脚本之前，您需要配置对远程服务器的无密码ssh访问。我们还希望您安装python和docker在主机和远程机器上。默认情况下，我们使用带有NVIDIA V100 GPU和16G GPU内存的服务器，例如AWS EC2 p3.2xlarge实例。

After you have configured the remote server, you need to add its IP address and host name in the file ```scripts/config/server.txt```.Then you can run the script ```scripts/experiment.sh``` and wait for the result.

> 配置完远程服务器后，您需要在文件```scripts/config/server.txt```中添加它的IP地址和主机名。然后您可以运行脚本``` scripts/ experimental .sh```并等待结果。

```scripts/experiment.sh``` will do the following things:
- Create a docker image with compiled PyTorch locally.
- Export the docker image to a file.
- Load the image file from the host machine to the remote server.
- Import the image file on the remote server.
- Create different docker images for different experiments on the remote server based on the basic image.
- Run experiments for figure 5-9.

> ```Scripts / experimental.sh```将做以下事情:
>
> - 使用本地编译的PyTorch创建一个docker图像。
> - 导出docker镜像到一个文件。
> - 将镜像文件从主机加载到远程服务器。
> - 在远程服务器上导入镜像文件。
> - 在基本镜像的基础上，为远程服务器上的不同实验创建不同的docker镜像。
> - 运行图5-9的实验。

You could modify the script to adapt to your requirement.For example, you can compile PyTorch and create the basic docker image directly on the remote server.
We use different branches for different points in the figures.These branches are now in Zhihao's repo, and we will move them to this repo in the future.
> 您可以修改脚本以适应您的需求。例如，您可以编译PyTorch并直接在远程服务器上创建基本的docker镜像。我们用不同的支点表示图中的不同点。这些分行现在都在Zhihao的repo中，以后我们会把它们移到这个repo中。
# 5. Contact 联系

If you have any question, please contact `zbai1 at jhu dot edu`

> 如果您有任何问题，请联系“zbai1 at jhu dot edu” 

# 学习过程记录
## 路径添加
将以下代码追加到 ```/etc/profile``` 中，并执行```source /etc/profile```，**其中```/home/ctry/gitReg/PipeSwitch```需要更改为本地git 仓库的绝对路径。**
```
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/client/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/kill_restart/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/mps/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/pipeswitch/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/pytorch_plugin/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/ready_model/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/scripts/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/task/:$PYTHONPATH
export  PYTHONPATH=/home/ctry/gitReg/PipeSwitch/util/:$PYTHONPATH
```

## 根据端口查询任务
遇到某个端口被占用时，可以执行以下命令。
### 查询对应端口的信息，获取其PID
```
netstat -tunpl | grep 端口号
```
or 
```
lsof -i:端口号
```
### kill某进程
```
kill -9 PID 
```

## 尝试运行
### 执行步骤

> 1. 先执行kill_restart.py 文件，运行如下命令 ```python3.6 kill_restart.py```
> 2. 再执行client_inference.py文件，运行如下命令```python3.6 client_inference.py inception_v3 1```

其中，inception_v3、1 分别表示model_name 和 batch_size。


### 遇到如下问题
#### 问题1 执行client_inference.py失败
##### 问题描述
> (base) ctry@Ctry:~/gitReg/PipeSwitch$ python3.6 ./client/client_inference.py inception_v3 1
Traceback (most recent call last):
  File "./client/client_inference.py", line 7, in <module>
    from util.util import TcpClient, timestamp
ModuleNotFoundError: No module named 'util.util'; 'util' is not a package
##### 解决办法
> 将util.py 修改为utils.py即可。（<font color="red">为何能解决未知</font>）
#### 问题2 执行kill_restart.py失败
##### 问题描述
>Exception in thread Thread-2:
Traceback (most recent call last):
  File "/usr/lib/python3.6/threading.py", line 916, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.6/threading.py", line 864, in run
    self._target(*self._args, **self._kwargs)
  File "/home/ctry/gitReg/PipeSwitch/kill_restart/kill_restart.py", line 42, in func_schedule
    active_worker.kill()
AttributeError: 'Process' object has no attribute 'kill'
##### 解决办法 【待探究，后续可以在运行的容器中，执行命令，观察结果】
> 未知，待考究
#### 问题3 构建镜像时，无法git clone的问题
构建镜像时，出现无法git clone的问题，
##### 问题描述
执行```docker build -f Dockerfile-base -t pipeswitch:base .```出现以下错误：
>Sending build context to Docker daemon  6.656kB
Step 1/11 : FROM pytorch/pytorch:1.3-cuda10.1-cudnn7-devel
 ---> fe0f6ec79dbf
Step 2/11 : WORKDIR /workspace
 ---> Using cache
 ---> fe6604990671
Step 3/11 : RUN git clone --branch v1.3.0 https://github.com/pytorch/pytorch.git
 ---> Running in dcbad6097ca2
Cloning into 'pytorch'...
fatal: unable to access 'https://github.com/pytorch/pytorch.git/': gnutls_handshake() failed: The TLS connection was non-properly terminated.
The command '/bin/sh -c git clone --branch v1.3.0 https://github.com/pytorch/pytorch.git' returned a non-zero code: 128

##### 解决办法
在Dockerfile-base文件中添加git proxy设置。
```shell
RUN git config --global http.proxy socks5://地址:端口号
RUN git config --global https.proxy socks5://地址:端口号
```
然后再执行
```shell
docker build -f Dockerfile-base -t pipeswitch:base .
```
参数说明： 
  - -f 表示指定生成镜像的Dockerfile
  - -t 表示目标镜像，:base表示标签

#### 问题4 构建pipeswitch:pipeswitch 镜像时，出现问题
sudo docker build -f Dockerfile-pipeswitch -t pipeswitch:pipeswitch .
##### 问题描述
>Using cache found in /home/ctry/.cache/torch/hub/pytorch_vision_v0.4.2
Using cache found in /home/ctry/.cache/torch/hub/pytorch_vision_v0.4.2
Downloading: "https://github.com/huggingface/pytorch-transformers/archive/v2.5.0.zip" to /home/ctry/.cache/torch/hub/v2.5.0.zip
Traceback (most recent call last):
  File "../scripts/environment/container_download_models.py", line 8, in <module>
    main()
  File "../scripts/environment/container_download_models.py", line 5, in main
    get_model(model_name)
  File "/home/ctry/gitReg/PipeSwitch/task/helper.py", line 10, in get_model
    model = model_module.import_model()
  File "/home/ctry/gitReg/PipeSwitch/task/bert_base_inference.py", line 24, in import_model
    model = bert_base.import_model()
  File "/home/ctry/gitReg/PipeSwitch/task/bert_base.py", line 10, in import_model
    'bert-base-cased')
  File "/home/ctry/.local/lib/python3.6/site-packages/torch/hub.py", line 397, in load
    repo_or_dir = _get_cache_or_reload(repo_or_dir, force_reload, verbose, skip_validation)
  File "/home/ctry/.local/lib/python3.6/site-packages/torch/hub.py", line 192, in _get_cache_or_reload
    download_url_to_file(url, cached_file, progress=False)
  File "/home/ctry/.local/lib/python3.6/site-packages/torch/hub.py", line 452, in download_url_to_file
    u = urlopen(req)
  File "/usr/lib/python3.6/urllib/request.py", line 223, in urlopen
    return opener.open(url, data, timeout)
  File "/usr/lib/python3.6/urllib/request.py", line 532, in open
    response = meth(req, response)
  File "/usr/lib/python3.6/urllib/request.py", line 642, in http_response
    'http', request, response, code, msg, hdrs)
  File "/usr/lib/python3.6/urllib/request.py", line 564, in error
    result = self._call_chain(*args)
  File "/usr/lib/python3.6/urllib/request.py", line 504, in _call_chain
    result = func(*args)
  File "/usr/lib/python3.6/urllib/request.py", line 756, in http_error_302
    return self.parent.open(new, timeout=req.timeout)
  File "/usr/lib/python3.6/urllib/request.py", line 526, in open
    response = self._open(req, data)
  File "/usr/lib/python3.6/urllib/request.py", line 544, in _open
    '_open', req)
  File "/usr/lib/python3.6/urllib/request.py", line 504, in _call_chain
    result = func(*args)
  File "/usr/lib/python3.6/urllib/request.py", line 1368, in https_open
    context=self._context, check_hostname=self._check_hostname)
  File "/usr/lib/python3.6/urllib/request.py", line 1328, in do_open
    r = h.getresponse()
  File "/usr/lib/python3.6/http/client.py", line 1377, in getresponse
    response.begin()
  File "/usr/lib/python3.6/http/client.py", line 320, in begin
    version, status, reason = self._read_status()
  File "/usr/lib/python3.6/http/client.py", line 289, in _read_status
    raise RemoteDisconnected("Remote end closed connection without"
http.client.RemoteDisconnected: Remote end closed connection without response

##### 解决办法 
在dockfile_pipeswitch中添加git proxy的配置信息，并执行以下命令
```
sudo docker build -f Dockerfile-pipeswitch -t pipeswitch:pipeswitch . --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg https_proxy=$HTTPS_PROXY
```

##### 构造 mps镜像
执行以下命令
```
sudo docker build -f Dockerfile-mps -t pipeswitch:mps . --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg https_proxy=$HTTPS_PROXY
```
#### 构造ready_model镜像
执行以下命令
```
sudo docker build -f Dockerfile-ready_model -t pipeswitch:ready_model . --build-arg HTTP_PROXY=$HTTP_PROXY --build-arg http_proxy=$HTTP_PROXY --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg https_proxy=$HTTPS_PROXY
```
#### 清理所有创建失败的镜像
```
sudo docker stop $(sudo docker ps -aq)
sudo docker rm $(sudo docker ps -aq)
sudo docker rmi 创建失败的镜像的ID
```
#### 问题5 如何利用 构建的docker镜像，并运行
##### 执行过程
运行docker容器，使用GPU资源
```shell
sudo docker run --gpus all -it --name pipeswitch pipeswitch:pipeswitch
```
##### 遇到问题
>Error response from daemon: could not select device driver "" with capabilities: [[gpu]].
##### 解决办法
按照[博客](https://blog.csdn.net/BigData_Mining/article/details/104991349)的做法，执行安装nvidia-container-runtime，而后执行```systemctl restart docker```重启docker damon进程。

最后执行```sudo docker run --gpus all -it --rm --name pipeswitch pipeswitch:pipeswitch nvidia-smi```验证是否成功

如果成功显示类似如下的命令行界面
```(base) ctry@Ctry:~/gitReg/PipeSwitch/pipeswitch$ sudo docker run --gpus all -it --rm --name pipeswitch pipeswitch:pipeswitch nvidia-smi
Thu Jan 20 07:28:19 2022       
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 440.33.01    Driver Version: 440.33.01    CUDA Version: 10.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  GeForce GTX 1650    On   | 00000000:01:00.0 Off |                  N/A |
| N/A   42C    P8     5W /  N/A |    945MiB /  3911MiB |     13%      Default |
+-------------------------------+----------------------+----------------------+
                                                                               
+-----------------------------------------------------------------------------+
| Processes:                                                       GPU Memory |
|  GPU       PID   Type   Process name                             Usage      |
|=============================================================================|
+-----------------------------------------------------------------------------+

```