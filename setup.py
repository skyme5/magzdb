#!/usr/bin/env python
"""The setup script."""
from setuptools import find_packages
from setuptools import setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("requirements.txt", "r") as file:
    requirements = [r for r in file.readlines() if len(r) > 0]

setup_requirements = []

test_requirements = ["pytest"].extend(requirements)

setup(
    author="Aakash Gajjar",
    author_email="skyqutip@gmail.com",
    python_requires=">=3.5",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Magzdb.org Downloader",
    entry_points={"console_scripts": ["magzdb=magzdb.cli:main",],},
    include_package_data=True,
    install_requires=requirements,
    keywords="magzdb",
    license="MIT license",
    long_description=readme + "\n\n" + history,
    name="magzdb",
    packages=find_packages(include=["magzdb", "magzdb.*"]),
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/skyme5/magzdb",
    version="0.1.0",
    zip_safe=False,
)
