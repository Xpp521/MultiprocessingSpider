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
from enum import IntEnum
from ..utils import format_path


class SignalPackage(IntEnum):
    # stop signal
    END = 0


class ResultPackage:
    """Result package base class."""
    def __init__(self, sleep=True):
        # notify the subprocess whether to sleep after returning this package
        self.__sleep = sleep

    @property
    def sleep(self):
        return self.__sleep

    def json(self):
        r = {}
        for p in dir(self):
            if not p.startswith('_') and 'sleep' != p and not callable(getattr(self, p)):
                r[p] = (str(getattr(self, p)))
        return r


class DataPackage:
    """Data package base class."""
    def __init__(self, url, https2http=False):
        """
        :param url: data url.
        :param https2http: whether to convert https to http.
        """
        if not isinstance(url, str):
            raise TypeError('url must be a string')
        if not url.startswith('http'):
            raise ValueError('wrong url format')
        self._url = url.replace('https', 'http') if https2http else url

    @property
    def url(self):
        return self._url

    def __repr__(self):
        return '''<{} url: {}>'''.format(self.__class__.__name__, self._url)


class FileDataPackage(DataPackage):
    """File package class."""
    def __init__(self, url, filename, dirname='', https2http=False):
        """
        :param filename: filename.
        :param url: file url.
        :param dirname: the name of the storage directory.
        :param https2http: whether to convert https to http.
        """
        super(self.__class__, self).__init__(url, https2http)
        if isinstance(filename, str) and isinstance(dirname, str):
            self._name = format_path(filename)
            self._root = format_path(dirname, True)
        else:
            raise TypeError('name and dirname must be a string')

    @property
    def name(self):
        return self._name

    @property
    def root(self):
        return self._root

    def __repr__(self):
        return '<{} name: {} url: {}>'.format(self.__class__.name, self._name, self._url)
