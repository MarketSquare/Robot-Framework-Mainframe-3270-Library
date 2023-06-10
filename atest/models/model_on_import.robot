*** Settings ***
Library             ../../Mainframe3270/    model=4
Library             modellibrary.py
Resource            ../pub400_variables.robot

Test Teardown       Test Teardown


*** Test Cases ***
Should Use Model From Import
    Open Connection    ${HOST}
    Emulator Model Should Be    4


*** Keywords ***
Test Teardown
    Close All Connections
    Sleep    3 s
