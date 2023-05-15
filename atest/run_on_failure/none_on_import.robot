*** Settings ***
Library             ../../Mainframe3270/    run_on_failure_keyword=None
Library             OperatingSystem
Resource            ../pub400_variables.robot

Suite Setup         Open Mainframe
Suite Teardown      Close Mainframe


*** Test Cases ***
None Should Run On Failure
    Cause Error
    File Should Not Exist    ${CURDIR}/*.html


*** Keywords ***
Open Mainframe
    Open Connection    ${HOST}
    Sleep    3 seconds

Cause Error
    Run Keyword And Expect Error
    ...    The string "${STRING_NON_EXISTENT}" was not found
    ...    Page Should Contain String    ${STRING_NON_EXISTENT}

Close Mainframe
    Run Keyword And Ignore Error    Close Connection
    Sleep    1 second
