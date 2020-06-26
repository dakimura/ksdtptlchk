# -*- coding: utf-8 -*-

from io import open
from setuptools import setup, find_packages

with open('README.md', encoding="utf-8") as f:
    readme = f.read()

with open('LICENSE', encoding="utf-8") as f:
    license = f.read()

setup(
    name="ksdtptlchk",
    version="1.0.0",
    description="check updates on https://koto-kosodate-portal.jp/smf/mizube/general/refresh_cal.php?center_cd=60",
    author="Daito Akimura",
    #install_requires=["pip @ git+https://github.com/dakimura/pymarketstore.git@2029ff6830596c96f7dba3e0e497127c687f1870#egg=pymarketstore", "argparse", ],
    install_requires = list(f.read().splitlines()),
    packages=find_packages(exclude=('tests', 'docs')),
    entry_points={
        "console_scripts": [
            "ksdtptlchk = ksdtptlchk.app:main",
        ]
    }
)
