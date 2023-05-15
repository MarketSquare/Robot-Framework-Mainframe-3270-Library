*** Settings ***
Documentation       These tests verify that all keywords are working correctly and displaying the expected exception messages.

Library             ../Mainframe3270/    run_on_failure_keyword=None
Library             OperatingSystem
Library             String
Resource            pub400_variables.robot

Suite Setup         Suite Setup
Suite Teardown      Suite Teardown


*** Test Cases ***
Exception Test Read
    Wait Field Detected
    ${read_text}    Read    1    10    21
    Run Keyword And Expect Error
    ...    ${WELCOME_TEXT_EXPECTED_ERROR}
    ...    Should Be Equal As Strings
    ...    ${WELCOME_TITLE}
    ...    ${read_text}
    Run Keyword And Expect Error    ${X_AXIS_EXCEEDED_EXPECTED_ERROR}    Read    4    48    34
    Run Keyword And Expect Error    ${X_AXIS_EXCEEDED_EXPECTED_ERROR}    Read    4    81    1
    Run Keyword And Expect Error    ${Y_AXIS_EXCEEDED_EXPECTED_ERROR}    Read    25    48    34

Exception Test Write In Position
    Run Keyword And Expect Error    ${X_AXIS_EXCEEDED_EXPECTED_ERROR}    Write In Position    ${WRITE_TEXT}    10    81
    Run Keyword And Expect Error    ${Y_AXIS_EXCEEDED_EXPECTED_ERROR}    Write In Position    ${WRITE_TEXT}    25    10

Exception Test Write Bare In Position
    Run Keyword And Expect Error
    ...    ${X_AXIS_EXCEEDED_EXPECTED_ERROR}
    ...    Write Bare In Position
    ...    ${WRITE_TEXT}
    ...    10
    ...    81
    Run Keyword And Expect Error
    ...    ${Y_AXIS_EXCEEDED_EXPECTED_ERROR}
    ...    Write Bare In Position
    ...    ${WRITE_TEXT}
    ...    25
    ...    10

Exception Test Page Should Contain String
    Verify String Not Found    Page Should Contain String    ${WELCOME_WRONG_CASE}
    Verify String Not Found    Page Should Contain String    ${STRING_NON_EXISTENT}    ignore_case=${True}

Exception Test Page Should Contain All Strings
    Verify String Not Found In List    Page Should Contain All Strings    ${LIST_STRINGS_WRONG_CASE_IN_THE_FIRST}    1
    Verify String Not Found In List
    ...    Page Should Contain All Strings
    ...    ${LIST_STRINGS_WRONG_CASE_IN_THE_SECONDS}
    ...    2
    Verify String Not Found In List    Page Should Contain All Strings    ${LIST_STRINGS_WRONG_CASE_IN_THE_THIRD}    3
    Verify String Not Found In List
    ...    Page Should Contain All Strings
    ...    ${LIST_STRINGS_WRONG_IN_THE_FIRST}
    ...    1
    ...    ignore_case=${True}
    Verify String Not Found In List
    ...    Page Should Contain All Strings
    ...    ${LIST_STRINGS_WRONG_IN_THE_SECOND}
    ...    2
    ...    ignore_case=${True}
    Verify String Not Found In List
    ...    Page Should Contain All Strings
    ...    ${LIST_STRINGS_WRONG_IN_THE_THIRD}
    ...    3
    ...    ignore_case=${True}

Exception Test Page Should Contain Any String
    Verify List Not Found    Page Should Contain Any String    ${LIST_STRINGS_ALL_WRONG_CASE}
    Verify List Not Found
    ...    Page Should Contain Any String
    ...    ${LIST_STRINGS_NON_EXITENT_IGNORE_CASE}
    ...    ignore_case=${True}

Exception Test Page Should Contain Match
    Verify Pattern Not Found    Page Should Contain Match    ${TEXT_NOT_MATCH_WRONG_CASE}
    Verify Pattern Not Found    Page Should Contain Match    ${STRING_NON_EXISTENT}    ignore_case=${True}

Exception Test Page Should Contain String X Times
    Verify String Does Not Appear X Times    Page Should Contain String X Times    ${TEXT_TO_COUNT}    1    3
    Verify String Does Not Appear X Times
    ...    Page Should Contain String X Times
    ...    ${TEXT_TO_COUNT_WRONG_CASE}
    ...    1
    ...    5
    ...    ignore_case=${True}

Exception Test Page Should Match Regex
    Verify Pattern Not Found    Page Should Match Regex    ${INVALID_REGEX}

