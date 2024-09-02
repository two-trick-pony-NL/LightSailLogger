from setuptools import setup, find_packages

setup(
    name="lightsaillogger",
    version="0.1.6",
    author="Peter van Doorn",
    author_email="peter@petervandoorn.com",
    description="Log all your lightsail containers in 1 log file",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/two-trick-pony-NL/LightSailLogger",  # Change to your project's URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
