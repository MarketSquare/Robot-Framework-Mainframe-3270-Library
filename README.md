[![PyPi downloads](https://img.shields.io/pypi/dm/robotframework-mainframe3270.svg)](https://pypi.org/project/robotframework-mainframe3270/)
[![Total downloads](https://static.pepy.tech/personalized-badge/robotframework-mainframe3270?period=total&units=international_system&left_color=lightgrey&right_color=yellow&left_text=total)](https://pypi.org/project/robotframework-mainframe3270/)
[![Latest Version](https://img.shields.io/pypi/v/robotframework-mainframe3270.svg)](https://pypi.org/project/robotframework-mainframe3270/)
[![tests](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/actions/workflows/run-tests.yml/badge.svg?branch=master)](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/actions/workflows/run-tests.yml)
[![codecov](https://codecov.io/gh/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/branch/master/graph/badge.svg?token=N41G62D883)](https://codecov.io/gh/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library)

# Mainframe3270Library

## Introduction

Mainframe3270 is a library for Robot Framework based on the [py3270 project](https://pypi.org/project/py3270/), a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

## Compatibility
Mainframe3270 requires Python 3. It is tested with Python 3.7 and 3.10, but should support all versions in between these.

## Installation

In order to use this library, first install the package from PyPI.
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

More information can be found on the [Wiki page](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/wiki/Installation) of this project.

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

You can find the keyword documentation [here](https://raw.githack.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/doc/Mainframe3270.html).

## Importing

Arguments:
   - visible = True
   - timeout = 30
   - wait_time = 0.5
   - wait_time_after_write = 0
   - img_folder = .
   - run_on_failure_keyword = Take Screenshot

By default the emulator visibility is set to visible=True.
In this case test cases are executed using wc3270 (Windows) or x3270 (Linux/MacOSX).
You can change this by setting visible=False. Then test cases are run using ws3720 (Windows) or s3270 (Linux/MacOS).
This is useful when test cases are run in a CI/CD-pipeline and there is no need for a graphical user interface.

Timeout, waits and screenshot folder are set on library import as shown above. However, they can be changed during runtime. To modify the ``wait_time``, see [Change Wait Time](https://raw.githack.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/doc/Mainframe3270.html#Change%20Wait%20Time),
to modify the ``img_folder``, see [Set Screenshot Folder](https://raw.githack.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/doc/Mainframe3270.html#Set%20Screenshot%20Folder),
and to modify the ``timeout``, see the [Change Timeout](https://raw.githack.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/doc/Mainframe3270.html#Change%20Timeout) keyword.
Timeouts support all available Robot Framework [time formats](https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#time-format).

By default, Mainframe3270 will take a screenshot on failure. You can overwrite this to run any other keyword by setting the ``run_on_failure_keyword`` option. If you pass ``None`` to this argument, no keyword will be run. To change the ``run_on_failure_keyword`` during runtime, see [Register Run On Failure Keyword](https://raw.githack.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/doc/Mainframe3270.html#Register%20Run%20On%20Failure%20Keyword).

## Running with Docker

The Docker image contains everything that is needed to run Mainframe tests. Currently the image is not published to Docker Hub. In order to use it, perform the following steps.

1. Download the Dockerfile sources
```sh
curl -O https://raw.githubusercontent.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/Dockerfile

curl -O https://raw.githubusercontent.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/entrypoint.sh
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

Interested in contributing to the project? Great to hear! Whether you found a bug, or want to develop a new feature, please refer to our [Contributing Guidelines](COUNTRIBUTING.md) to help you get started.

## Keyword Tests

To run all the library tests, you will need to create a user on the [pub400](https://www.pub400.com/) website.

## WIKI
For more information visit the repository [Wiki](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/wiki).

## Authors
   - **Altran -** [Altran Web Site](https://www.altran.com/us/en/)
   - **Samuel Cabral**
   - **Joao Gomes**
   - **Bruno Calado**
   - **Ricardo Morgado**

## License
This project is licensed under the MIT License - see [LICENSE.md](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/blob/master/LICENSE.md) for details.
