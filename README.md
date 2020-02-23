# MultiprocessingSpider
## Description
MultiprocessingSpider is a simple and easy-to-use web crawling and web scraping framework.  

## Dependencies
- requests

## Installation
```
pip install MultiprocessingSpider
```

## Basic Usage
#### FileSpider
```python
from MultiprocessingSpider.spiders import FileSpider
from MultiprocessingSpider.packages import FileDataPackage


class MySpider(FileSpider):
    start_urls = ['https://www.a.com/page1']

    def parse(self, response):
        # parsing data from "response"
        ...
        # yield a file package
        yield FileDataPackage('https://www.a.com/file.png', 'file.png')
        ...
        # yield a new web page url and its parsing method
        yield 'https://www.a.com/page2', self.parse


spider = MySpider()
spider.run()
```
#### FileDownloader
```
>>> from MultiprocessingSpider.spiders import FileDownloader
>>> d = FileDownloader()

# add a file to download
>>> d.add_file('https://www.a.com/file.png', 'file.png')
True

# start the downloader
>>> d.run()
...
```
