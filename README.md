# my_clock

一个适用于Windows系统的提醒休息计时器，使用Python + QT6

### 安装需求

```bash
# 推荐python版本3.11+
# 推荐在conda或venv等虚拟环境中运行
pip install -r requirements.txt
```

### 测试运行

- 在`config.py`中配置绝对路径
- 运行`aclock.py`

### 打包

```bash
# 推荐在conda或venv等虚拟环境中运行，否则可能导致打包过大。
# 推荐使用字母a开头的名称，若遇到问题，在任务管理器中可以轻松找到，并强制停止运行。
pyinstaller --name=aclock aclock.py -w -F -i aclock.ico
```

### 设置开机启动

``` bash
# 为打包好的exe文件创建快捷方式
# 将快捷方式复制入“启动”文件夹
# 在windows系统中，路径大致为：
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

