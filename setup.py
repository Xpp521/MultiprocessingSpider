from os import getcwd
from os.path import join, dirname
from setuptools import setup, find_packages

# Module name
NAME = 'MultiprocessingSpider'

# Root directory
ROOT = dirname(__file__)

# Load README.md
try:
    with open(join(ROOT, 'README.md'), encoding='utf') as f:
        README = f.read()
except IOError:
    README = ''

# Load CHANGES.md
try:
    with open(join(ROOT, 'CHANGES.md'), encoding='utf') as f:
        CHANGES = f.read()
except IOError:
    CHANGES = ''

setup(
    name=NAME,
    version='1.0.0',
    description='A multiprocessing web crawling and web scraping framework.',
    long_description=README + CHANGES,
    long_description_content_type='text/markdown',
    author='Xpp',
    author_email='Xpp233@foxmail.com',
    url='https://github.com/Xpp521/MultiprocessingSpider',
    project_urls={
        'Documentation': 'https://github.com/Xpp521/MultiprocessingSpider/wiki',
        'Source': 'https://github.com/Xpp521/MultiprocessingSpider',
        'Tracker': 'https://github.com/Xpp521/MultiprocessingSpider/issues'
    },
    license='GPLv3',
    keywords=['crawler', 'spider', 'requests', 'multiprocessing'],
    packages=find_packages(getcwd()),
    python_requires='>=3',
    install_requires=['requests'],
    setup_requires=[],
    extras_require={},
    classifiers=[
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows NT/2000',
        'Operating System :: POSIX',
        'License :: OSI Approved :: GNU Lesser General Public License v3 '
        '(LGPLv3)',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
