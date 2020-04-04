# MultiprocessingSpider
[[English version]](https://github.com/Xpp521/MultiprocessingSpider/blob/master/README.md "English version")
## 简介
MultiprocessingSpider是一个基于多进程的、简单易用的爬虫框架。

## 架构
![Architecture](https://raw.githubusercontent.com/Xpp521/Images/master/MultiprocessingSpider_Architecture_cn.jpg)

## 依赖
- requests

## 安装
```
pip install MultiprocessingSpider
```

## 基本使用
#### MultiprocessingSpider
```python
from MultiprocessingSpider.spiders import MultiprocessingSpider
from MultiprocessingSpider.packages import TaskPackage, ResultPackage


class MyResultPackage(ResultPackage):
    def __init__(self, prop1, prop2, sleep=True):
        super().__init__(sleep)
        self.prop1 = prop1
        self.prop2 = prop2


class MySpider(MultiprocessingSpider):
    start_urls = ['https://www.a.com/page1']

    proxies = [
        {"http": "http://111.111.111.111:80"},
        {"http": "http://123.123.123.123:8080"}
    ]

    def router(self, url):
        return self.parse

    def parse(self, response):
        # 从"response"中解析任务包或新网址
        ...
        # 返回一个任务包
        yield TaskPackage('https://www.a.com/task1')
        ...
        # 返回新网址（列表）
        yield 'https://www.a.com/page2'
        ...
        yield ['https://www.a.com/page3', 'https://www.a.com/page4']

    @classmethod
    def subprocess_handler(cls, package, sleep_time, timeout, retry):
        url = package.url
        # 加载"url"并解析数据
        ...
        # 返回结果包
        return MyResultPackage('value1', 'value2')

    @staticmethod
    def process_result_package(package):
        # 对结果包中的数据进行预处理
        if 'value1' == package.prop1:
            return package
        else:
            return None


if __name__ == '__main__':
    s = MySpider()

    # 启动爬虫
    s.start()

    # 阻塞当前进程
    s.join()

    # 将结果导出到csv文件
    s.to_csv('result.csv')

    # 将结果导出到json文件
    s.to_json('result.json')
```
#### FileSpider
```python
from MultiprocessingSpider.spiders import FileSpider
from MultiprocessingSpider.packages import FilePackage


class MySpider(FileSpider):
    start_urls = ['https://www.a.com/page1']

    stream = True

    buffer_size = 1024

    overwrite = False

    def router(self, url):
        return self.parse

    def parse(self, response):
        # 从"response"中解析任务包或新网址
        ...
        # 返回文件任务包
        yield FilePackage('https://www.a.com/file.png', 'file.png')
        ...
        # 返回新网址（列表）
        yield 'https://www.a.com/page2'
        ...
        yield ['https://www.a.com/page3', 'https://www.a.com/page4']


if __name__ == '__main__':
    s = MySpider()

    # 添加网址
    s.add_url('https://www.a.com/page5')

    # 启动爬虫
    s.start()

    # 阻塞当前进程
    s.join()
```
#### FileDownloader
```python
from MultiprocessingSpider.spiders import FileDownloader


if __name__ == '__main__':
    d = FileDownloader()

    # 启动下载器
    d.start()
    
    # 添加任务
    d.add_file('https://www.a.com/file.png', 'file.png')
    
    # 阻塞当前进程
    d.join()
```
更多用法 → [GitHub](https://github.com/Xpp521/MultiprocessingSpider/tree/master/examples "示例")
### 许可证
[GPLv3.0](https://github.com/Xpp521/MultiprocessingSpider/blob/master/LICENSE.md "License")  
这是一个自由软件，欢迎感兴趣的小伙伴贡献代码 : )
