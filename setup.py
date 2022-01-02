
from setuptools import setup, find_packages
from bahamutexporter.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='bahamutexporter',
    version=VERSION,
    description='Exports floors and replies in Bahamut posts',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Yotsuba',
    author_email='happy819tw@gmail.com',
    url='https://github.com/Yooootsuba/bahamut-exporter',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'bahamutexporter': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        bahamutexporter = bahamutexporter.main:main
    """,
)
