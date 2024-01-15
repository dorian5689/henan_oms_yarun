-- nanfangyunying.data_oms definition

-- nanfangyunying.data_oms definition

CREATE TABLE `data_oms` (
  `省份` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `电场名称` varchar(100) CHARACTER SET utf8 NOT NULL,
  `日期` varchar(100) CHARACTER SET utf8 NOT NULL,
  `发电量` double DEFAULT NULL,
  `上网电量` double DEFAULT NULL,
  `弃电量` double DEFAULT NULL,
  `储能最大充电电力` double DEFAULT NULL,
  `储能最大放电电力` double DEFAULT NULL,
  `储能日充电` double DEFAULT NULL,
  `储能日放电` double DEFAULT NULL,
  `充电次数` bigint(20) DEFAULT NULL,
  `放电次数` bigint(20) DEFAULT NULL,
  `填报开始时间` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `填报结束时间` varchar(100) CHARACTER SET utf8 DEFAULT NULL,
  `是否已完成` int(11) DEFAULT NULL,
  PRIMARY KEY (`电场名称`,`日期`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_icelandic_ci;