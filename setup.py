# setup.py

from setuptools import setup, find_packages

setup(
    name='GlenAtom',
    version='0.1.0',
    author='KRTEY', # GitHub 사용자 이름으로 수정
    description='A post-processing tool for molecular dynamics simulations.',
    packages=find_packages(),
    package_data={
        'glenatom': ['styles/*.mplstyle'],
    },
    install_requires=[
        'matplotlib',
        'numpy',
        'ase',
    ],
)