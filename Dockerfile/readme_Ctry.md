- Dockerfile-base:
  - 编译原生pytorch。
- Dockerfile-mps:
  - 基于原生的pytorch，执行''' overwrite.sh /workspace/pytorch/ '''，替换'''CUDACachingAllocator.cpp'''文件，将其中的cudaMalloc替换成cudaMallocManaged。
- Dockerfile-pipeswitch:
  - 基于原生的pytorch替换了以下几个函数
    1. $PYTORCH_PATH/torch/cuda/__init__.py
    2. $PYTORCH_PATH/torch/csrc/cuda/Module.cpp
    3. $PYTORCH_PATH/c10/cuda/CUDACachingAllocator.h
    4. $PYTORCH_PATH/c10/cuda/CUDACachingAllocator.cpp
- <font color="red">疑问：</font>$Dockerfile-ready\_model$ 与 $Dockerfile-pipeswitch$ 有什么区别，$Dockerfile-ready\_model$仅扮演一个提供模型的worker角色？