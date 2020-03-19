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
from re import escape, sub
from requests import get, post
from os.path import split, join
from random import choice, randint
from requests.exceptions import RequestException


def request_get(url, params=None, **kwargs):
    try:
        response = get(url, params, **kwargs)
    except RequestException:
        return None
    if 200 <= response.status_code < 400:
        return response
    return None


def request_post(url, data=None, json=None, **kwargs):
    try:
        response = post(url, data, json, **kwargs)
    except RequestException:
        return None
    if 200 <= response.status_code < 400:
        return response
    return None


def format_path(path, multiple=False, repl='_'):
    """
    Format path, replace invalid characters in it.
    :param path: the path string.
    :param multiple: whether path is a multi-level path.
    :param repl: the character used to replace invalid characters.
    :return: the formatted path string.
    """
    invalid_chars = [':', '*', '?', '"', '<', '>', '|', '/', '\\']
    repl = '_' if not isinstance(repl, str) or repl in invalid_chars else repl
    if multiple:
        temp = []
        dirname, basename = split(path)
        while dirname and basename:
            temp.append(format_path(basename))
            dirname, basename = split(dirname)
        else:
            temp.append(dirname if dirname else format_path(basename))
        path = ''
        while temp:
            path = join(path, temp.pop())
        return path
    else:
        return sub('|'.join([escape(char) for char in invalid_chars]), repl, path.strip())


class UAGenerator:
    __types = ['chrome', 'ie']

    user_agents = (
        'chrome', 'firefox', 'internet_explorer', 'opera', 'safari',
    )

    windows_platform_tokens = (
        'Windows 95', 'Windows 98', 'Windows 98; Win 9x 4.90', 'Windows CE',
        'Windows NT 4.0', 'Windows NT 5.0', 'Windows NT 5.01',
        'Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1',
        'Windows NT 6.2', 'Windows NT 10.0'
    )

    linux_processors = ('i686', 'x86_64')

    mac_processors = ('Intel', 'PPC', 'U; Intel', 'U; PPC')

    ios_versions = (
        '3.1.3', '4.2.1', '5.1.1', '6.1.6', '7.1.2', '9.3.5', '9.3.6', '10.3.3', '10.3.4', '12.4',
    )

    def random(self):
        return getattr(self, choice(self.__types))()

    def chrome(self, version_from=13, version_to=63, build_from=800, build_to=899):
        saf = '{0}.{1}'.format(randint(531, 536),
                               randint(0, 2))
        tmplt = '({0}) AppleWebKit/{1} (KHTML, like Gecko)' \
                ' Chrome/{2}.0.{3}.0 Safari/{4}'
        platforms = (
            tmplt.format(self.linux_platform_token(),
                         saf,
                         randint(version_from, version_to),
                         randint(build_from, build_to),
                         saf),
            tmplt.format(self.windows_platform_token(),
                         saf,
                         randint(version_from, version_to),
                         randint(build_from, build_to),
                         saf),
            tmplt.format(self.mac_platform_token(),
                         saf,
                         randint(version_from, version_to),
                         randint(build_from, build_to),
                         saf),
        )
        return 'Mozilla/5.0 ' + choice(platforms)

    def ie(self):
        tmplt = 'Mozilla/5.0 (compatible; MSIE {0}.0; {1}; Trident/{2}.{3})'
        return tmplt.format(randint(5, 9),
                            self.windows_platform_token(),
                            randint(3, 5),
                            randint(0, 1))

    @property
    def types(self):
        return self.__types

    def windows_platform_token(self):
        return choice(self.windows_platform_tokens)

    def linux_platform_token(self):
        return 'X11; Linux {0}'.format(
            choice(self.linux_processors))

    def mac_platform_token(self):
        return 'Macintosh; {0} Mac OS X 10_{1}_{2}'.format(
            choice(self.mac_processors),
            randint(5, 12),
            randint(0, 9),
        )
