# PyTorch plugins
This folder contains modifications to the PyTorch code.
此文件夹包含对PyTorch代码的修改。
# Content
- PyTorch files
    - \_\_init\_\_.py: $PYTORCH_PATH/torch/cuda/\_\_init\_\_.py
    - Module.cpp: $PYTORCH_PATH/torch/csrc/cuda/Module.cpp
    - CUDACachingAllocator.cpp: $PYTORCH_PATH/c10/cuda/CUDACachingAllocator.cpp
    - CUDACachingAllocator.h: $PYTORCH_PATH/c10/cuda/CUDACachingAllocator.h
- overwrite.sh: Overwrite corresponding files in $PYTORCH_PATH

# Usage
1. Compile the original PyTorch (1.3.0) from source. https://github.com/pytorch/pytorch/tree/v1.3.0.
   > 从源代码编译原始的PyTorch(1.3.0)。https://github.com/pytorch/pytorch/tree/v1.3.0。
2. Copy modified files to the PyTorch folder. `bash overwrite.sh [path_to_PyTorch]`
   > 将修改后的文件复制到PyTorch文件夹。`bash overwrite.sh [path_to_PyTorch]`
3. Compile the modified PyTorch. Then you may install it to Python library folder or set `PYTHONPATH` to make sure that PipeSwitch can find it.
    > 编译修改后的PyTorch。然后你可以将它安装到Python库文件夹中，或者设置`PYTHONPATH`以确保PipeSwitch能找到它。
# Implementation
All the modified functions are labeled with a comment of "PipeSwitch" around them.
> 所有修改过的函数都用"PipeSwitch"注释标记。

The code is implemented for NVIDIA V100 and T4, both of which have 16 GB GPU memory. Thus, some related parameters for memory management are directly written in the code. If you use GPUs with different GPU memory size, you need to change these parameters.
> 该代码是在NVIDIA V100和T4上实现的，这两个版本都有16gb的GPU显存。因此，内存管理的一些相关参数被直接写入代码中。<font color="red">如果使用不同GPU内存大小的GPU，则需要修改这些参数。</font>

There are some printed message for debug. You can comment them if needed.
> 有一些用于调试的打印信息。如果需要，可以把他们注释掉