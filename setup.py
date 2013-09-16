import re
from setuptools import setup, find_packages

file_text = open('sc/__init__.py').read()

def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval

setup(
    name='sc',
    version=grep('__version__'),
    author='Zach Kelling',
    author_email='zk@monoid.io',
    url='https://github.com/zeekay/sc',
    description='Soundcloud CLI app',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=['bin/sc'],
    install_requires=['soundcloud'],
)
