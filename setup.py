from setuptools import find_packages, setup
setup(
    name='validationlib',
    packages=find_packages(include=['validationlib']),
    version='0.1.0',
    description='POSRocket Task',
    author='Olga Hijazin',
    license='MIT',
    install_requires=[
        'beautifulsoup4==4.9.3',
        'bs4==0.0.1',
        'lxml==4.6.3',
        'soupsieve==2.2.1',
    ],
)