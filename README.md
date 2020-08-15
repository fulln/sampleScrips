# sampleScrips
目前搜罗到的一些简单有效的py脚本orgolang再实现版本

<!-- toc -->
<!-- tocstop -->

## hlsVideoDownload

[hls_video_download](./hls) 目的是用来下载一个在线播放的视频网站的流信息，并通过ffmpeg重新组装成mp4格式.这个想法是我在群里看到一个群友提供了一个ts下载脚本,于是我想写得更加通用点，但是可惜[目前版本](./hls/ts_download_v5.py)只能很有限的支持一些简单场景和网站。我也在尝试加密的版本的适用和链中链情况的使用。如果你有更通用的版本或者有更加好的想法欢迎pr

## Alfred_ywz

[Alfred_ywz](./Alfred_ywz)  一个颜文字的工作流，之前的颜文字流竟然不能使用了,于是简单的写了一个,目前收录的只有<a>http://www.yanwenzi.com/</a>中的相关分类（其实就是从这个网站上爬下来的）

**ywz使用方式**

1. 加载workflow,从<a>https://github.com/fulln/sampleScrips/releases/tag</a> 上下载最新的版本
2. 打开alfred搜索栏
3. 输入`moji` + 你想要搜的颜文字分类（注意打拼音)</br>
  3.1 如果你输入的是少于2个字符的情况，目录会自动展示，但是还是需要你手动输入下目录的前面几个拼音</br>
  3.2 如果输入的时候是“-”开头 ，则意味着从所有已存在的颜文字中查询对应有中文意思的颜文字</br>
  3.3 如果输入的时候 只输入“-” 则会展示所有的颜文字（大小36K）</br>

> 目前收录的分类有
> 'kaixin', 'daoqian', 'teshu', 'jieri', 'meishi', 'liuyanlei', 'haipa', 'shangxin', 'dazhaohu', 'thangzhou', 'haixiu', 'yun', 'biaoqing', 'mofa', 'keai', 'tanshou', 'hua', 'xingxing', 'changyong', 'zan', 'liulei', 'xiazhuozi', 'ku', 'dalian', 'zhenjing', 'chouyan', 'ganbei', 'jian', 'bingchang', 'shuijue', 'benpao', 'test.py', 'chihuo', 'memeda', 'aixin', 'xiaozhu', 'yiwen', 'xiezi', 'gouxiong', 'liukoushui', 'niao', 'wunai', 'miaozhao', 'jiayou', 'jingli', 'dongwu', 'xinqing', 'duocang', 'zhaoshou', 'shengqi', 'wuqi', 'miaomai', 'pengyou', 'yu', 'nvhai', 'deyi', 'dongzuo', 'huaiyi', 'shuila', 'jingya', 'zaijian', 'aojiao', 'qita', 'tianqi', 'tiaowu', 'yinle', 'daothang', 'gou', 'yundong', 'jiong', 'maimeng', 'sikao', 'nanguo', 'ganga', 'gaoxing', 'laonianren', 'qinwen'


4. **找到你想要的颜文字，并按enter**  

## AbstractQueryHelper
[AbstractQueryHelper](./AbstractQueryHelper)


> 一个避免oom的导出下载帮助java类

导出查询的问题基本上在2点

1. 查询效率，导出查询有时候总量直接上百万，上千万
2. OOM问题，还是由于总量上升导致的内存消耗过大的问题

在需要大量导出的环境种，一般导出的功能不会跟随项目，而是有个导出项目专门负责异步导出，而导出的功能一般还会结合redis或者hadoop来进行中心化处理，
这样就能将大量io的场景集中在某一集群上面，从而集中进行优化和处理。

以下是几种方式的优缺点分析

<table aline='center'>
<tr>
<td  valign="top">\</td>
<td  valign="top">redis</td>
<td  valign="top">hadoop</td>
<td  valign="top">原项目导出</td>
</tr>
<tr>
<td  valign="top">优点</td><td  valign="top">
	
* 在分布式服务中方便集中进行导出的处理
* 实现异步的导出控制

</td>
<td  valign="top">
	
* 实现异步导出控制
* io对服务器性能影响不大
* 不占用原服务器的io

</td>
<td  valign="top">
	
* 维护方便
* 实现简单

</td>
</tr>
<tr>
<td>缺点</td>
<td  valign="top">
	
* 不能避免OOM
* 数据容易被串改操作
* 敏感数据容易被暴露
* 大量数据容易对redis的造成负担

</td>
<td  valign="top">
	
* 对高性能服务器的一个浪费
* 一般hadoop服务器由大数据维护,增加了对数据的维护
* 同样有文件安全的问题
* OOM的风险

</td>
<td  valign="top">
	
* 不能异步导出或者较难异步导出
* 高IO对原服务器上其他服务接口造成影响
* OOM

</td>
</tr>
</table>

本工具类就是为了避免上面的统一的OOM缺点而写的，市面上又已经有了如easyexcel等工具包进行导出的服务，这些工具类大部分也是有了避免OOM的功能，所以在[开头](#AbstractQueryHelper)我就提出了2个点，于是我将这2个点都进行了部分的优化

1. 查询优化

查询条件填充，如果原来的查询条件包含了时间or主键相关的条件,那么就可以将条件散列为list，然后遍历list条件进行查询，如时间条件散列为每2天一组的时间参数,从而降低范围查询中总条数，然后在这每2天的时间内再进行分页的查询，这样变相的降低了深翻页的深度，从而达到查询的优化的目的 PS:这个2天的时间间隔是可以改变的

2. OOM问题

本质上是每隔多少条数据就进行一个写入文件并释放内存的操作，我这边实现的是查询部分的每隔多少条记录就进行一次释放内存的操作
```java

do {
				try {
					currentList.clear();
					currentList = doQuery(getPrototypeObj(obj, pages));
					//判断要是达到了默认的size大小，就开始写入到excel里面
					if (parallelList.size() > getDefaultExportListSize()) {
						getExportDataListToExcelList(parallelList);
						setTotalCount(parallelList.size());
						//清空
						parallelList.clear();
					}
					parallelList.addAll(currentList);
					if (pages.getId() != null) {
						pages.setId(pages.getId() + pages.getPageSize());
					} else {
						pages.setPageNo(pages.getPageNo() + 1);
					}
				} catch (Exception e) {
					log.error("query happened exception ", e);
				}
			}
			while (!CollectionUtils.isEmpty(currentList));

```

具体的写入excel的 `getExportDataListToExcelList` 这个方法是交给用户自主实现。poi包中可以通过SXXSF进行操作避免OOM,目前市面上比较推荐的excel操作包是 `easyexcel`，也可以避免OOM

### 使用步骤

- 将[该文件](./abstractExportHelper/AbstractQueryHelper.java)放到你所在的工具类中
- 在需要使用到的地方

```java
 AbstractQueryHelper<String> abstractQueryHelper = new AbstractQueryHelper<String>() {
            @Override
            public List doQuery(String s) {
                 return null;
            }

            @Override
            protected void getExportDataListToExcelList(List parallelList) {
//自主实现将list存入excel
                 return ;
            }
        };
//最后剩余的list也要注意存入excel
        abstractQueryHelper.startQueryProcess();
//这个可以获取到总条数
        abstractQueryHelper.getTotalCount();
```

## ssh登录脚本

采用了expect 脚本流程控制 ，用于多ip登录时查询对应ip的日志，免去了要手动输入完整ip 和 密码的烦恼，特别适用于容器服务器日志查询，如果需要其他操作可以自行加spawn




