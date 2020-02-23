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
"""
Packing tool.
"""
from os import listdir, remove
from shutil import rmtree, move
from sys import argv, executable
from subprocess import Popen, PIPE
from os.path import join, isfile, isdir, dirname


def exec_cmd(*args):
    """
    Executes a command.
    :param args: the command.
    :return: stdout of the command.
    :raises: RuntimeError.
    """
    res = Popen(args, stdout=PIPE, stderr=PIPE)
    stdout, stderr = res.communicate()
    if 0 != res.returncode:
        raise RuntimeError('Failed to execute <{}> ({}): {}'.format(args, res.returncode, stderr.decode('gbk')))
    else:
        return stdout.decode('gbk')


# The current directory
CUR_DIR = dirname(__file__)

# The root directory
ROOT = dirname(CUR_DIR)
ROOT = CUR_DIR

# Load main package name
with open(join(ROOT, 'setup.py')) as f:
    for line in f.readlines():
        if line.startswith('NAME'):
            line = line.strip().replace(' ', '').replace('"', '').replace("'", '')
            MAIN_PACKAGE_NAME = line.split('=')[-1]
            break


def remove_paths(paths):
    """Remove all directories and files in the given paths."""
    for p in paths:
        try:
            if isfile(p):
                print('Removing file: {}'.format(p))
                remove(p)
            elif isdir(p):
                print('Removing directory: {}'.format(p))
                rmtree(p, True)
        except FileNotFoundError:
            continue


def clean():
    """Remove old version."""
    remove_paths([join(ROOT, 'build'), join(ROOT, 'dist'), join(ROOT, '{}.egg-info'.format(MAIN_PACKAGE_NAME))])


def pack():
    """Package new version."""
    print(exec_cmd(executable, join(ROOT, 'setup.py'), 'sdist', 'bdist_wheel'))
    for p in listdir(CUR_DIR):
        if p in ('build', 'dist', '{}.egg-info'.format(MAIN_PACKAGE_NAME)):
            move(join(CUR_DIR, p), join(ROOT, p))


def check():
    """Check current version."""
    print(exec_cmd('twine', 'check', join(ROOT, 'dist', '*')))


def upload():
    """Upload current version to PYPI."""
    print(exec_cmd('twine', 'upload', join(ROOT, 'dist', '*')))


def main():
    note = '''Packing tool

Usage:


\t1. pack r:\t\tRemove old version.


\t2. pack p:\t\tPackage new version.


\t3. pack c:\t\tCheck current version.


\t4. pack u:\t\tUpload current version.


'''
    if 2 != len(argv):
        print(note)
        return
    operation = argv[1]
    if 'r' == operation:
        clean()
    elif 'p' == operation:
        pack()
    elif 'c' == operation:
        check()
    elif 'u' == operation:
        if 'y' == input('Upload to PYPI (y/n)? '):
            upload()
    else:
        print(note)


if __name__ == '__main__':
    main()
