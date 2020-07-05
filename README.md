# sampleScrips
目前搜罗到的一些简单有效的py脚本orgolang再实现版本

## hlsVideoDownload

[hls_video_download](./hls) 目的是用来下载一个在线播放的视频网站的流信息，并通过ffmpeg重新组装成mp4格式.这个想法是我在群里看到一个群友提供了一个ts下载脚本,于是我想写得更加通用点，但是可惜[目前版本](./hls/ts_download_v5.py)只能很有限的支持一些简单场景和网站。我也在尝试加密的版本的适用和链中链情况的使用。如果你有更通用的版本或者有更加好的想法欢迎pr

## Alfred_ywz

[Alfred_ywz](./Alfred_ywz)  一个颜文字的工作流，之前的颜文字流竟然不能使用了,于是简单的写了一个,目前收录的只有<a>http://www.yanwenzi.com/</a>中的相关分类（其实就是从这个网站上爬下来的）

**ywz使用方式**

1. 加载workflow,从<a>https://github.com/fulln/sampleScrips/releases/tag</a> 上下载最新的版本
2. 打开alfred搜索栏
3. 输入`moji` + 你想要搜的颜文字分类（注意打拼音)
  3.1 如果你输入的是少于2个字符的情况，目录会自动展示，但是还是需要你手动输入下目录的前面几个拼音
  3.2 如果输入的时候是“-”开头 ，则意味着从所有已存在的颜文字中查询对应有中文意思的颜文字
  3.3 如果输入的时候 只输入“-” 则会展示所有的颜文字（大小36K）

> 目前收录的分类有
> 'kaixin', 'daoqian', 'teshu', 'jieri', 'meishi', 'liuyanlei', 'haipa', 'shangxin', 'dazhaohu', 'thangzhou', 'haixiu', 'yun', 'biaoqing', 'mofa', 'keai', 'tanshou', 'hua', 'xingxing', 'changyong', 'zan', 'liulei', 'xiazhuozi', 'ku', 'dalian', 'zhenjing', 'chouyan', 'ganbei', 'jian', 'bingchang', 'shuijue', 'benpao', 'test.py', 'chihuo', 'memeda', 'aixin', 'xiaozhu', 'yiwen', 'xiezi', 'gouxiong', 'liukoushui', 'niao', 'wunai', 'miaozhao', 'jiayou', 'jingli', 'dongwu', 'xinqing', 'duocang', 'zhaoshou', 'shengqi', 'wuqi', 'miaomai', 'pengyou', 'yu', 'nvhai', 'deyi', 'dongzuo', 'huaiyi', 'shuila', 'jingya', 'zaijian', 'aojiao', 'qita', 'tianqi', 'tiaowu', 'yinle', 'daothang', 'gou', 'yundong', 'jiong', 'maimeng', 'sikao', 'nanguo', 'ganga', 'gaoxing', 'laonianren', 'qinwen'


4. 找到你想要的颜文字，并按enter


