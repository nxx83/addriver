                                        

#!/usr/bin/env python # 
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='adriver-bs-category',
        version='0.0.3',
    packages = find_packages(),
        url='https://git.x/stats/categories_eater',
    include_package_data=True,
    install_requires=[
        'configparser==3.5.0',
	'falcon==2.0.0',
	'flake8==3.0.4',
	'pathlib2==2.1.0',
	'PyYAML==3.12',
	'requests==2.13.0',
	'simplejson==3.10.0',
	'six==1.11.0',
	'tld==0.12.6',
	'urllib3==1.19.1',
	'yml==0.0.1',
    ],

)
