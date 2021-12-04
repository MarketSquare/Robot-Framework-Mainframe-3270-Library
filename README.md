[![PyPi downloads](https://img.shields.io/pypi/dm/robotframework-mainframe3270.svg)](https://pypi.org/project/robotframework-mainframe3270/)
[![Total downloads](https://static.pepy.tech/personalized-badge/robotframework-mainframe3270?period=total&units=international_system&left_color=lightgrey&right_color=yellow&left_text=total)](https://pypi.org/project/robotframework-mainframe3270/)
[![Latest Version](https://img.shields.io/pypi/v/robotframework-mainframe3270.svg)](https://pypi.org/project/robotframework-mainframe3270/)

# Mainframe3270Library

## Introduction

Mainframe3270 is a library for Robot Framework based on [py3270 project](https://pypi.org/project/py3270/), a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

## Installation

In order to use this library you need to install the [x3270 project](http://x3270.bgp.nu/download.html).

`pip install robotframework-mainframe3270`

### Windows

You need to install the [x3270 project](http://x3270.bgp.nu/index.html) and put the directory on your PATH. 

The default folder is "C:\Program Files\wc3270" and this needs to be in the PATH of the Environment Variables.

### Unix

You can install the x3270 project from [their instructions page](http://x3270.bgp.nu/Build.html#Unix). Or if it is available in your distribution through the `sudo apt-get install x3270`

More information on the [Wiki page](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/wiki/Installation) of this project.

## Example

    *** Settings ***
    Library           Mainframe3270

    *** Test Cases ***
    Example
        Open Connection    Hostname    LUname
        Change Wait Time    0.4
        Change Wait Time After Write    0.4
        Set Screenshot Folder    C:\\Temp\\IMG
        ${value}    Read    3    10    17
        Page Should Contain String    ENTER APPLICATION
        Wait Field Detected
        Write Bare    applicationname
        Send Enter
        Take Screenshot
        Close Connection

## Importing

Arguments:
   - visible = True
   - timeout = 30
   - wait_time = 0.5
   - wait_time_after_write = 0
   - img_folder = .
   - run_on_failure_keyword = Take Screenshot

You can change to hide the emulator screen set the argument visible=${False}

To change the wait_time see Change Wait Time, to change the img_folder
see the Set Screenshot Folder and to change the timeout see the Change Timeout keyword.

By default, Mainframe3270 will take a screenshot on failure. You can overwrite this to run any other keyword by setting the ``run_on_failure_keyword`` option. If you pass ``None`` to this argument, no keyword will be run.

## Running with Docker

Docker image contains everything that's needed to run the Mainframe tests. Currently image is not pushed to Docker hub, so steps to use it
* Build image:
  * Python 2: `docker image build --build-arg PYTHON_MAJOR=2 -t mainframe3270-p2 .`
  * Python 3: `docker image build --build-arg PYTHON_MAJOR=3 -t mainframe3270-p3 .`
- Run all tests: docker container run --rm -it mainframe3270-p<PYTHON_MAJOR>

Reports are stored to /reports. Those can be get to host by mapping it as volume. E.g. in Windows CMD with current directory mounting command is `docker container run --rm -it -v %cd%\reports:/reports mainframe3270-p<PYTHON_MAJOR>`

If wanting to run just single/specific tests, it can be mentioned at the end of command. Currently only single argument can be given, so multiple tests can be given with wildcards like: `docker container run --rm -it -v %cd%\reports:/reports mainframe3270-p<PYTHON_MAJOR> *PF*` (this executes just single tests, as PF is mentioned only in one).

When developing tests, also source code and tests can be mounted to container. Command to run tests using current sources with Python 3 (without need to recreate container all the time):
* Windows: `docker container run --rm -it -v %cd%\reports:/reports -v %cd%\tests:/tests -v %cd%\source:/usr/local/lib/python3.7/site-packages/Mainframe3270 mainframe3270-p3` (_reports_ -dir needs to be created beforehand)
* Linux/MacOSX: `docker container run --rm -it -v $(pwd)/reports:/reports -v $(pwd)/tests:/tests -v $(pwd)/source:/usr/local/lib/python3.7/site-packages/Mainframe3270 mainframe3270-p3`  

## Notes

By default the import set the visible argument to true, on this option the py3270 is running the wc3270.exe, but is you set the visible to false, the py3270 will run the ws3270.exe.

## Keyword Documentation

You can find the keywords documentation [here](https://raw.githack.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/doc/Mainframe3270.html)

## Keyword Tests

To run all the library tests, you will need to create a user in the https://www.pub400.com/ website.

## WIKI
For more information visit this repository [Wiki](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/wiki).

## Authors
   - **Altran -** [Altran Web Site](https://www.altran.com/us/en/)
   - **Samuel Cabral**
   - **Joao Gomes**
   - **Bruno Calado**
   - **Ricardo Morgado**
   
## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/blob/master/LICENSE.md) file for details.
