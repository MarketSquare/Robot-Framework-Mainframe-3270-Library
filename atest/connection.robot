*** Settings ***
Library             OperatingSystem
Library             ../Mainframe3270/
Resource            pub400_variables.robot

Test Teardown       Test Teardown


*** Variables ***
${ARGFILE}          ${CURDIR}/resources/argfile.txt
${TRACE_FILE}       ${CURDIR}/x3270.trace


*** Test Cases ***
Test Connection With Extra Args List
    ${extra_args}    Create List    -trace    -tracefile    ${TRACE_FILE}
    Open Connection    ${HOST}    extra_args=${extra_args}
    Sleep    0.5 s
    File Should Exist    ${TRACE_FILE}

Test Connection With Argfile
    Open Connection    ${HOST}    extra_args=${ARGFILE}
    Sleep    0.5 s
    File Should Exist    ${TRACE_FILE}


*** Keywords ***
Test Teardown
    Close Connection
    Sleep    1 second
    Remove File    ${TRACE_FILE}
