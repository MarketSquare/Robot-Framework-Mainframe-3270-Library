*** Settings ***
Library    ../Mainframe3270/    run_on_failure_keyword=None
Library    DebugLibrary

*** Variables ***
${host}           pub400.com


*** Test Cases ***
Test case
    Open Connection    ${HOST}
    Sleep    3
    Write Unicode Bare    ßßß
    Take Screenshot    img=${True}
    Write Unicode Bare    abc
    Take Screenshot
    [Teardown]    Close Connection
