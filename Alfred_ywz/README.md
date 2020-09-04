
## Alfred_ywz

[Alfred_ywz](./Alfred_ywz)  一个颜文字的工作流，之前的颜文字流竟然不能使用了,于是简单的写了一个

### 初始化

目前该workflow 使用了`sqlLite`数据库作为存储工具。在`MacOs`中是自带了sqlLite的数据库的(所有的linux的服务器都自带)。
> 输入 `sqlLite3 -version` 可以看到sqlLite数据库自带的信息

针对不同的网址，有不同的爬取方式和需要选定不同的元素，所以这里有提供多个`ywz*.py`的脚本,目前比较常用的我都爬取了下来，放到了对应JSON文件中，
如果你还有需要其他网站中的颜文字，可以自行去修改。

下面是初始化的步骤

* 加载workflow,从<a>https://github.com/fulln/sampleScrips/releases/tag</a> 上下载最新的颜文字workflow版本
* 唤出Alfred搜索栏并输入moji 

> 如果你想要更准确的常用颜文字推荐，输入`moji init` 将当前的所有颜文字json加载到sqlLite中,这样使用的性能更好，而且推荐的颜文字更加准确

### 使用

- 输入`moji` + 你想要搜的颜文字分类（注意打拼音)</br>
  - 如果你输入的是少于2个字符的情况，目录会自动展示，但是还是需要你手动输入下目录的前面几个拼音</br>
  - 如果输入的时候是“-”开头 ，则意味着从所有已存在的颜文字中查询对应有中文意思的颜文字</br>
  - 如果输入的时候 只输入“-” 则会展示所有的颜文字（大小36K）</br>

> 目前收录的分类有
> 'kaixin', 'daoqian', 'teshu', 'jieri', 'meishi', 'liuyanlei', 'haipa', 'shangxin', 'dazhaohu', 'thangzhou', 'haixiu', 'yun', 'biaoqing', 'mofa', 'keai', 'tanshou', 'hua', 'xingxing', 'changyong', 'zan', 'liulei', 'xiazhuozi', 'ku', 'dalian', 'zhenjing', 'chouyan', 'ganbei', 'jian', 'bingchang', 'shuijue', 'benpao', 'test.py', 'chihuo', 'memeda', 'aixin', 'xiaozhu', 'yiwen', 'xiezi', 'gouxiong', 'liukoushui', 'niao', 'wunai', 'miaozhao', 'jiayou', 'jingli', 'dongwu', 'xinqing', 'duocang', 'zhaoshou', 'shengqi', 'wuqi', 'miaomai', 'pengyou', 'yu', 'nvhai', 'deyi', 'dongzuo', 'huaiyi', 'shuila', 'jingya', 'zaijian', 'aojiao', 'qita', 'tianqi', 'tiaowu', 'yinle', 'daothang', 'gou', 'yundong', 'jiong', 'maimeng', 'sikao', 'nanguo', 'ganga', 'gaoxing', 'laonianren', 'qinwen'


- **找到你想要的颜文字，并按enter**  

