### 操作步骤 

首先在**能联网**的机器安装 docker，并 pull 想要安装的镜像，完成后，使用 `docker save` 命令导出镜像：

```bash
# 将 java:8 的镜像导出成 tar 文件
# java:8 为镜像名
docker save java:8 -o java.tar  
```

导出后将 tar 文件上传到需要安装的 docker 服务器，使用如下命令导入镜像文件：

```bash
docker load -i java.tar
```

查看导入的镜像文件：

```bash
$ docker images
REPOSITORY                                             TAG                 IMAGE ID            CREATED             SIZE
java                                                   8                   d23bdf5b1b1b        3 years ago         643MB
```

1. 配置连接器，连接器可以使用如下配置

    ```json
    {
        "name": "inventory-connector",
        "config": {
            "database.user": "${file:/secrets/mysql.properties:user}",
            "database.password": "${file:/secrets/mysql.properties:password}",
            ...
        }
    }
    ```

* **column**

    * 描述：目的表需要写入数据的字段，字段 c 之间用英文逗号分隔。例如: "column": ["id","name","age"]。如果要依次写入全部列，使用 `*` 表示，例如:`"column": ["*"]`。

            **column 配置项必须指定，不能留空！**


dockerfile 配置：

```bash
RUN sed -i 's/apt.p/apt-archive.p/g' /etc/apt/sources.list.d/pgdg.list
```

请使用`function_call(param1, param2)` 来调用函数。


### 常见问题

#### open .../json: no such file or directory

出现该异常可能为：

1. 文件在传输过程中损坏
2. 文件使用 `docker export` 打包，但是使用了 `docker load` 加载包，对于这种情况，使用 `docker import <文件名>` 命令加载打包的文件即可。


### 参考

1. [docker save 与 docker export 的区别 - jingsam](https://jingsam.github.io/2017/08/26/docker-save-and-docker-export.html#你好)
