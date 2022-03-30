DROP TABLE IF EXISTS `scan_result`;
CREATE TABLE `scan_result` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `IP` varchar(255) default NULL,
  `Port` int(11) default NULL,
  `ServiceName` varchar(255) default NULL,
  `Version` varchar(255) default NULL,
  `TaskType` varchar(255) default NULL,						/*任务类型，如celery的定时任务、人工提交的即时任务*/
  `CreateTime` datetime DEFAULT current_timestamp,			/*插入时默认填写当前时间*/
  `UpdateTime` datetime default current_timestamp,			/*插入时默认填写当前时间*/
  `Submitter` varchar(255) default NULL,					/*任务提交者，如celery自动化，安全小组谁手动提交的，记录用户名*/
  `Flags` int(10) DEFAULT NULL,								/*是否处理的标记, 0为新增的, 1为正在处理的, 2为已经处理的*/
  PRIMARY KEY  (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
