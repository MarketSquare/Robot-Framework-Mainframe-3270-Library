[![PyPi downloads](https://img.shields.io/pypi/dm/robotframework-mainframe3270.svg)](https://pypi.org/project/robotframework-mainframe3270/)
[![Total downloads](https://static.pepy.tech/personalized-badge/robotframework-mainframe3270?period=total&units=international_system&left_color=lightgrey&right_color=yellow&left_text=total)](https://pypi.org/project/robotframework-mainframe3270/)
[![Latest Version](https://img.shields.io/pypi/v/robotframework-mainframe3270.svg)](https://pypi.org/project/robotframework-mainframe3270/)
[![tests](https://github.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/actions/workflows/run-tests.yml/badge.svg?branch=master)](https://github.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/actions/workflows/run-tests.yml)
[![codecov](https://codecov.io/gh/MarketSquare/Robot-Framework-Mainframe-3270-Library/branch/master/graph/badge.svg?token=N41G62D883)](https://codecov.io/gh/MarketSquare/Robot-Framework-Mainframe-3270-Library)

# Mainframe3270Library

## Introduction

Mainframe3270 is a library for Robot Framework based on the [py3270 project](https://pypi.org/project/py3270/), a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

## Compatibility
Mainframe3270 requires Python 3. It is tested with Python 3.8 and 3.12, but should support all versions in between these.

## Installation

In order to use this library, first install the package from [PyPI](https://pypi.org/project/robotframework-mainframe3270/).
```commandline
pip install robotframework-mainframe3270
```

Or you can upgrade with:
```commandline
pip install --upgrade robotframework-mainframe3270
```

Then, depending on your OS, proceed with the corresponding chapters in this README.

### Windows

You need to install the [x3270 project](http://x3270.bgp.nu/index.html) and put the directory on your PATH.

The default folder is "C:\Program Files\wc3270". This needs to be in the `PATH` environment variable.

### Unix

You can install the x3270 project from [the instructions page](http://x3270.bgp.nu/Build.html#Unix). Or if it is available in your distribution through:
```commandline
sudo apt-get install x3270
```
or
```commandline
brew install x3270
```

More information can be found on the [Wiki page](https://github.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/wiki/Installation) of this project.

## Example
```RobotFramework
*** Settings ***
Library    Mainframe3270

*** Test Cases ***
Example
    Open Connection    Hostname    LUname
    Change Wait Time    0.4 seconds
    Change Wait Time After Write    0.4 seconds
    Set Screenshot Folder    C:\\Temp\\IMG
    ${value}    Read    3    10    17
    Page Should Contain String    ENTER APPLICATION
    Wait Field Detected
    Write Bare    applicationname
    Send Enter
    Take Screenshot
    Close Connection
```

## Keyword Documentation

You can find the keyword documentation [here](https://raw.githack.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/master/doc/Mainframe3270.html).

## Running with Docker

The Docker image contains everything that is needed to run Mainframe tests. Currently the image is not published to Docker Hub. In order to use it, perform the following steps.

1. Download the Dockerfile sources
```sh
curl -O https://raw.githubusercontent.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/master/Dockerfile

curl -O https://raw.githubusercontent.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/master/entrypoint.sh
```

2. Build the image:
```sh
docker build -t mainframe3270 .
```

3. Run the container
```sh
docker run --user mfuser -v /path/to/your/tests:/home/mfuser/tests mainframe3270 robot /home/mfuser/tests
```

## Contributing to Robot-Framework-Mainframe3270-Library

Interested in contributing to the project? Great to hear! Whether you found a bug, or want to develop a new feature, please refer to our [Contributing Guidelines](https://github.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/blob/master/CONTRIBUTING.md) to help you get started.

## Wiki
For more information visit the repository [Wiki](https://github.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/wiki).

## Changelog
For an overview of the (latest) changes see [CHANGELOG](https://github.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/blob/master/CHANGELOG.md).

## Authors
Initial development was sponsored by [Capgemini Engineering](https://www.capgemini.com/about-us/who-we-are/our-brands/capgemini-engineering/)
   - **Samuel Cabral**
   - **Joao Gomes**
   - **Bruno Calado**
   - **Ricardo Morgado**

## Maintainers
   - **Robin Matz**

## License
This project is licensed under the MIT License - see [LICENSE](https://github.com/MarketSquare/Robot-Framework-Mainframe-3270-Library/blob/master/LICENSE.md) for details.
