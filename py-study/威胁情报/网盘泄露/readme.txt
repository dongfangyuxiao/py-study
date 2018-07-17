使用简介
这个脚本主要是用来排查网盘信息泄露，在企业员工有意识或无意识中可能会把一些企业内部资料或敏感信息上传到云盘备份，进而可能被不法分子获得，对企业的信息安全造成威胁。
脚本主要调用网盘搜索引起，共覆盖
http://www.pansou.com  盘搜
http://www.panduoduo.net/ 盘多多
http://www.wangpansou.com/ 网盘搜
http://www.iwapan.com/  爱挖盘
http://www.soyunpan.com  搜云盘
http://www.slimego.cn/   史莱姆搜索
https://www.57fx.com/search/  57分享
http://www.sosuopan.com/ 搜索盘
http://ishare.iask.sina.com.cn 爱共享
实际执行中出于各方面考虑只调用了57分享、爱挖盘、盘搜、史莱姆搜索和搜索盘。目录下的keyword.txt 中存放要搜索的关键字，建议中文（英文误报太高），支持多关键字搜索，每个关键字大概会有100个结果。