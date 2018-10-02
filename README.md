# Mainframe3270Library

## Introduction

Mainframe3270 is a library for Robot Framework based on py3270 project, a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

## Instalation

For use this library you need to install the x3270 project and put the directory on your PATH. On Windows, you need to download wc3270 and put the "C:\Program Files\wc3270" in PATH of the Environment Variables.
Notes

By default the import set the visible argument to true, on this option the py3270 is running the wc3270.exe, but is you set the visible to false, the py3270 will run the ws3270.exe.

## Example

    *** Settings ***
    Library           Mainframe3270
    Library           BuiltIn

    *** Test Cases ***
    Example
        Open Connection    Hostname    LUname
        Change Wait Time    0.9
        Set Screenshot Folder    C:\\Temp\\IMG
        ${value}    Read    3    10    17
        Should Be Equal As Strings    ${value}    ENTER APPLICATION
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