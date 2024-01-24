# my_clock
一个提醒休息的计时器

### 安装需求

```bash
# 推荐python版本3.7+
# 推荐在conda或venv等虚拟环境中运行
pip install -r requirements.txt
```

### 测试运行

- 运行aclock.py

### 打包

```bash
# 推荐在conda或venv等虚拟环境中运行，否则可能导致打包过大。
# 推荐使用字母a开头的名称，若遇到问题，在任务管理器中可以轻松找到，并强制停止运行。
pyinstaller --name=aclock aclock.py -w -F # -i aclock.ico # （可选）定制图标
```

### 设置开机启动

```
# 为打包好的exe文件创建快捷方式
# 将快捷方式复制入“启动”文件夹
# 在windows系统中，路径大致为：
%USERPROFILE%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
```

