# my_clock

一个适用于Windows系统的提醒休息计时器，使用Python + QT6

### 安装需求

```bash
# 推荐python版本3.11+
# 推荐在conda或venv等虚拟环境中运行
pip install -r requirements.txt
```

### 测试运行

- 在`config.py`中配置**当前文件夹绝对路径**

```bash
当前文件夹目录树如下：
│   aclock.ico # 图标文件
│   aclock.py # 主程序
│   config.py # 配置文件
│   requirements.txt # 依赖库
│   timer_widget.py # 计时器窗口
├───end # 休息提示音乐文件夹
├───start # 工作提示音乐文件夹
```

- 运行`aclock.py`

### 打包

```bash
# 推荐在conda或venv等虚拟环境中运行，否则可能导致打包过大。
# 推荐使用字母a开头的名称，若遇到问题，在任务管理器中可以轻松找到，并强制停止运行。
pyinstaller --name=aclock aclock.py -w -F -i aclock.ico
```

### 设置开机启动

- 打包好的exe文件在`dist`文件夹中`dist/aclock.exe`
- 为`aclock.exe`创建快捷方式，不要移动exe文件
- 将快捷方式复制入“启动”文件夹

在windows系统中，“启动”文件夹路径为：

``` bash
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

### 播放音乐

- 在`start`文件夹中放入工作提示音乐
- 在`end`文件夹中放入休息提示音乐
- 音乐文件格式为`.mp3`
