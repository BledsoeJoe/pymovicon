from setuptools import setup, find_packages

requirements = []

with open('./requirements.txt', 'r') as file:
    for line in file.readlines():
        requirements.append(line.strip())

setup(
    name='pymovicon',
    version='0.1.0',
    packages=find_packages(),
    install_requires=requirements,
)
