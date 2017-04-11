# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages


install_requires = [
    'github3.py>=1.0.0a4',
    'requests'
]


setup(
    name='whouses',
    description='Who uses my python module?',
    maintainer='Will Kahn-Greene',
    url='http://github.com/willkg/whouses',
    license='MPL v2',
    packages=find_packages(),
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        whouses=whouses.main:cmdline
    """,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
