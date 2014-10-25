import re
from setuptools import setup, find_packages

file_text = open('soundcloud_cli/__init__.py').read()

def grep(attrname):
    pattern = r"{0}\W*=\W*'([^']+)'".format(attrname)
    strval, = re.findall(pattern, file_text)
    return strval

setup(
    name='soundcloud-cli',
    version=grep('__version__'),
    author='Zach Kelling',
    author_email='zk@monoid.io',
    url='https://github.com/zeekay/soundcloud-cli',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    scripts=['bin/sc', 'bin/soundcloud-cli'],
    install_requires=['soundcloud'],
    license='MIT',
    description='Soundcloud command-line utility',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',

        'License :: OSI Approved :: MIT License',
    ],
    keywords='commandline cli soundcloud music upload utility',
)
