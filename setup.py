# -*- coding: utf-8 -*-
import os.path
import setuptools

project_name = 'env_var_config'
version = '0.1.0'

setup_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(setup_dir, 'README.rst')) as readme_file:
    readme = readme_file.read()

setuptools.setup(
    name=project_name,
    version=version,
    description='Parsing configuration from environment variables as typing.NamedTuple',
    long_description=readme,
    url='https://github.com/iteriodata/env_var_config',
    packages=setuptools.find_packages(exclude=['tests']),
    license="MIT",
    keywords='config env var',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/iteriodata/env_var_config/issues',
        'Source': 'https://github.com/iteriodata/env_var_config',
    }
)
