from os.path import abspath, dirname, join

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

VERSION = None
version_file = join(dirname(abspath(__file__)), "Mainframe3270", "version.py")

with open(version_file) as file:
    code = compile(file.read(), version_file, "exec")
    exec(code)

with open("README.md", encoding="utf-8") as file:
    long_description = file.read()


package_kwargs = {
    "name": "robotframework-mainframe3270",
    "version": VERSION,
    "description": "Mainframe Test library for Robot Framework",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "author": "Altran Portugal",
    "author_email": "samuca@gmail.com",
    "license": "MIT License",
    "license_files": ["LICENSE.md", "THIRD-PARTY-NOTICES.txt"],
    "url": "https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library",
    "packages": ["Mainframe3270"],
    "install_requires": ["robotframework", "robotframework-pythonlibcore"],
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Framework :: Robot Framework",
        "Framework :: Robot Framework :: Library",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Testing :: Acceptance",
    ],
}

setup(**package_kwargs)
