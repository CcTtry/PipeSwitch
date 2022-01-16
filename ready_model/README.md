# Ready model
This folder contains code for ready-model.
> 这个文件夹包含了现成（准备就绪的）模型的代码
# Environment
You need to add the path to the repo to `PYTHONPATH`.
> 你需要将ready-model的路径添加到```PYTHONPATH```中。例如，添加到/etc/profile 中。

```shell
echo "export  PYTHONPATH=XX/PipeSwitch/ready_model/:$PYTHONPATH" >> /etc/profile
```




# Ussage 使用方法
```
python ready_model.py [model_name]
```
`model_name` can be `resnet152`, `inception_v3` or `bert_base`.

For example:
```
python ready_model.py resnet152
```