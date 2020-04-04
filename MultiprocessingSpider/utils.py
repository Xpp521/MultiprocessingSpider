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
from datetime import date
from re import escape, sub
from calendar import isleap
from requests import get, post
from os.path import split, join
from random import choice, randint, getrandbits
from requests.exceptions import RequestException


def request_get(url, params=None, **kwargs):
    """Send a GET request with requests library.
    :rtype: requests.models.Response or None."""
    try:
        response = get(url, params, **kwargs)
    except RequestException:
        return None
    if 200 <= response.status_code < 300:
        return response
    return None


def request_post(url, data=None, json=None, **kwargs):
    """Send a POST request with requests library.
    :rtype: requests.models.Response or None."""
    try:
        response = post(url, data, json, **kwargs)
    except RequestException:
        return None
    if 200 <= response.status_code < 300:
        return response
    return None


def try_convert2int(obj, default=None):
    """Try converting "obj" to an integer.
    :param obj: the object to be converted.
    :param default: the default return value when conversion fails. Type: int.
    :rtype: int or original object.
    """
    if isinstance(obj, int):
        return obj
    elif isinstance(obj, (bool, float)):
        return int(obj)
    elif isinstance(obj, str):
        obj = obj.strip()
        if obj:
            if obj.isnumeric() or '-' == obj[0] and obj[1:].isnumeric():
                return int(obj)
    return default if isinstance(default, int) else obj


def try_convert2float(obj, default=None):
    """Try converting "obj" to a float.
    :param obj: the object to be converted:param default: the default return value when conversion fails.
    :param default: the default return value when conversion fails. Type: float.
    :rtype: float or original object.
    """
    if isinstance(obj, float):
        return obj
    elif isinstance(obj, (bool, int)):
        return float(obj)
    elif isinstance(obj, str):
        obj = obj.strip()
        if obj:
            minus = '-' == obj[0]
            dot = 1 == obj.count('.')
            if minus and dot:
                if obj[1:].replace('.', '').isnumeric():
                    return float(obj)
            elif minus:
                if obj[1:].isnumeric():
                    return float(obj)
            elif dot:
                if any(obj.split('.')):
                    return float(obj)
            else:
                if obj.isnumeric():
                    return float(obj)
    return default if isinstance(default, float) else obj


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


