# 发行说明
## v1.1.2
#### 重构
- 删除 "FileDownloader" 中的 "name" 属性。
- 完善 "MultiprocessingSpider.utils" 中的 "UserAgentGenerator" 类。
- 继续优化各属性的setter方法。若给定值不符合条件会抛出异常；"sleep_time" 属性现在可以设置为 0。
- 调整子进程休眠策略：改为收到任务包之后休眠，可以防止同一时刻发出多个请求。
___
## v1.1.1
#### 修复漏洞
- 修复 "start_urls" 失效漏洞。
___
## v1.1.0
#### 新特性
- 为 "FileSpider" 添加覆盖文件选项。
- 添加路由系统。重载 "router" 方法之后，即可在解析方法中直接返回新网址或网址列表，无需指定对应的解析方法。

#### 修复漏洞
- 修复重试提示信息错误。

#### 重构
- 优化各属性的setter方法，现在可以这样写：spider.sleep_time = ' 5'。
- 当请求状态码 "status_code" 不在200与300之间时，不再重新发送请求。
##### a) MultiprocessingSpider
- "web_headers" 中的 "User-Agent" 改为随机生成。
- 将属性 "handled_url_table" 重命名为 "handled_urls"。
- 删除 "parse" 方法，添加示例方法："example_parse_method"。 
- 改变 "url_table" 的解析顺序，新解析顺序："FIFP"（First in First parse），即先添加的链接先解析。
##### b) FileDownloader
- 删除 "add_files" 方法.
___
## v1.0.0
- 初始版本.