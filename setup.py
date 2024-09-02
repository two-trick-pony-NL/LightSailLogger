# setup.py

from setuptools import setup, find_packages

setup(
    name='LightSail Loger',
    version='0.1',
    packages=find_packages(),
    install_requires=[],  # Add your dependencies here
    author='Peter van Doorn',
    author_email='peter@petervandoorn.com',
    description='A simple logger that combines AWS Lightsail containerlogs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/mypackage',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
