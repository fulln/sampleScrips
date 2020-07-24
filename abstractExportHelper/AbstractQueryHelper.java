package com.fulln.me.api.common.utils;

import lombok.Data;
import lombok.Getter;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.util.CollectionUtils;
import org.springframework.util.ReflectionUtils;

import javax.validation.ConstraintViolation;
import javax.validation.Validation;
import javax.validation.Validator;
import javax.validation.ValidatorFactory;
import java.io.Serializable;
import java.lang.reflect.Field;
import java.lang.reflect.ParameterizedType;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.time.temporal.ChronoField;
import java.time.temporal.ChronoUnit;
import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

/**
 * @author fulln
 * @description 指定字段(如 id,时间)分区进行查询，尽量避免深翻页的问题
 *
 * @date Created in  19:22  2020-05-12.
 */
@Slf4j
@Data
public abstract class AbstractQueryHelper<T extends Serializable> {
	/**
	 * 默认查询的时间间隔
	 */
	private Integer defaultDateInterval =2;
	/**
	 * 当前查询的总条数
	 */
	private Integer totalCount = 0;
	/**
	 * 为查询做准备
	 */
	public List<ExportPageInfo> pageInfoList = new ArrayList<>();
	/**
	 * 传入的基本参数
	 */
	ExportTotalInfo totalInfo = setQueryTotalInfo();
	/**
	 * 需要使用原型复制
	 */
	T obj;
	/**
	 * 传入的class
	 */
	Class<T> clazz = getTClass();
	/**
	 * 默认的导出大小限制
	 */
	private int defaultExportListSize = 2000;
	/**
	 * 查询出来的结果
	 */
	private List parallelList = new ArrayList();

	/**
	 * info的初始化
	 * 参数的初始化
	 * @return
	 */
	public  ExportTotalInfo setQueryTotalInfo(){
		return  new ExportTotalInfo();
	};


	/**
	 * 自定义查询
	 *
	 * @param t 泛型参数
	 * @return
	 */
	public abstract List doQuery(T t);

	/**
	 * 设置查询的总条数
	 */
	public void setTotalCount(Integer total){
		this.totalCount = total;
	}
	/**
	 * 参数的初始化
	 *
	 * @param t 需要进行查询的参数
	 * @return
	 */
	public AbstractQueryHelper(T t) {
		//参数检查
		checkPageParams(t);
		obj = t;
		//初始化所有时间
		handleJobs(totalInfo);
	}

	/**
	 * 获取parallelList的值进行excel的填充
	 * @param parallelList
	 */
	protected void getExportDataListToExcelList(List parallelList) {
		//在这个地方去获取parallelList的值进行excel的填充
		//需要分页的时候
		throw new RuntimeException("请重写该方法以根据分页获取的结果进行excel的填充");
	}

	private void checkPageParams(T t) {
		// fastFail
		ValidatorFactory factory = Validation.buildDefaultValidatorFactory();

		Validator validator = factory.getValidator();

		Set<ConstraintViolation<ExportTotalInfo>> validate = validator.validate(totalInfo);
		if (validate.stream().findAny().isPresent()) {
			throw new IllegalArgumentException("参数异常");
		}
	}


	@SuppressWarnings("unchecked")
	private Class<T> getTClass() {
		return (Class<T>) ((ParameterizedType) getClass().getGenericSuperclass()).getActualTypeArguments()[0];
	}

