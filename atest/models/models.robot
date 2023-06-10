*** Settings ***
Library             ../../Mainframe3270/
Library             ../HelperLibrary.py
Resource            ../pub400_variables.robot

Test Teardown       Run Keyword And Ignore Error    Close All Connections


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
    Sleep    0.5 s
    Open Connection    ${HOST}    extra_args=["-xrm", "*model: 4"]
    Emulator Model Should Be    4