class UserAgentGenerator:
    """PC User-Agent generator class."""
    __types = ('ie', 'chrome', 'opera', 'safari', 'firefox')

    __linux_processors = ('x86_64', 'i686')

    __mac_processors = ('U; Intel', 'U; PPC', 'PPC', 'Intel')

    __windows_versions = ('Windows NT 5.1', 'Windows NT 5.2', 'Windows NT 6.0', 'Windows NT 6.1', 'Windows NT 6.2',
                          'Windows NT 6.4', 'Windows NT 10.0')

    __language_locale_codes = {
        'aa': ('DJ', 'ER', 'ET'), 'af': ('ZA',), 'ak': ('GH',), 'am': ('ET',), 'an': ('ES',), 'apn': ('IN',),
        'ar': ('AE', 'BH', 'DJ', 'DZ', 'EG', 'EH', 'ER', 'IL', 'IN', 'IQ', 'JO', 'KM', 'KW', 'LB', 'LY', 'MA', 'MR',
               'OM', 'PS', 'QA', 'SA', 'SD', 'SO', 'SS', 'SY', 'TD', 'TN', 'YE'),
        'as': ('IN',), 'ast': ('ES',), 'ayc': ('PE',), 'az': ('AZ', 'IN'),
        'be': ('BY',), 'bem': ('ZM',), 'ber': ('DZ', 'MA'), 'bg': ('BG',), 'bhb': ('IN',), 'bho': ('IN',),
        'bn': ('BD', 'IN'), 'bo': ('CN', 'IN'), 'br': ('FR',), 'brx': ('IN',), 'bs': ('BA',), 'byn': ('ER',),
        'ca': ('AD', 'ES', 'FR', 'IT'), 'ce': ('RU',), 'ckb': ('IQ',), 'cmn': ('TW',), 'crh': ('UA',), 'cs': ('CZ',),
        'csb': ('PL',), 'cv': ('RU',), 'cy': ('GB',),
        'da': ('DK',), 'de': ('AT', 'BE', 'CH', 'DE', 'LI', 'LU'), 'doi': ('IN',), 'dv': ('MV',), 'dz': ('BT',),
        'el': ('GR', 'CY'), 'en': ('AG', 'AU', 'BW', 'CA', 'DK', 'GB', 'HK', 'IE', 'IN', 'NG', 'NZ', 'PH', 'SG', 'US',
                                   'ZA', 'ZM', 'ZW'),
        'eo': ('US',), 'es': ('AR', 'BO', 'CL', 'CO', 'CR', 'CU', 'DO', 'EC', 'ES', 'GT', 'HN', 'MX', 'NI', 'PA', 'PE',
                              'PR', 'PY', 'SV', 'US', 'UY', 'VE'),
        'et': ('EE',), 'eu': ('ES', 'FR'),
        'fa': ('IR',), 'ff': ('SN',), 'fi': ('FI',), 'fil': ('PH',), 'fo': ('FO',), 'fr': ('CA', 'CH', 'FR', 'LU'),
        'fur': ('IT',), 'fy': ('NL', 'DE'),
        'ga': ('IE',), 'gd': ('GB',), 'gez': ('ER', 'ET'), 'gl': ('ES',), 'gu': ('IN',), 'gv': ('GB',),
        'ha': ('NG',), 'hak': ('TW',), 'he': ('IL',), 'hi': ('IN',), 'hne': ('IN',), 'hr': ('HR',), 'hsb': ('DE',),
        'ht': ('HT',), 'hu': ('HU',), 'hy': ('AM',),
        'ia': ('FR',), 'id': ('ID',), 'ig': ('NG',), 'ik': ('CA',), 'is': ('IS',), 'it': ('CH', 'IT'), 'iu': ('CA',),
        'iw': ('IL',), 'ja': ('JP',),
        'ka': ('GE',), 'kk': ('KZ',), 'kl': ('GL',), 'km': ('KH',), 'kn': ('IN',), 'ko': ('KR',), 'kok': ('IN',),
        'ks': ('IN',), 'ku': ('TR',), 'kw': ('GB',), 'ky': ('KG',),
        'lb': ('LU',), 'lg': ('UG',), 'li': ('BE', 'NL'), 'lij': ('IT',), 'ln': ('CD',), 'lo': ('LA',), 'lt': ('LT',),
        'lv': ('LV',), 'lzh': ('TW',),
        'mag': ('IN',), 'mai': ('IN',), 'mg': ('MG',), 'mhr': ('RU',), 'mi': ('NZ',), 'mk': ('MK',), 'ml': ('IN',),
        'mn': ('MN',), 'mni': ('IN',), 'mr': ('IN',), 'ms': ('MY',), 'mt': ('MT',), 'my': ('MM',),
        'nan': ('TW',), 'nb': ('NO',), 'nds': ('DE', 'NL'), 'ne': ('NP',), 'nhn': ('MX',), 'niu': ('NU', 'NZ'),
        'nl': ('AW', 'BE', 'NL'), 'nn': ('NO',), 'nr': ('ZA',), 'nso': ('ZA',),
        'oc': ('FR',), 'om': ('ET', 'KE'), 'or': ('IN',), 'os': ('RU',),
        'pa': ('IN', 'PK'), 'pap': ('AN', 'AW', 'CW'), 'pl': ('PL',), 'ps': ('AF',), 'pt': ('BR', 'PT'), 'quz': ('PE',),
        'raj': ('IN',), 'ro': ('RO',), 'ru': ('RU', 'UA'), 'rw': ('RW',),
        'sa': ('IN',), 'sat': ('IN',), 'sc': ('IT',), 'sd': ('IN', 'PK'), 'se': ('NO',), 'shs': ('CA',), 'si': ('LK',),
        'sid': ('ET',), 'sk': ('SK',), 'sl': ('SI',), 'so': ('DJ', 'ET', 'KE', 'SO'), 'sq': ('AL', 'ML'),
        'sr': ('ME', 'RS'), 'ss': ('ZA',), 'st': ('ZA',), 'sv': ('FI', 'SE'), 'sw': ('KE', 'TZ'), 'szl': ('PL',),
        'ta': ('IN', 'LK'), 'tcy': ('IN',), 'te': ('IN',), 'tg': ('TJ',), 'th': ('TH',), 'the': ('NP',),
        'ti': ('ER', 'ET'), 'tig': ('ER',), 'tk': ('TM',), 'tl': ('PH',), 'tn': ('ZA',), 'tr': ('CY', 'TR'),
        'ts': ('ZA',), 'tt': ('RU',),
        'ug': ('CN',), 'uk': ('UA',), 'unm': ('US',), 'ur': ('IN', 'PK'), 'uz': ('UZ',),
        've': ('ZA',), 'vi': ('VN',),
        'wa': ('BE',), 'wae': ('CH',), 'wal': ('ET',), 'wo': ('SN',), 'xh': ('ZA',),
        'yi': ('US',), 'yo': ('NG',), 'yue': ('HK',),
        'zh': ('CN', 'HK', 'SG', 'TW'), 'zu': ('ZA',),
    }

    def random(self):
        return getattr(self, choice(self.__types))()

    def ie(self):
        return 'Mozilla/5.0 (compatible; MSIE {}.0; {}; Trident/{}.{})'.format(randint(5, 9), self.__windows_token(),
                                                                               randint(3, 5), randint(0, 1))

    def chrome(self, version_from=55, version_to=81, build_from=800, build_to=899):
        saf = '{}.{}'.format(randint(531, 536), randint(0, 2))
        template = '({}) AppleWebKit/{} (KHTML, like Gecko) Chrome/{}.0.{}.0 Safari/{}'
        platforms = (
            template.format(self.__linux_token(), saf, randint(version_from, version_to), randint(build_from, build_to),
                            saf),
            template.format(self.__windows_token(), saf, randint(version_from, version_to),
                            randint(build_from, build_to), saf),
            template.format(self.__mac_token(), saf, randint(version_from, version_to), randint(build_from, build_to),
                            saf)
        )
        return 'Mozilla/5.0 {}'.format(choice(platforms))

    def opera(self):
        return 'Opera/{}.{}.{}'.format(
            randint(8, 9),
            randint(10, 99),
            '({}; {}) Presto/2.9.{} Version/{}.00'.format(
                (self.__linux_token() if getrandbits(1) else self.__windows_token()),
                self.__locale(),
                randint(160, 190),
                randint(10, 12)
            )
        )

    def safari(self):
        saf = "{}.{}.{}".format(randint(531, 535), randint(1, 50), randint(1, 7))
        ver = "{}.0.{}".format(randint(4, 5), randint(1, 5)) if getrandbits(1) else "{}.{}".format(randint(4, 5),
                                                                                                   randint(0, 1))
        locale = self.__locale()
        platforms = (
            '(Windows; U; {}) AppleWebKit/{} (KHTML, like Gecko) Version/{} Safari/{}'.format(self.__windows_token(),
                                                                                              saf,
                                                                                              ver,
                                                                                              saf),
            '({} rv:{}.0; {}) AppleWebKit/{} (KHTML, like Gecko) Version/{} Safari/{}'.format(self.__mac_token(),
                                                                                              randint(2, 6),
                                                                                              locale,
                                                                                              saf,
                                                                                              ver,
                                                                                              saf),
        )
        return 'Mozilla/5.0 {}'.format(choice(platforms))

    def firefox(self):
        ver = (
            'Gecko/{} Firefox/3.8'.format(self.__get_date_between('2010-01-01').isoformat().replace('-', '')),
            'Gecko/{} Firefox/{}.0'.format(self.__get_date_between('2011-01-01').isoformat().replace('-', ''),
                                           randint(4, 15)),
            'Gecko/{} Firefox/3.6.{}'.format(self.__get_date_between('2010-01-01').isoformat().replace('-', ''),
                                             randint(1, 20)),
        )
        platforms = (
            '({}; rv:1.9.{}.20) {}'.format(self.__mac_token(), randint(2, 6), choice(ver)),
            '({}; rv:1.9.{}.20) {}'.format(self.__linux_token(), randint(5, 7), choice(ver)),
            '({}; {}; rv:1.9.{}.20) {}'.format(self.__windows_token(), self.__locale(), randint(0, 2), choice(ver))
        )
        return 'Mozilla/5.0 {}'.format(choice(platforms))

    @property
    def types(self):
        return self.__types

    def __locale(self):
        key = choice(list(self.__language_locale_codes.keys()))
        return '{}-{}'.format(key, choice(self.__language_locale_codes.get(key)))

    @staticmethod
    def __get_date_between(start, end='today'):
        """Get a date between "start" and "end".
        :param start: start date. Type: datetime.date or ISO format string.
        :param end: end date. Type: datetime.date or ISO format string. Default value: "today".
        :rtype: datetime.date or None.
        """
        if 'today' == end:
            end = date.today()
        try:
            if isinstance(start, str):
                start = date.fromisoformat(start)
            if isinstance(end, str):
                end = date.fromisoformat(end)
        except ValueError:
            pass
        if isinstance(start, date) and isinstance(end, date) and end >= start:
            # Generate year
            year = randint(start.year, end.year)
            # Generate month
            if start.year == end.year:
                month = randint(start.month, end.month)
            elif start.year == year:
                month = randint(start.month, 12)
            elif end.year == year:
                month = randint(1, end.month)
            else:
                month = randint(1, 12)
            # Generate day
            if start.year == end.year and start.month == end.month:
                day = randint(start.day, end.day)
            elif start.year == year and start.month == month:
                if 2 == month:
                    day = randint(start.day, 29) if isleap(year) else randint(start.day, 28)
                elif month in (4, 6, 9, 11):
                    day = randint(start.day, 30)
                else:
                    day = randint(start.day, 31)
            elif end.year == year and end.month == month:
                day = randint(1, end.day)
            else:
                if 2 == month:
                    day = randint(1, 29) if isleap(year) else randint(1, 28)
                elif month in (4, 6, 9, 11):
                    day = randint(1, 30)
                else:
                    day = randint(1, 31)
            return date(year, month, day)
        return None

    def __windows_token(self):
        return choice(self.__windows_versions)

    def __linux_token(self):
        return 'X11; Linux {}'.format(choice(self.__linux_processors))

    def __mac_token(self):
        return 'Macintosh; {} Mac OS X 10_{}_{}'.format(choice(self.__mac_processors), randint(5, 12), randint(0, 9))