	/**
	 * 使用json复制 并 修改对应的值
	 *
	 * @param t
	 * @return
	 */
	public T getPrototypeObj(T t, ExportPageInfo info) {
		String s = GsonUtil.gsonString(t);
		T o = GsonUtil.gsonToBean(s, clazz);

		//单页参数
		Field pageSize = ReflectionUtils.findField(clazz, totalInfo.getPageSizeFiled(), Integer.class);
		if (!Objects.isNull(pageSize)) {
			pageSize.setAccessible(true);
			ReflectionUtils.setField(pageSize, o, info.getPageSize());
		} else {
			throw new RuntimeException("不能获取到对应设置的字段");
		}

		//id
		if (info.getId() != null) {
			Field idField = ReflectionUtils.findField(clazz, totalInfo.getIdFiled(), Long.class);
			if (!Objects.isNull(idField)) {
				idField.setAccessible(true);
				ReflectionUtils.setField(idField, o, info.getId());
			} else {
				idField = ReflectionUtils.findField(clazz, totalInfo.getIdFiled(), Integer.class);
				if (!Objects.isNull(idField)) {
					idField.setAccessible(true);
					ReflectionUtils.setField(idField, o, info.getId().intValue());
				} else {
					throw new RuntimeException("不能获取到对应设置的字段");
				}
			}
			return o;
		}


		//开始时间
		Field startField = ReflectionUtils.findField(clazz, totalInfo.getStartTimeFiled(), String.class);
		if (!Objects.isNull(startField)) {
			startField.setAccessible(true);
			ReflectionUtils.setField(startField, o, SimpleDateUtils.formatDate(info.getStartDate()));
		} else {
			startField = ReflectionUtils.findField(clazz, totalInfo.getStartTimeFiled(), Date.class);
			if (!Objects.isNull(startField)) {
				startField.setAccessible(true);
				ReflectionUtils.setField(startField, o, info.getStartDate());
			} else {
				throw new RuntimeException("不能获取到对应设置的字段");
			}
		}
		//结束时间
		Field endField = ReflectionUtils.findField(clazz, totalInfo.getEndTimeFiled(), String.class);
		if (!Objects.isNull(endField)) {
			endField.setAccessible(true);
			ReflectionUtils.setField(endField, o, SimpleDateUtils.formatDate(info.getEndDate()));
		} else {
			endField = ReflectionUtils.findField(clazz, totalInfo.getEndTimeFiled(), Date.class);
			if (!Objects.isNull(endField)) {
				endField.setAccessible(true);
				ReflectionUtils.setField(endField, o, info.getEndDate());
			} else {
				throw new RuntimeException("不能获取到对应设置的字段");
			}
		}
		//页码参数
		if (totalInfo.pageable) {
			Field pageNoField = ReflectionUtils.findField(clazz, totalInfo.getPageNoFiled(), Integer.class);
			if (!Objects.isNull(pageNoField)) {
				pageNoField.setAccessible(true);
				ReflectionUtils.setField(pageNoField, o, info.getPageNo());
			} else {
				throw new RuntimeException("不能获取到对应的字段");
			}
		}


		return o;
	}


	/**
	 * 初始化流程
	 */
	private void handleJobs(ExportTotalInfo info) {
		//0. 首先判断传入的是id还是时间
		if (info.getId() != null) {
			ExportPageInfo pageInfo = new ExportPageInfo();
			pageInfo.setId(info.getId());
			pageInfoList.add(pageInfo);
			return;
		}
		//1.得到初始化的时间间隔
		LocalDateTime startDateTime = SimpleDateUtils.changeDate(info.getTotalStartTime());
		LocalDateTime endDateTime = SimpleDateUtils.changeDate(info.getTotalEndTime());
		int timeInterval = (int) ChronoUnit.DAYS.between(startDateTime, endDateTime);
		//2.得到所有的开始，结束的参数
		int cycleSize = (timeInterval + (timeInterval & 1)) / getDefaultDateInterval();
		//3.从开始时间到结束时间内的所有以分割时间进行分隔的时间参数
		//  精确到毫秒级别
		IntStream.range(0, cycleSize).forEach(i -> {
			ExportPageInfo pageInfo = new ExportPageInfo();
			pageInfo.setStartDate(i * getDefaultDateInterval() == 0 ? info.getTotalStartTime() : SimpleDateUtils.addDayStart(info.getTotalStartTime(), i * getDefaultDateInterval()));
			pageInfo.setEndDate((i * getDefaultDateInterval() + 2) < timeInterval ? SimpleDateUtils.addDayEnd(info.getTotalStartTime(), i * getDefaultDateInterval() + 2) : info.totalEndTime);
			pageInfoList.add(pageInfo);
		});
	}

	/**
	 * 使用分页可以流加载避免oom
	 *
	 * @return
	 */
	public List startQueryProcess() {
		// 并行去查询得到结果
		if (CollectionUtils.isEmpty(pageInfoList)) {
			throw new RuntimeException("cannot get any pageInfo from data");
		}
		List collect = pageInfoList
				.stream()
				.map(this::getCurrentDateList)
				.filter(list -> !CollectionUtils.isEmpty(list))
				.flatMap(Collection::stream)
				.collect(Collectors.toList());
		setTotalCount(collect.size());
		return collect;
	}

