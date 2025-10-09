*** Settings ***
Library             ../../Mainframe3270/    img_folder=${CURDIR}
Library             OperatingSystem
Resource            ../pub400_variables.robot

Suite Setup         Open Connection    ${HOST}
Suite Teardown      Run Keyword And Ignore Error    Close Connection


*** Variables ***
${CUSTOM_FILE}      ${CURDIR}${/}output.txt


*** Test Cases ***
Takes Screenshot On Failure
    [Tags]    no-ci
    Cause Error
    File Should Exist    ${CURDIR}/*.html
    [Teardown]    Remove File    ${CURDIR}/*.html

Register Custom Keyword To Run On Failure
    Register Run On Failure Keyword    Custom Run On Failure Keyword
    Cause Error
    File Should Exist    ${CUSTOM_FILE}
    [Teardown]    Remove File    ${CUSTOM_FILE}

Register None To Run On Failure
    Register Run On Failure Keyword    None
    Cause Error
    File Should Not Exist    ${CURDIR}/*.html


*** Keywords ***
Cause Error
    Run Keyword And Expect Error
    ...    The string "${STRING_NON_EXISTENT}" was not found
    ...    Page Should Contain String    ${STRING_NON_EXISTENT}

Custom Run On Failure Keyword
    Create File    ${CUSTOM_FILE}    An error ocurred
