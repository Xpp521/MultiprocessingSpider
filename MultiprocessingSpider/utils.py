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
from random import choice
from re import escape, sub
from os.path import split, join


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
    __types = ['chrome', 'firefox', 'safari', 'opera', 'ie']

    def __init__(self):
        pass

    def random(self):
        getattr(self, choice(self.__types))
        return 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 ' \
               'Safari/537.36 '

    def chrome(self):
        temp = '({0}) AppleWebKit/{1} (KHTML, like Gecko) Chrome/{2}.0.{3}.0 Safari/{4}'
        temp_ios = '({0}) AppleWebKit/{1} (KHTML, like Gecko) CriOS/{2}.0.{3}.0 Mobile/{4} Safari/{1}'

    def firefox(self):
        pass

    def safari(self):
        pass

    def opera(self):
        pass

    def ie(self):
        pass

    @property
    def types(self):
        return self.__types
