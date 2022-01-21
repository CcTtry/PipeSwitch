本包实现了mps的相关功能，修改了pytorch的相关```.cpp```文件其中的**```cuda_malloc_retry```函数**
-> ```/pytorch/pytorch/v1.3.0/c10/cuda/CUDACachingAllocator.cpp```

具体修改的代码如下所示：
未修改的```CUDACachingAllocator.cpp```文件如下

```C++
cudaError_t cuda_malloc_retry(int device, void** devPtr, size_t size)
  {
    // Try cudaMalloc. If cudaMalloc fails, frees all non-split cached blocks
    // and retries.
    cudaError_t err = cudaMalloc(devPtr, size);
    if (err != cudaSuccess) {
      cudaGetLastError();  // reset the last CUDA error
      free_cached_blocks(device);
      err = cudaMalloc(devPtr, size);
      if (err != cudaSuccess) {
        return err;
      }
    }
    return cudaSuccess;
  }
```
修改过后的```CUDACachingAllocator.cpp```文件如下:
```C++
cudaError_t cuda_malloc_retry(int device, void** devPtr, size_t size)
  {
    // Try cudaMalloc. If cudaMalloc fails, frees all non-split cached blocks
    // and retries.
    cudaError_t err = cudaMallocManaged(devPtr, size);
    if (err != cudaSuccess) {
      cudaGetLastError();  // reset the last CUDA error
      free_cached_blocks(device);
      err = cudaMallocManaged(devPtr, size);
      if (err != cudaSuccess) {
        return err;
      }
    }
    return cudaSuccess;
  }
```