Exception Test Page Should Not Contain String
    Verify String Found    Page Should Not Contain String    ${WELCOME}
    Verify String Found    Page Should Not Contain String    ${WELCOME_WRONG_CASE}    ignore_case=${True}

Exception Test Page Should Not Contain All Strings
    Verify List Found    Page Should Not Contain All Strings    ${LIST_STRINGS_RIGHT_IN_THE_FIRST}    1
    Verify List Found    Page Should Not Contain All Strings    ${LIST_STRINGS_RIGHT_IN_THE_SECOND}    2
    Verify List Found    Page Should Not Contain All Strings    ${LIST_STRINGS_RIGHT_IN_THE_THIRD}    3

Exception Test Page Should Not Contain Any String
    Verify List Found    Page Should Not Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_FIRST}    1
    Verify List Found    Page Should Not Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_SECOND}    2
    Verify List Found    Page Should Not Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_THIRD}    3

Exception Test Wait Until String
    Verify Wait Until String    Wait Until String    ${STRING_NON_EXISTENT}

Exception Test Wait Until String With Timeout
    Verify Wait Until String With Timeout    Wait Until String    ${STRING_NON_EXISTENT}    timeout=2

Test Wait Until String
    Wait Until String    ${WELCOME_TITLE}    timeout=4

Test Page Should Contain All Strings
    Page Should Contain All Strings    ${LIST_STRINGS}
    Page Should Contain All Strings    ${LIST_STRINGS_WRONG_CASE}    ignore_case=${True}

Test Page Should Contain Any String
    Page Should Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_FIRST}
    Page Should Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_SECOND}
    Page Should Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_THIRD}
    Page Should Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_FIRST_WRONG_CASE}    ignore_case=${True}
    Page Should Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_SECOND_WRONG_CASE}    ignore_case=${True}
    Page Should Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_THIRD_WRONG_CASE}    ignore_case=${True}

Test Page Should Contain Match
    Page Should Contain Match    ${TEXT_MATCH}
    Page Should Contain Match    ${TEXT_MATCH_WRONG_CASE}    ignore_case=${True}

Test Page Should Contain String X Times
    Page Should Contain String X Times    ${TEXT_TO_COUNT}    3
    Page Should Contain String X Times    ${TEXT_TO_COUNT_WRONG_CASE}    5    ignore_case=${True}

Test Page Should Match Regex
    Page Should Match Regex    ${VALID_REGEX}

Test Page Should Not Match Regex
    Page Should Not Match Regex    ${INVALID_REGEX}

Test Page Should Not Contain All Strings
    Page Should Not Contain All Strings    ${LIST_STRINGS_NON_EXISTENT}
    Page Should Not Contain All Strings    ${LIST_STRINGS_NON_EXITENT_IGNORE_CASE}    ignore_case=${True}

Test Page Should Not Contain Any String
    Page Should Not Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_FIRST_WRONG_CASE}
    Page Should Not Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_SECOND_WRONG_CASE}
    Page Should Not Contain Any String    ${LIST_STRINGS_RIGHT_IN_THE_THIRD_WRONG_CASE}
    Page Should Not Contain Any String    ${LIST_STRINGS_NON_EXITENT_IGNORE_CASE}    ignore_case=${True}

Test Page Should Not Contain Match
    Page Should Not Contain Match    ${TEXT_NOT_MATCH}
    Page Should Not Contain Match    ${TEXT_NOT_MATCH_WRONG_CASE}    ignore_case=${True}

Test Page Should Not Contain String
    Page Should Not Contain String    ${WELCOME_WRONG_CASE}
    Page Should Not Contain String    ${STRING_NON_EXISTENT}    ignore_case=${True}

Test Read
    ${read_text}    Read    1    10    48
    Should Be Equal As Strings    ${WELCOME_TITLE}    ${read_text}

Test Read All Screen
    ${screen_content}    Read All Screen
    Should Contain    ${screen_content}    i
    Should Contain    ${screen_content}    c I
    Should Not Contain    ${screen_content}    xyz

Test Write Bare
    Write Bare    ${WRITE_TEXT}
    ${read_text}    Read    5    25    4
    Take Screenshot
    Should Be Equal As Strings    ${WRITE_TEXT}    ${read_text}
    Sleep    1s

Test Write Bare In Position
    Write Bare In Position    ${WRITE_TEXT_UTF8}    5    30
    ${read_text}    Read    5    30    4
    Take Screenshot
    Should Be Equal As Strings    ${WRITE_TEXT_UTF8}    ${read_text}
    Sleep    1s

