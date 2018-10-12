# Mainframe3270Library

## Introduction

Mainframe3270 is a library for Robot Framework based on [py3270 project](https://pypi.org/project/py3270/), a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

## Instalation

In order to use this library you need to install the [x3270 project](http://x3270.bgp.nu/download.html). More information on the [Wiki page](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/wiki/Instalation) of this project.

## Notes

By default the import set the visible argument to true, on this option the py3270 is running the wc3270.exe, but is you set the visible to false, the py3270 will run the ws3270.exe.

## Example

    *** Settings ***
    Library           Mainframe3270

    *** Test Cases ***
    Example
        Open Connection    Hostname    LUname
        Change Wait Time    0.9
        Set Screenshot Folder    C:\\Temp\\IMG
        ${value}    Read    3    10    17
        Page Should Contain String    ENTER APPLICATION
        Write Bare    applicationname
        Send Enter
        Take Screenshot
        Close Connection

## Importing

Arguments:
   - visible = True
   - timeout = 30
   - wait_time = 0.5
   - img_folder = . 	

You can change to hide the emulator screen set the argument visible=${False}

To change the wait_time see Change Wait Time, to change the img_folder see the Set Screenshot Folder and to change the timeout see the Change Timeout keyword.

## Keyword Documentation

You can find the keywords documentation [here](https://rawgit.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/master/doc/documentation.html)

## WIKI
For more information visit this repository [Wiki](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/wiki).

## Authors
   - **Altran -** [Altran Web Site](https://www.altran.com/us/en/)
   - **Samuel Cabral**
   - **Joao Gomes**
   - **Bruno Calado**
   - **Ricardo Morgado**
   
## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Altran-PT-GDC/Robot-Framework-Mainframe-3270-Library/blob/master/LICENSE) file for details.
