# sampleScrips
目前搜罗到的一些简单有效的py脚本orgolang再实现版本

## hlsVideoDownload

[hls_video_download](./hls) 目的是用来下载一个在线播放的视频网站的流信息，并通过ffmpeg重新组装成mp4格式.这个想法是我在群里看到一个群友提供了一个ts下载脚本,于是我想写得更加通用点，但是可惜[目前版本](./hls/ts_download_v5.py)只能很有限的支持一些简单场景和网站。我也在尝试加密的版本的适用和链中链情况的使用。如果你有更通用的版本或者有更加好的想法欢迎pr

## Alfred_ywz

[Alfred_ywz](./Alfred_ywz)  一个颜文字的工作流，之前的颜文字流竟然不能使用了,于是简单的写了一个,目前收录的只有<a>http://www.yanwenzi.com/</a>中的相关分类（其实就是从这个网站上爬下来的）

**ywz使用方式**

1. 加载workflow,从<a>https://github.com/fulln/sampleScrips/releases/tag</a> 上下载最新的版本
2. 打开alfred搜索栏
3. 输入`moji` + 你想要搜的颜文字分类（注意打拼音),你输入其他的是没有办法找到对应的

> 目前收录的分类有
> 'changyong', 'gaoxing', 'maimeng', 'zhenjing', 'shengqi', 'wunai', 'yun', 'daoqian', 'dongwu', 'haixiu', 'ku', 'memeda', 'shuila', 'zaijian', 'aojiao', 'chihuo', 'deyi', 'haipa', 'jiong', 'zan', 'nanguo', 'jian', 'qita'

4. 找到你想要的颜文字，并按enter


