"""API"""

import os
from setuptools import find_packages, setup

readme = open('README.rst').read()

tests_require = [
    'coverage>=4.5',
    'coveralls>=1.8',
    'pytest>=5.2',
    'pytest-cov>=2.8',
    'pytest-pep8>=1.0',
    'isort>4.3'
]

extras_require = {
    'tests': tests_require,
}

extras_require['all'] = [ req for exts, reqs in extras_require.items() for req in reqs ]

setup_requires = [
    'pytest-runner>=5.2',
]

install_requires = [
    'Flask>=1.1.1',
    'flask_restplus>=0.13.0',
    'Flask-Cors==3.0.8',
    'Flask-JWT==0.3.2',
    'Flask-RESTful==0.3.6',
    'Flask-Migrate>=2.5.2',
    'Flask-SQLAlchemy>=2.4.1',
    'SQLAlchemy[postgresql]>=1.3.10',
    'SQLAlchemy-Utils>=0.34.2',
    'Werkzeug==0.16.1',
    'requests>=2.20.0',
    'marshmallow>=2.15.2',
    'cerberus==1.3.1',
    'flask-redoc==0.1.0',
    'beautifulsoup4==4.9.1',
    'pandas==1.0.4'
]

packages = find_packages()

with open(os.path.join('api', 'version.py'), 'rt') as fp:
    g = {}
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='api-worker-finance',
    version=version,
    long_description=readme,
    author='Beto Noronha',
    author_email='beto_noronha@live.com',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'worker-finance = api.cli:cli'
        ]
    }
)