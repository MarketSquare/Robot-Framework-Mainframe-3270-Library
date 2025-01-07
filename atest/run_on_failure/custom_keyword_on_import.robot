*** Settings ***
Library             OperatingSystem
Library             ../../Mainframe3270/    run_on_failure_keyword=Custom Run On Failure Keyword
Library             ../HelperLibrary.py
Resource            ../pub400_variables.robot

Suite Setup         Open Connection    ${HOST}    extra_args=["-utf8"]
Suite Teardown      Run Keyword And Ignore Error    Close Connection


*** Variables ***
${CUSTOM_FILE}      ${CURDIR}${/}output.txt


*** Test Cases ***
Should Run Custom Keyword
    Cause Error
    File Should Exist    ${CUSTOM_FILE}
    [Teardown]    Remove File    ${CUSTOM_FILE}


*** Keywords ***
Cause Error
    Run Keyword And Expect Error
    ...    The string "${STRING_NON_EXISTENT}" was not found
    ...    Page Should Contain String    ${STRING_NON_EXISTENT}

Custom Run On Failure Keyword
    Create File    ${CUSTOM_FILE}    An error ocurred
