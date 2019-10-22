# -*- encoding: utf-8 -*-
from .x3270 import x3270
from .version import VERSION


class Mainframe3270(x3270):
    """Mainframe3270 is a library for Robot Framework based on [https://pypi.org/project/py3270/|py3270 project],
       a Python interface to x3270, an IBM 3270 terminal emulator. It provides an API to a x3270 or s3270 subprocess.

       = Installation  =
       
       For use this library you need to install the [http://x3270.bgp.nu/download.html|x3270 project]
       and put the directory on your PATH. On Windows, you need to download wc3270 and put
       the "C:\Program Files\wc3270" in PATH of the Environment Variables.

       = Notes  =

       By default the import set the visible argument to true, on this option the py3270 is running the wc3270.exe,
       but is you set the visible to false, the py3270 will run the ws3270.exe.

       = Example =

       | ***** Settings *****
       | Library           Mainframe3270
       | Library           BuiltIn
       |
       | ***** Test Cases *****
       | Example
       |     Open Connection    Hostname    LUname
       |     Change Wait Time    0.4
       |     Change Wait Time After Write    0.4
       |     Set Screenshot Folder    C:\\\Temp\\\IMG
       |     ${value}    Read    3    10    17
       |     Page Should Contain String    ENTER APPLICATION
       |     Wait Field Detected
       |     Write Bare    applicationname
       |     Send Enter
       |     Take Screenshot
       |     Close Connection
    """
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = VERSION
