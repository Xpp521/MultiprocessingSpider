# MultiprocessingSpider
[[简体中文版]](https://github.com/Xpp521/MultiprocessingSpider/blob/master/README_cn.md "中文版")
## Description
MultiprocessingSpider is a simple and easy-to-use web crawling and web scraping framework.

## Architecture
![Architecture](https://raw.githubusercontent.com/Xpp521/Images/master/MultiprocessingSpider_Architecture.jpg)

## Dependencies
- requests

## Installation
```
pip install MultiprocessingSpider
```

## Basic Usage
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

    def parse(self, response):
        # # parsing task or new page from "response"
        ...
        # yield a task package
        yield TaskPackage('https://www.a.com/task1')
        ...
        # yield a new web page url and its parsing method
        yield 'https://www.a.com/page2', self.parse

    @classmethod
    def subprocess_handler(cls, package, sleep_time, timeout, retry):
        url = package.url
        # request "url" and parse data
        ...
        # return result package
        return MyResultPackage('value1', 'value2')

    @staticmethod
    def process_result_package(package):
        # Processing result package
        if 'value1' == package.prop1:
            return package
        else:
            return None


if __name__ == '__main__':
    s = MySpider()

    # Start the spider
    s.start()

    # Block current process
    s.join()

    # Export results to csv file
    s.to_csv('result.csv')

    # Export results to json file
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

    def parse(self, response):
        # parsing task or new page from "response"
        ...
        # yield a file package
        yield FilePackage('https://www.a.com/file.png', 'file.png')
        ...
        # yield a new web page url and its parsing method
        yield 'https://www.a.com/page2', self.parse


if __name__ == '__main__':
    s = MySpider()

    # Add a new page
    s.add_url('https://www.a.com/page3')

    # Start the spider
    s.start()

    # Block current process
    s.join()
```
#### FileDownloader
```python
from MultiprocessingSpider.spiders import FileDownloader


if __name__ == '__main__':
    d = FileDownloader()

    # Start the downloader
    d.start()
    
    # Add a file
    d.add_file('https://www.a.com/file.png', 'file.png')
    
    # Block current process
    d.join()
```
