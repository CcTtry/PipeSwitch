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

具体修改内容
1. CUDACachingAllocator.cpp
该文件主要添加了以下一些方法
```C++
/* PipeSwitch: allocate shared GPU memory */
void allocateSharedCache(void) {
  caching_allocator.allocateSharedCache();
}

/* PipeSwitch: send shared GPU memory */
void sendSharedCache(void) {
  caching_allocator.sendSharedCache();
}

/* PipeSwitch: recv shared GPU memory */
void recvSharedCache(void) {
  caching_allocator.recvSharedCache();
}

/* PipeSwitch: insert shared GPU memory to large block pool */
void insertSharedCache(size_t size, size_t offset) {
    caching_allocator.insertSharedCache(size, offset);
}

/* PipeSwitch: clear shared GPU memory */
void clearSharedCache(void) {
  caching_allocator.clearSharedCache();
}
```
2. CUDACachingAllocato.h
该文件，相比于pytorch的原生文件，<font color="red">添加了几个函数的声明</font>
```C++
C10_CUDA_API void allocateSharedCache(); // PipeSwitch
C10_CUDA_API void sendSharedCache(); // PipeSwitch
C10_CUDA_API void recvSharedCache(); // PipeSwitch
C10_CUDA_API void insertSharedCache(size_t size, size_t offset); // PipeSwitch
C10_CUDA_API void clearSharedCache(); // PipeSwitch
```
3. pytorch_Module.cpp
该文件增添了以下几个函数的声明
```C++
PyObject * THCPModule_allocateSharedCache(PyObject *_unused, PyObject *noargs)
{
  HANDLE_TH_ERRORS
  c10::cuda::CUDACachingAllocator::allocateSharedCache();
  END_HANDLE_TH_ERRORS
  Py_RETURN_NONE;
}

// PipeSwitch
PyObject * THCPModule_sendSharedCache(PyObject *_unused, PyObject *noargs)
{
  HANDLE_TH_ERRORS
  c10::cuda::CUDACachingAllocator::sendSharedCache();
  END_HANDLE_TH_ERRORS
  Py_RETURN_NONE;
}

// PipeSwitch
PyObject * THCPModule_recvSharedCache(PyObject *_unused, PyObject *noargs)
{
  HANDLE_TH_ERRORS
  c10::cuda::CUDACachingAllocator::recvSharedCache();
  END_HANDLE_TH_ERRORS
  Py_RETURN_NONE;
}

// PipeSwitch
PyObject * THCPModule_insertSharedCacheForParameter(PyObject *_unused, PyObject *noargs)
{
  HANDLE_TH_ERRORS
      c10::cuda::CUDACachingAllocator::insertSharedCache(1UL * 1024UL * 1024UL * 1024UL, 0);
  END_HANDLE_TH_ERRORS
  Py_RETURN_NONE;
}

// PipeSwitch
PyObject * THCPModule_insertSharedCacheForComputation(PyObject *_unused, PyObject *noargs)
{
  HANDLE_TH_ERRORS
      c10::cuda::CUDACachingAllocator::insertSharedCache(11UL * 1024UL * 1024UL * 1024UL, 1UL * 1024UL * 1024UL * 1024UL);
  END_HANDLE_TH_ERRORS
  Py_RETURN_NONE;
}

// PipeSwitch
PyObject * THCPModule_clearSharedCache(PyObject *_unused, PyObject *noargs)
{
  HANDLE_TH_ERRORS
  c10::cuda::CUDACachingAllocator::clearSharedCache();
  END_HANDLE_TH_ERRORS
  Py_RETURN_NONE;
}
```
4. __init__.py
该文件对比pytorch 源文件有以下修改:(添加了几个函数)
```c
# PipeSwitch
def allocate_shared_cache():
    if _initialized:
        torch._C._cuda_allocateSharedCache()

# PipeSwitch
def send_shared_cache():
    if _initialized:
        torch._C._cuda_sendSharedCache()

# PipeSwitch
def recv_shared_cache():
    if _initialized:
        torch._C._cuda_recvSharedCache()

# PipeSwitch
def insert_shared_cache_for_parameter():
    if _initialized:
        torch._C._cuda_insertSharedCacheForParameter()

# PipeSwitch
def insert_shared_cache_for_computation():
    if _initialized:
        torch._C._cuda_insertSharedCacheForComputation()

# PipeSwitch
def clear_shared_cache():
    if _initialized:
        torch._C._cuda_clearSharedCache()
```