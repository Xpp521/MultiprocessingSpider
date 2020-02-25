# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Xpp521
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from time import sleep
from os import makedirs
from requests import get
from random import randint
from ..utils import UAGenerator
from os.path import exists, join
from multiprocessing import Process, Queue, cpu_count
from ..packages import TaskPackage, FilePackage, ResultPackage, SignalPackage


class MultiprocessingSpider:
    # spider name
    __name = ''

    # proxy ip
    proxies = [None]

    # request headers
    web_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/65.0.3325.162 Safari/537.36'}

    # start urls
    start_urls = []

    def __init__(self, name=None, process_num=None, sleep_time=None, timeout=None, retry=None):
        self.__name = name if name and isinstance(name, str) else 'unset'
        base_class = str(self.__class__.__base__)
        self.__base_class = base_class[base_class.find("'") + 1: base_class.rfind("'")]
        # Process pool
        self.__pool = []
        self.timeout = timeout
        self.sleep_time = sleep_time
        self.retry = retry
        self.__result = []
        self.__url_table = [url for url in self.start_urls if url.startswith('http')]
        self.__handled_url_tables = []
        self.__data_queue = Queue()
        self.__result_queue = Queue()
        self.process_num = process_num if isinstance(process_num, int) and 1 <= process_num <= 50 else cpu_count()

    def add_url(self, url, handler=None):
        """Add a url.
        :param url: url.
        :param handler: handler function, default value: self.parse.
        :rtype: bool.
        """
        if handler is None:
            handler = self.parse
        if isinstance(url, str) and url.startswith('http') and callable(handler):
            self.__url_table.append((url, handler))
            if self.__pool:
                self.__parse()
            return True
        return False

    def add_urls(self, urls, handlers=None):
        """Add urls.
        :param urls: url list.
        :param handlers: handler list.
        :rtype: bool.
        """
        if handlers is None:
            handlers = [self.parse for _ in urls]
        if isinstance(urls, list) and isinstance(handlers, list) and len(urls) == len(handlers):
            return all([self.add_url(url, handler) for url, handler in zip(urls, handlers)])
        return False

    def _add_data_package(self, package):
        if isinstance(package, TaskPackage):
            self.__data_queue.put_nowait(package)
            return True
        return False

    def __download_web(self):
        """Download web page."""
        while self.__url_table:
            url_data = self.__url_table.pop()
            if url_data not in self.__handled_url_tables:
                n = 1
                while True:
                    if self._retry + 1 < n:
                        self.__handled_url_tables.append(url_data)
                        break
                    try:
                        response = get(url_data[0], headers=self.web_headers, timeout=self._timeout)
                    except Exception as e:
                        print('【Web page load failed】{}, message: {}, try re-downloading ({}/{})...'.
                              format(url_data[0], e, n, self._retry))
                    else:
                        if 200 <= response.status_code < 300:
                            self.__handled_url_tables.append(url_data)
                            yield response, url_data[1]
                            break
                        else:
                            print('【Web page load failed】{}, status code: {}, try re-downloading ({}/{})...'
                                  .format(url_data[0], response.status_code, n, self._retry))
                    n += 1
                    sleep(randint(1, self._sleep_time))

    def __parse(self):
        """Parse data."""
        for response, parse in self.__download_web():
            for p in parse(response):
                if isinstance(p, tuple) and 2 == len(p):
                    self.add_url(p[0], p[1])
                else:
                    if isinstance(p, TaskPackage):
                        self.__data_queue.put_nowait(p)
            sleep(randint(1, self._sleep_time))

    @classmethod
    def _subprocess_wrapper(cls, data_queue, result_queue, sleep_time, timeout, retry):
        while True:
            p = data_queue.get()
            if SignalPackage.END == p:
                result_queue.put_nowait(p)
                return
            elif isinstance(p, TaskPackage):
                result_package = cls.subprocess_handler(p, sleep_time, timeout, retry)
                if isinstance(result_package, ResultPackage):
                    result_queue.put_nowait(result_package)
                    if result_package.sleep:
                        sleep(randint(1, sleep_time))
                else:
                    sleep(randint(1, sleep_time))

    @classmethod
    def subprocess_handler(cls, package, sleep_time, timeout, retry):
        """Handler function for subprocesses.
        :param package: task package.
        :param sleep_time: max sleep time after each download.
        :param timeout: timeout.
        :param retry: retry count.
        :rtype: MultiprocessingSpider.packages.ResultPackage or its subclass or None.
        """
        raise NotImplementedError

    def parse(self, response):
        """Parse target content from response.
        ex:

        def parse(self, response):

            # yield a task package
            yield TaskPackage('https://www.a.com/page_1/task1')

            # yield a new url with its parsing method, which will be parsed later
            yield 'https://www.a.com/page_2', self.parse

        :param response: response object, type: requests.models.Response.
        :rtype: GentileSpider.packages.TaskPackage or its subclass or a url tuple.
        """
        raise NotImplementedError

    @staticmethod
    def process_result_package(package):
        """Process result package.
        :return: MultiprocessingSpider.packages.ResultPackage or its subclass or None.
        """
        return package

    def start(self):
        """Start method."""
        self._start()
        self.__parse()

    def _start(self):
        for _ in range(self._process_num):
            self.__pool.append(Process(target=self._subprocess_wrapper,
                                       args=(self.__data_queue, self.__result_queue,
                                             self._sleep_time, self._timeout, self._retry)))
            self.__pool[-1].start()
        print(self.info)
        print('———————————————Mission (⊙o⊙) Start———————————————')

    def join(self):
        for _ in self.__pool:
            self.__data_queue.put_nowait(SignalPackage.END)
        n = 0
        while True:
            if self._process_num == n:
                break
            result_package = self.__result_queue.get()
            if SignalPackage.END == result_package:
                n += 1
            elif isinstance(result_package, ResultPackage):
                result_package = self.process_result_package(result_package)
                if isinstance(result_package, ResultPackage):
                    json = result_package.json()
                    if json:
                        self.__result.append(json)
        while self.__pool:
            self.__pool.pop().terminate()
        print('———————————————Mission (∩_∩) Accomplished——————————')

    def to_csv(self, path):
        """Export results in csv.
        :param path: csv file path.
        :rtype: bool.
        """
        if self.__result:
            from csv import DictWriter
            with open(path, 'w', encoding='utf', newline='') as f:
                writer = DictWriter(f, self.__result[0].keys())
                writer.writeheader()
                writer.writerows(self.__result)
                return True
        return False

    def to_json(self, path):
        """Export results in json.
        :param path: json file path.
        :rtype: bool.
        """
        if self.__result:
            from json import dump
            dump(self.__result, open(path, 'w', encoding='utf'))
            return True
        return False

    @property
    def info(self):
        return '''\t\t\tSpider message
name:\t\t\t\t{}
class:\t\t\t\t{}
base class:\t\t\t{}
subprocess count:\t{}
max sleep time:\t\t{}s
timeout:\t\t\t{}s
retry count:\t\t{}'''.format(self.__name, self.__class__.__name__, self.__base_class,
                             self._process_num, self._sleep_time, self._timeout, self._retry)

    @property
    def name(self):
        return self.__name

    @property
    def process_num(self):
        return self._process_num

    @process_num.setter
    def process_num(self, n):
        if isinstance(n, int) and 1 <= n <= 50:
            self._process_num = n

    @property
    def sleep_time(self):
        return self._sleep_time

    @sleep_time.setter
    def sleep_time(self, t):
        t = t if isinstance(t, int) and 0 < t else 5
        self._sleep_time = t

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, t):
        t = t if isinstance(t, int) and 0 < t else 5
        self._timeout = t

    @property
    def retry(self):
        return self._retry

    @retry.setter
    def retry(self, r):
        r = r if isinstance(r, int) and 0 <= r <= 5 else 3
        self._retry = r

    @property
    def url_table(self):
        return self.__url_table

    @property
    def handled_url_table(self):
        return self.__handled_url_tables


