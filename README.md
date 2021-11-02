# kindle-clock
只是个一时兴起做的小东西，最大的特点是可以以`整, 一刻, 半, 三刻`的方式显示时间，降低了需要刷新的次数……就这样。

`constants.py`来自[wttr.in](https://github.com/chubin/wttr.in), 未作任何修改。

## DEMO

![kindle-monitor.png](https://test.yxyy.top/kindle-monitor.png)

为什么是反的？因为我推荐把kindle倒置以便于充电。

![](https://raw.githubusercontent.com/Xuyiyang23333/kindle-clock/main/%E5%AE%9E%E9%99%85%E6%95%88%E6%9E%9C.jpg)

实机演示。

## HOW TO USE?

### 普通用户
注: `/mnt/us/`其实就是连接电脑时显示的根目录。
1. 将你的Kindle越狱，并安装KUAL
2. 从[mobileread](https://www.mobileread.com/forums/showthread.php?t=225030)下载`FBInk`，选择你需要的版本并将内容物解压到/mnt/us/FBInk即可。（为什么不把FBInk也一起分发出来？因为这程序用了GPL，而我选了MIT……）
例：`压缩包/K5/* --> /mnt/us/FBInk/`（我的设备是Kindle PaperWhite 1, 故选择K5）
3. 下载该仓库内的`kindle-monitor`文件夹，放置到`/mnt/us/extensions`即可在KUAL菜单内启动。

## Geeks
1. Clone本仓库
2. `pip install PIL requeses feedparser qrcode`
3. 下载两份字体，放置到仓库目录下。一份应当有中文支持，另一份应当有Emoji支持。（推荐使用[霞鹜文楷](https://github.com/lxgw/LxgwWenKai)和![Twitter Color Emoji SVGinOT Font](https://github.com/eosrei/twemoji-color-font)）
4. 修改`kindle-monitor-pillow.py`中的`fontFile`和`emojiFontFile`变量。
5. `python kindle-monitor-pillow.py`
6. 将同一目录下生成的`kindle-monitor.png`拷贝至web服务器的目录下。
7. 修改`kindle-monitor/run.sh`中的`uri`变量。

# License
[Apache License 2.0](https://github.com/chubin/wttr.in/blob/master/LICENSE)
[MIT License](https://github.com/Xuyiyang23333/kindle-clock/blob/main/LICENSE)
