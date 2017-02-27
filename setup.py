#setup.py

from setuptools import setup
import codecs
import os
import antscheduler

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='AntScheduler',
    version=antscheduler.__version__,
    description='Application for solving scheduling problems',
    long_description=long_description,
    url='https://github.com/pypa/sampleproject',
    author='mcalus3',
    author_email='marek.calus3@gmail.com',
    license='GPL-3.0',
    packages=['antscheduler'],
    package_dir={'antscheduler': 'antscheduler'},
    install_requires=['graphviz', 'PyQt5'],
    entry_points={
        'console_scripts': ['AntScheduler = antscheduler.__main__:main'],
    },
    keywords='job-shop graph scheduling',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',

    ]
)
