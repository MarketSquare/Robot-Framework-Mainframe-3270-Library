*** Settings ***
Library             ../../Mainframe3270/    run_on_failure_keyword=None
Library             OperatingSystem
Resource            ../pub400_variables.robot

Suite Setup         Open Connection    ${HOST}
Suite Teardown      Run Keyword And Ignore Error    Close Connection


*** Test Cases ***
None Should Run On Failure
    Cause Error
    File Should Not Exist    ${CURDIR}/*.html


*** Keywords ***
Cause Error
    Run Keyword And Expect Error
    ...    The string "${STRING_NON_EXISTENT}" was not found
    ...    Page Should Contain String    ${STRING_NON_EXISTENT}
