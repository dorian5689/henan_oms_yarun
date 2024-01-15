-- nanfangyunying.data_oms_notification_table definition

CREATE TABLE `data_oms_notification_table` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subject` varchar(255) DEFAULT NULL COMMENT '主题',
  `needs_feedback` varchar(8) DEFAULT NULL COMMENT '是否需要反馈',
  `feedback_deadline` date DEFAULT NULL COMMENT '反馈截止日期',
  `processing_info` text COMMENT '处理信息',
  `feedback_time` datetime DEFAULT NULL COMMENT '反馈时间',
  `publisher` varchar(255) DEFAULT NULL COMMENT '发布人',
  `publish_time` datetime DEFAULT NULL COMMENT '发布时间',
  `attachment_name` varchar(255) DEFAULT NULL COMMENT '操作',
  `attachment_data` longblob COMMENT '存储附件数据',
  PRIMARY KEY (`id`),
  UNIQUE KEY `publish_time` (`publish_time`)
) ENGINE=InnoDB AUTO_INCREMENT=200 DEFAULT CHARSET=utf8;