# setup.py

from setuptools import setup, find_packages

setup(
    name='GlenAtom',
    version='0.1.0',
    author='KRTEY', # GitHub 사용자 이름으로 수정
    description='A post-processing tool for molecular dynamics simulations.',
    packages=find_packages(), # glenatom 폴더 안의 모든 .py 파일을 자동으로 패키지에 포함시키므로 setup.py는 수정할 필요가 없습니다.
    package_data={
        'glenatom': ['styles/*.mplstyle'],
    },
    install_requires=[
        'matplotlib',
        'numpy',
        'ase',
        'pandas',
        'scipy',
        'seaborn',
    ],
)