*** Settings ***
Resource            pub400_variables.robot
Library             OperatingSystem
Library             ../Mainframe3270/    ${VISIBLE}
Library             HelperLibrary.py

Test Teardown       Test Teardown


*** Variables ***
${ARGFILE}              ${CURDIR}/resources/argfile.txt
${SESSION_TEMPLATE}     ${CURDIR}/resources/session.template
${TRACE_FILE}           ${CURDIR}/x3270.trace


*** Test Cases ***
Test Connection With Extra Args List
    ${extra_args}=    Create List    -port    992    -trace    -tracefile    ${TRACE_FILE}
    Open Connection    L:${HOST}    extra_args=${extra_args}
    File Should Exist    ${TRACE_FILE}

Test Connection With Argfile
    Open Connection    ${HOST}    extra_args=${ARGFILE}
    File Should Exist    ${TRACE_FILE}

Test Connection From Session File
    ${session_file}=    Create Session File    *hostname: L:pub400.com    *port: 992
    Open Connection From Session File    ${SESSION_FILE}
    Wait Field Detected
    Page Should Contain String    ${WELCOME}

Test Concurrent Connections
    Open Connection    ${HOST}    alias=first
    Write Bare    ABCD
    Page Should Contain String    ABCD
    Open Connection    ${HOST}    alias=second
    Write Bare    DEFG
    Page Should Contain String    DEFG
    Page Should Not Contain String    ABCD
    Switch Connection    first
    Page Should Contain String    ABCD
    Page Should Not Contain String    DEFG
    [Teardown]    Close All Connections


*** Keywords ***
Test Teardown
    Run Keyword And Ignore Error    Close Connection
    Remove File    ${TRACE_FILE}
