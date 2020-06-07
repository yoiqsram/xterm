import os
from setuptools import setup

from xterm import __version__


def read(fname, encoding='utf-8'):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding=encoding).read()


setup(name='xterm',
      version=__version__,
      author='Yoiq S Rambadian',
      author_email='yoiqrambadian@gmail.com',
      description='Styled input and output for xterm',
      long_description=read('README.md'),
      long_description_content_type='text/markdown',
      keywords='terminal',
      url='https://github.com/yoiqsram/xterm',
      packages=['xterm'])
