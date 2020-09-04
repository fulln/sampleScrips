 ### 分页查询helper

[AbstractQueryHelper](./AbstractQueryHelper.java)


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
















