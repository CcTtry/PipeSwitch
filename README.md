<!-- TOC -->

- [说明](#说明)
- [1. Introduction 引言](#1-introduction-引言)
- [2. Contents 内容](#2-contents-内容)
- [3. Brief usage  简要用法](#3-brief-usage--简要用法)
- [4. Scripts to reproduce figures in our paper. 复现我们论文中的数据的脚本](#4-scripts-to-reproduce-figures-in-our-paper-复现我们论文中的数据的脚本)
- [5. Contact 联系](#5-contact-联系)

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