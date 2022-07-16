*** Settings ***
Library             ../../Mainframe3270/    img_folder=${CURDIR}
Library             OperatingSystem

Suite Setup         Open Mainframe
Suite Teardown      Close Mainframe


*** Variables ***
${custom_file}          ${CURDIR}${/}output.txt
${host}                 pub400.com
${not_found_string}     4%$3123


*** Test Cases ***
Takes Screenshot On Failure
    Cause Error
    File Should Exist    ${CURDIR}/*.html
    [Teardown]    Remove File    ${CURDIR}/*.html

Register Custom Keyword To Run On Failure
    Register Run On Failure Keyword    Custom Run On Failure Keyword
    Cause Error
    File Should Exist    ${custom_file}
    [Teardown]    Remove File    ${custom_file}

Register None To Run On Failure
    Register Run On Failure Keyword    None
    Cause Error
    File Should Not Exist    ${CURDIR}/*.html


*** Keywords ***
Open Mainframe
    Open Connection    ${host}
    Sleep    3 seconds

Cause Error
    Run Keyword And Expect Error
    ...    The string "${not_found_string}" was not found
    ...    Page Should Contain String    ${not_found_string}

Custom Run On Failure Keyword
    Create File    ${custom_file}    An error ocurred

Close Mainframe
    Close Connection
    Sleep    1 second
