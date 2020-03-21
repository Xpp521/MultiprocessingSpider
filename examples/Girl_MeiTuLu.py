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
from os import mkdir
from lxml.etree import HTML
from re import search, split
from os.path import join, exists
from MultiprocessingSpider.utils import format_path
from MultiprocessingSpider.spiders import FileSpider
from MultiprocessingSpider.packages import FilePackage


class MeiTuLuSpider(FileSpider):
    """https://www.meitulu.com/"""

    name = 'MeiTuLuSpider'

    proxies = [
        {"http": "http://39.137.95.74:80"},
        {"http": "http://39.137.69.7:8080"},
        {"http": "http://221.180.170.104:8080"},
        {"http": "http://180.118.252.180:8118"},
    ]

    def router(self, url):
        if url.startswith('https://www.meitulu.com/item/'):
            return self.parse_album
        else:
            return self.parse_other

    def parse_album(self, response):
        html = HTML(response.content.decode('utf8'))
        # 标题
        title = html.xpath('//div[@class="weizhi"]/h1/text()')[0]
        if search(r' \d+/\d+$', title):
            title = title[:title.rfind(' ')]
        # 图片网址
        base_url = html.xpath('//div[@class="content"]/center/img[1]/@src')[0]
        suffix = base_url[base_url.rfind('.'):]
        base_url = base_url[:base_url.rfind('/') + 1]
        div = html.xpath('//div[@class="c_l"]')[0]
        # 发行机构
        source = div.xpath('p[1]/a/text()')[0]
        # 发行机构网址
        source_url = div.xpath('p[1]/a/@href')[0]
        # 图片数量
        num = div.xpath('p[2]/text()')[0]
        if '图片数量' not in num:
            num = div.xpath('p[3]/text()')[0]
        num = int(num[num.find(' ') + 1: num.rfind(' ')])
        # 模特名称
        model = div.xpath('p[last()-1]/a/text()')[0] if div.xpath('p[last()-1]/a') \
            else div.xpath('p[last()-1]/text()')[0]
        model = model[model.find('：') + 1:]
        # 模特网址
        model_url = div.xpath('p[last()-1]/a/@href')
        model_url = model_url[0] if model_url else ''
        # 发行日期
        date = div.xpath('p[last()]/text()')[0]
        # 标签
        tags = ''
        for tag in html.xpath('//div[@class="fenxiang_l"]/a'):
            tags += '\t{}\t{}\r\n'.format(tag.xpath('text()')[0], tag.xpath('@href')[0])
        # 补充说明
        msg = html.xpath('//p[@class="buchongshuoming"]/text()')
        msg = msg[0] if msg else ''
        info = '''{}

模特名称：{}\t\t{}
发行机构：{}\t\t{}
{}
标签：
{}
补充说明：{}'''.format(title, model, model_url, source, source_url, date, tags, msg)
        title = format_path(title)
        if not exists(title):
            mkdir(title)
        with open(join(title, 'info.txt'), 'w', encoding='utf') as file:
            file.write(info)
        for i in range(1, num + 1):
            yield FilePackage('{}{}{}'.format(base_url, i, suffix), '{}{}'.format(i, suffix), title, True)

    def parse_other(self, response):
        yield HTML(response.content.decode('utf8')).xpath('//div[@class="boxs"]/ul/li/a/@href')


def main():
    p_num = input('子进程数量：')
    s_time = input('最大休眠时间（秒）：')
    timeout = 5
    retry = 3
    s = MeiTuLuSpider(p_num, s_time, timeout, retry)
    while True:
        r = s.add_urls(split(r' +', input('网址（多个网址用空格分隔）：').strip()))
        if r:
            s.start()
            s.join()
        else:
            print('格式错误！重新输入。')
            continue


if __name__ == '__main__':
    main()
