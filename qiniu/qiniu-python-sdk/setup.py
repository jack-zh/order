from setuptools import setup, find_packages
from setuptools.command.test import test


class TestCommand(test):
    def run(self):
        from tests.runtests import runtests
        runtests()

setup(
    name='qiniu-python-sdk',
    version='0.1',
    description='Qiniu Cloud Storage python SDK',
    long_description=open('README.md').read(),
    author='chzyer',
    author_email='me@chenye.org',
    url='https://github.com/Beeblio/python-sdk',
    packages=find_packages(exclude=['qiniu-logo.jpeg', 'demo.py']),
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Multimedia :: Graphics',
        'Framework :: Any',
    ],
    cmdclass={"test": TestCommand},
)
