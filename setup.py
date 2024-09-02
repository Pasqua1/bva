from setuptools import setup, find_packages

setup(
    name='bva',
    packages=find_packages(),
    version='0.1.0',
    description='Python3 BOVA HTTP API Connector',
    author='Alexander Voronkov',
    author_email='voronkov_743@mail.ru',
    url='https://github.com/Pasqua1/bva',
    keywords="bova api connector",
    install_requires=[
        "requests",
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6"
)
