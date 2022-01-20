<!-- TOC -->

- [PipeSwitch](#pipeswitch)
- [Content](#content)
- [Environment](#environment)
- [Usage](#usage)

<!-- /TOC -->
# PipeSwitch
This folder contains code for PipeSwitch.
> 这个文件夹包含了pipeswitch的代码
# Content 
- main.py: Part of the controller and part of the memory management. It accepts connections from the client. It request the entrie GPU memory for the memory management. Besides, it creates threads and processes for other components.
  > 控制器和内存管理模块。接收来自客户端的连接请求，它为整个GPU内存进行内存管理；此外，它还为其他组件创建线程和进程。
- frontend_tcp.py: After main.py accepts connections from the client, this thread receives requests and send replies.
  > main.py接受客户端的连接后，该线程接收请求并发送响应。
- frontend_schedule.py: Part of the controller and part of the memory management. It instructs workers to activate or deactivate. It transfers model parameters to GPU.
  > 控制器和内存管理模块。指示worker激活或停用；将模型参数传递给GPU。
- worker.py: The workers of PipeSwitch. It is responsible for executing requests. Besides, it has some functions to handle preemption and pipeline, and cooperate with the memory management.
  > pipeswitch的worker。它负责执行请求。此外，它还具有一些处理抢占和流水线的功能，并配合内存管理模块。
- worker_common.py: An interface to manage models. It loads models structures into the CPU. It add hooks to layers to wait for the parameters for the pipeline. It also executes models.
  > 一个管理模型的接口。它将模型结构加载到CPU中。它在网络层上添加hook（钩子）来等待参数以实现流水线的机制；它还执行模型推理的工作。
- worker_terminate.py: Listen to the controller for signals for deactivate. Then it notifies the main thread of the worker to stop the current task.
  > 监听控制器的信号使其停止工作。然后它通知工作线程的主线程停止当前任务。

# Environment
To support PipeSwitch, we add some plugins into PyTorch. Thus, before running this demo, you need to compile PyTorch as stated in [PyTorch plugin](https://github.com/netx-repo/PipeSwitch/tree/main/pytorch_plugin).
Besides, you need to add the path to the repo to `PYTHONPATH`.
> 为了支持PipeSwitch，我们在PyTorch中添加了一些插件。因此，在运行这个demo之前，你需要按照[PyTorch plugin](https://github.com/netx-repo/PipeSwitch/tree/main/pytorch_plugin)的规定编译PyTorch。
此外，你需要将repo的路径添加到```PYTHONPATH```。
# Usage
```
python main.py model_list.txt
```
After starting the program, you need to wait for several seconds to allow it load required models.
> 在启动程序之后，需要等待几秒钟，因为程序加载所需的模型需要一定的时间。