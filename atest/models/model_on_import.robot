*** Settings ***
Library             ../../Mainframe3270/    model=4
Library             ModelLibrary.py
Resource            ../pub400_variables.robot

Test Teardown       Close Connection


*** Test Cases ***
Should Use Model From Import
    Open Connection    ${HOST}
    Emulator Model Should Be    4
