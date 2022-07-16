*** Settings ***
Library             ../../Mainframe3270/    run_on_failure_keyword=None
Library             OperatingSystem

Suite Setup         Open Mainframe
Suite Teardown      Close Mainframe


*** Variables ***
${custom_file}          ${CURDIR}${/}output.txt
${host}                 pub400.com
${not_found_string}     4%$3123


*** Test Cases ***
None Should Run On Failure
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

Close Mainframe
    Close Connection
    Sleep    1 second
