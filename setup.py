import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="trois",
    version="0.1",
    description="A matching card game.",
    long_description=read('README.md'),
    author="Christopher Snow",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'twisted',
        'autobahn',
        'environs'
    ],
    extras_require={
        'test': ["pytest", "tox", "hypothesis"],
    },
    entry_points={
        'console_scripts': [
            'trois = trois.trois:run_server'
        ]
    }
)
