*** Settings ***
Library             ../Mainframe3270/
Library             OperatingSystem
Resource            pub400_variables.robot
Suite Setup         Suite Mainframe Setup
Suite Teardown      Close Connection


*** Test Cases ***
Test Wait Field
    Wait Field Detected
    ${read_text}    Read    1    10    21
    Log    ${read_text}    warn

Test Screenshot Png
    Sleep    1
    Take Screenshot    img=${True}

Test Screenshot Png Edge
    Sleep    1
    Take Screenshot    img=${True}    browser=edge

Test Screenshot Html
    Write Bare    HTML
    Sleep    1
    Take Screenshot


*** Keywords ***
Suite Mainframe Setup
    Open Connection    ${HOST}
    Change Wait Time    1
    Change Wait Time After Write    1.4