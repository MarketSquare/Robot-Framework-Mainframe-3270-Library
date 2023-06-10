*** Settings ***
Library             Collections
Library             OperatingSystem
Library             ../../Mainframe3270/
Library             modellibrary.py
Resource            ../pub400_variables.robot

Test Teardown       Test Teardown


*** Test Cases ***
Model Should Default To 2
    Open Connection    ${HOST}
    Emulator Model Should Be    2

Open Connection Can Override Model
    Open Connection    ${HOST}    extra_args=["-xrm", "*model: 4"]
    Emulator Model Should Be    4

Can Use Different Models In Different Sessions
    Open Connection    ${HOST}    extra_args=["-xrm", "*model: 5"]
    Emulator Model Should Be    5
    Sleep    3 s
    Open Connection    ${HOST}    extra_args=["-xrm", "*model: 4"]
    Emulator Model Should Be    4


*** Keywords ***
Test Teardown
    Close All Connections
    Sleep    3 s