class FileSpider(MultiprocessingSpider):
    """File spider base class."""

    # request headers for subprocesses
    # PS：subprocess will generate "User-Agent" automatically.
    file_headers = {}

    # download file in chunks
    stream = False

    # chunk size
    buffer_size = 1024

    @classmethod
    def _download_file(cls, url, path, timeout=10, retry=0):
        """
        :param url: file url.
        :param path: storage path.
        :param timeout: timeout.
        :param retry: retry count.
        :rtype: bool.
        """
        headers = cls.file_headers
        headers['User-Agent'] = UAGenerator().random()
        proxies = cls.proxies
        n = 1
        while True:
            if retry + 1 < n:
                return False
            try:
                response = get(url, headers=headers, proxies=proxies[randint(0, len(proxies)) - 1], timeout=timeout)
            except Exception as e:
                print('【File download failed】{}, message: {}, try re-downloading ({}/{})...'.format(path, e, n, retry))
            else:
                if 200 <= response.status_code < 300:
                    with open(path, 'wb') as file:
                        if cls.stream:
                            for chunk in response.iter_content(cls.buffer_size):
                                if chunk:
                                    file.write(chunk)
                        else:
                            file.write(response.content)
                    print('【File downloaded successfully】{}'.format(path))
                    return True
                else:
                    print('【File download failed】{}, status code: {}, try re-downloading ({}/{})...'.
                          format(path, response.status_code, n, retry))
            n += 1

    @classmethod
    def subprocess_handler(cls, package, sleep_time, timeout, retry):
        root = package.root
        if root:
            try:
                if not exists(root):
                    makedirs(root)
            except FileExistsError:
                pass
            file_path = join(root, package.name)
        else:
            file_path = package.name
        if exists(file_path):
            return ResultPackage(False)
        else:
            cls._download_file(package.url, file_path, timeout)
            return ResultPackage()

    def parse(self, response):
        """Parse target content from response.
        ex:

        def parse(self, response):

            # yield a file package for subprocesses to handle
            yield FilePackage(image.png, 'https://www.a.com/image.png')

            # yield a new web page url and its parsing method, which will be parsed later
            yield 'https://www.a.com/page_2', self.parse

        :param response: response object, type: requests.models.Response.
        :rtype: GentileSpider.packages.FilePackage or its subclass or a url tuple.
        """
        raise NotImplementedError

    @staticmethod
    def process_data_package(package):
        if isinstance(package, FilePackage):
            return package


class FileDownloader(FileSpider):
    """Multiprocessing file downloader."""
    def add_file(self, url, filename, dirname='', https2http=False):
        return self._add_data_package(FilePackage(url, filename, dirname, https2http))

    def add_files(self, urls, filenames, dirname='', https2http=False):
        if len(urls) == len(filenames):
            return all([self.add_file(url, filename, dirname, https2http) for url, filename in zip(urls, filenames)])
        return False

    def start(self):
        """Start the downloader."""
        self._start()

    def add_url(self, url, handler=None):
        return False

    def add_urls(self, urls, handlers=None):
        return False

    def parse(self, response):
        pass