	/**
	 * 分时间段后分页查询每个时间段内的数据查询
	 *
	 * @param pages
	 * @return
	 */
	public List getCurrentDateList(ExportPageInfo pages) {

		List currentList = new ArrayList();
		if (totalInfo.getPageable()) {
			do {
				try {
					currentList.clear();
					currentList = doQuery(getPrototypeObj(obj, pages));
					//判断要是达到了默认的size大小，就开始写入到excel里面
					if (parallelList.size() > getDefaultExportListSize()) {
						getExportDataListToExcelList(parallelList);
						setTotalCount(getTotalCount()+parallelList.size());
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
		} else {
			parallelList.addAll(doQuery(getPrototypeObj(obj, pages)));
		}
		return parallelList;
	}


	/**
	 * 简单定义的一个时间工具类
	 */
	private static class SimpleDateUtils {
		/**
		 * date 转str
		 *
		 * @param date 传入的date
		 * @return
		 */
		private static String formatDate(Date date) {
			DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern("yyyy-MM-dd hh:mm:ss.SSS");
			return dateTimeFormatter.format(
					LocalDateTime.ofInstant(
							Instant.ofEpochMilli(date.getTime()),
							ZoneId.systemDefault()));
		}

		private static Date parseDate(String date) {
			return parseDate(date, "yyyy-MM-dd HH:mm:ss");
		}

		private static Date parseDate(String date, String formats) {
			DateTimeFormatter dateTimeFormatter = DateTimeFormatter.ofPattern(formats);
			LocalDateTime localDateTime = LocalDateTime.parse(date, dateTimeFormatter);
			return Date.from(localDateTime.atZone(ZoneId.systemDefault()).toInstant());
		}

		/**
		 * 将date转换为localdatetime
		 *
		 * @param date
		 * @return
		 */
		private static LocalDateTime changeDate(Date date) {
			Instant instant = date.toInstant();
			ZoneId zoneId = ZoneId.systemDefault();
			return instant.atZone(zoneId).toLocalDateTime();
		}

		private static Date addDayEnd(Date date, int num) {
			LocalDateTime dateTime = changeDate(date);
			LocalDateTime dateTime1 = dateTime.plusDays(num).with(ChronoField.MILLI_OF_SECOND, 499);
			return Date.from(dateTime1.atZone(ZoneId.systemDefault()).toInstant());
		}

		private static Date addDayStart(Date date, int num) {
			LocalDateTime dateTime = changeDate(date);
			LocalDateTime dateTime1 = dateTime.plusDays(num).with(ChronoField.MILLI_OF_SECOND, 500);
			return Date.from(dateTime1.atZone(ZoneId.systemDefault()).toInstant());
		}

	}

	/**
	 * @author fulln
	 * @description 导出的详细信息，只在内部使用
	 * @date Created in  10:29  2020-05-15.
	 */
	@Getter
	@Setter
	private static class ExportPageInfo {
		/**
		 * 页数
		 */
		private Integer pageSize = 1000;
		/**
		 * 页码
		 */
		private Integer pageNo = 1;
		/**
		 * 开始时间
		 */
		private Date startDate;
		/**
		 * 结束时间
		 */
		private Date endDate;
		/**
		 * id 开始标志
		 */
		private Long id;
	}

	/**
	 * @author fulln
	 * @description 导出的基本信息 对外部使用
	 * @date Created in  10:30  2020-05-15.
	 */
	@Getter
	@Setter
	public static class ExportTotalInfo {
		/**
		 * 总开始时间字段名称
		 */
		private String startTimeFiled;
		/**
		 * 总结束时间字段名称
		 */
		private String endTimeFiled;
		/**
		 * id字段名称
		 */
		private String idFiled;
		/**
		 * 总开始时间
		 */
		private Date totalStartTime;
		/**
		 * 总结束时间
		 */
		private Date totalEndTime;
		/**
		 * id 标志
		 */
		private Long id;
		/**
		 * 是否要分页
		 */
		private Boolean pageable = Boolean.TRUE;
		/**
		 * 单页数量字段名称
		 */
		private String pageSizeFiled = "pageSize";
		/**
		 * 页码字段名称
		 */
		private String pageNoFiled = "pageNo";

		/**
		 * id 字段
		 *
		 * @param id 传入的id
		 */
		public void setId(Integer id) {
			if (id == null) {
				throw new RuntimeException("id 不能为空");
			}
			this.id = Long.valueOf(id);
		}

		public void setId(Long id) {
			this.id = id;
		}

		public String getStartTimeFiled() {
			if (Objects.isNull(startTimeFiled)) {
				startTimeFiled = "startTime";
			}
			return startTimeFiled;
		}

		public String getEndTimeFiled() {
			if (Objects.isNull(endTimeFiled)) {
				endTimeFiled = "endTime";
			}
			return endTimeFiled;
		}

		public String getIdFiled() {
			if (Objects.isNull(idFiled)) {
				idFiled = "id";
			}
			return idFiled;
		}

		/**
		 * 最初开始时间
		 *
		 * @param totalStartTime 传入的开始时间
		 * @param formats        时间格式
		 */
		public void setTotalStartTime(String totalStartTime, String... formats) {
			if (formats.length == 1) {
				this.totalStartTime = SimpleDateUtils.parseDate(totalStartTime, formats[0]);
			} else {
				this.totalStartTime = SimpleDateUtils.parseDate(totalStartTime);
			}
		}

		public void setTotalStartTime(Date totalStartTime) {
			this.totalStartTime = totalStartTime;
		}

		/**
		 * 最初结束时间
		 *
		 * @param totalEndTime 传入的开始时间
		 * @param formats      时间格式
		 */
		public void setTotalEndTime(String totalEndTime, String... formats) {
			if (formats.length == 1) {
				this.totalEndTime = SimpleDateUtils.parseDate(totalEndTime, formats[0]);
			} else {
				this.totalEndTime = SimpleDateUtils.parseDate(totalEndTime);
			}
		}

		public void setTotalEndTime(Date totalEndTime) {
			this.totalEndTime = totalEndTime;
		}

	}

}
