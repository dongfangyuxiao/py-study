写这个脚本是为了发现单位的代码泄露事件，主要利用的方法有：
1、github高级语法搜索
使用各式高级语法发现泄露代码信息

2、gitprey的利用，gitprey是很好用的github代码泄露工具，用起来很不错，改良后，支持多个关键字搜索


3、码云代码泄露搜索

4、svn中国代码泄露搜索

5、thinksaas 代码泄露排查

6、oschina 代码泄露排查

依赖模块  requests re time json os sys supprocess 版本是python 2.7都可以

脚本执行后，会在目录下生成图示txt文件，github_xielou是使用语法搜索的结果  mayun是码云的搜索结果  其他txt文档看名字就知道，log文件是gitprey的排查结果