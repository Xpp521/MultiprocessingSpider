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
# ROOT = dirname(CUR_DIR)
ROOT = CUR_DIR

# Module name
MODULE_NAME = ''

# Version
VERSION = ''

# Load module name and version
with open(join(ROOT, 'setup.py')) as f:
    for line in f.readlines():
        if line.startswith('NAME'):
            line = line.strip().replace(' ', '').replace('"', '').replace("'", '')
            MODULE_NAME = line.split('=')[-1]
        elif line.startswith('VERSION'):
            line = line.strip().replace(' ', '').replace('"', '').replace("'", '')
            VERSION = line.split('=')[-1]
        if MODULE_NAME and VERSION:
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
    """Remove the old version."""
    remove_paths([join(ROOT, 'build'), join(ROOT, 'dist'), join(ROOT, '{}.egg-info'.format(MODULE_NAME))])


def pack():
    """Package new version."""
    print(exec_cmd(executable, join(ROOT, 'setup.py'), 'sdist', 'bdist_wheel'))
    for p in listdir(CUR_DIR):
        if p in ('build', 'dist', '{}.egg-info'.format(MODULE_NAME)):
            move(join(CUR_DIR, p), join(ROOT, p))


def check():
    """Check the current version."""
    print(exec_cmd('twine', 'check', join(ROOT, 'dist', '*')))


def install():
    """Install the current version."""
    wheel = ''
    for p in listdir('dist'):
        if p.startswith('{}-{}'.format(MODULE_NAME, VERSION)) and p.endswith('.whl'):
            wheel = join('dist', p)
            break
    if wheel:
        print(exec_cmd('pip', 'uninstall', '-y', MODULE_NAME))
        print(exec_cmd('pip', 'install', wheel))
    else:
        raise FileNotFoundError('wheel file does not exist')


def upload():
    """Upload the current version to PYPI."""
    print(exec_cmd('twine', 'upload', join(ROOT, 'dist', '*')))


def main():
    note = '''Packing tool

Usage:
\t1. pack d:\t\tDelete the old version.

\t2. pack p:\t\tPackage new version.

\t3. pack i:\t\tInstall the current version.

\t3. pack u:\t\tUpload the current version.

'''
    if 2 != len(argv):
        print(note)
        return
    operation = argv[1]
    if 'd' == operation:
        clean()
    elif 'p' == operation:
        clean()
        pack()
        check()
    elif 'i' == operation:
        install()
    elif 'u' == operation:
        if 'y' == input('Upload to PYPI (y/n)? '):
            upload()
    else:
        print(note)


if __name__ == '__main__':
    main()