Test Delete Char
    Delete Char    5    25
    ${read_text}    Read    5    25    8
    Take Screenshot
    Should Be Equal As Strings    ${TEXT_AFTER_DELETE_CHAR}    ${read_text}
    Sleep    1s

Test Delete Field
    Delete Field
    ${read_text}    Read    5    25    8
    Take Screenshot
    Should Be Equal As Strings    ${TEXT_AFTER_DELETE_FIELD}    ${read_text}
    Sleep    1s

Test Move Next Field
    Move Next Field
    Write Bare    ${WRITE_TEXT}
    ${read_text}    Read    5    25    4
    Should Be Equal As Strings    ${TEXT_AFTER_MOVE_NEXT_FIELD}    ${read_text}
    Sleep    1s

Test Move Previous Field
    # Send two Move Previous Field because the first only puts the cursor at the beginning of the password field
    Move Previous Field
    Move Previous Field
    Write Bare    ${WRITE_TEXT}
    ${read_text}    Read    5    25    4
    Should Be Equal As Strings    ${WRITE_TEXT}    ${read_text}
    Sleep    1s

Test Send Enter
    Wait Field Detected
    Delete Field
    Move Next Field
    Delete Field
    Send Enter
    Page Should Contain String    Sign-on information required.

Test Send PF
    Send PF    1
    Page Should Contain String    Function key not allowed.


*** Keywords ***
Suite Setup
    Open Connection    ${HOST}
    Create Directory    ${FOLDER}
    Empty Directory    ${FOLDER}
    Set Screenshot Folder    ${FOLDER}
    Change Wait Time    0.4
    Change Wait Time After Write    0.4
    Sleep    3s

Suite Teardown
    Run Keyword And Ignore Error    Close Connection
    Sleep    1s

Verify String Not Found
    [Arguments]    ${keyword}    ${string}    ${ignore_case}=${False}
    ${expected_error}    Set Variable    The string "${string}" was not found
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}    ignore_case=${ignore_case}

Verify String Not Found In List
    [Arguments]    ${keyword}    ${string_list}    ${string_position}    ${ignore_case}=${False}
    ${not_found_string}    Set Variable If
    ...    ${ignore_case}==${False}
    ...    ${string_list[${${string_position}-1}]}
    ...    ${string_list[${${string_position}-1}].lower()}
    ${expected_error}    Set Variable    The string "${not_found_string}" was not found
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string_list}    ignore_case=${ignore_case}

Verify List Not Found
    [Arguments]    ${keyword}    ${list}    ${ignore_case}=${False}
    ${expected_error}    Set Variable    The strings "${list}" were not found
    Run Keyword And Expect Error    EQUALS: ${expected_error}    ${keyword}    ${list}    ignore_case=${ignore_case}

Verify Pattern Not Found
    [Arguments]    ${keyword}    ${string}    ${ignore_case}=${False}
    ${not_found_string}    Set Variable If    ${ignore_case}==${False}    ${string}    ${string.lower()}
    ${expected_error}    Set Variable    No matches found for "${not_found_string}" pattern
    IF    ${ignore_case}
        Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}    ignore_case=${ignore_case}
    ELSE
        Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}
    END

Verify String Does Not Appear X Times
    [Arguments]
    ...    ${keyword}
    ...    ${string}
    ...    ${wrong_number_of_times}
    ...    ${right_number_of_times}
    ...    ${ignore_case}=${False}
    ${expected_error}    Set Variable
    ...    The string "${string}" was not found "${wrong_number_of_times}" times, it appears "${right_number_of_times}" times
    Run Keyword And Expect Error
    ...    ${expected_error}
    ...    ${keyword}
    ...    ${TEXT_TO_COUNT}
    ...    1
    ...    ignore_case=${ignore_case}

Verify String Found
    [Arguments]    ${keyword}    ${string}    ${ignore_case}=${False}
    ${expected_error}    Set Variable    The string "${string}" was found
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}    ignore_case=${ignore_case}

Verify List Found
    [Arguments]    ${keyword}    ${string_list}    ${string_position}    ${ignore_case}=${False}
    ${expected_error}    Set Variable    The string "${string_list[${${string_position}-1}]}" was found
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string_list}    ignore_case=${ignore_case}

Verify Wait Until String
    [Arguments]    ${keyword}    ${string}
    ${expected_error}    Set Variable    String "${string}" not found in 5 seconds
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}

Verify Wait Until String With Timeout
    [Arguments]    ${keyword}    ${string}    ${timeout}
    ${expected_error}    Set Variable    String "${string}" not found in ${timeout} seconds
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}    ${timeout}
