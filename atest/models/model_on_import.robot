*** Settings ***
Library             ../../Mainframe3270/    model=4
Library             ../HelperLibrary.py
Resource            ../pub400_variables.robot

Test Teardown       Run Keyword And Ignore Error    Close Connection


*** Test Cases ***
Should Use Model From Import
    Open Connection    ${HOST}
    Emulator Model Should Be    4
