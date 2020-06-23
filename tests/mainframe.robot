*** Settings ***
Documentation     These tests verify that all keywords are working correctly and displaying the expected exception message.
...               To run all the tests, you will need to create a user in the https://www.pub400.com/ website,
...               this will affect the last test "Test With Login"
Suite Setup       Open Mainframe
Suite Teardown    Close Mainframe
Test Teardown     Run Keyword If Test Failed    Fatal Error
Library           ../Mainframe3270/
Library           Dialogs
Library           OperatingSystem
Library           String
Resource          pub400_variables.robot

*** Test Cases ***
Exception Test
    [Setup]    Initial Setting
    Exception Test Read
    Exception Test Write In Position
    Exception Test Write Bare In Position
    Exception Test Page Should Contain String
    Exception Test Page Should Contain All Strings
    Exception Test Page Should Contain Any String
    Exception Test Page Should Contain Match
    Exception Test Page Should Contain String X Times
    Exception Test Page Should Match Regex
    Exception Test Page Should Not Contain String
    Exception Test Page Should Not Contain All Strings
    Exception Test Page Should Not Contain Any String
    Exception Test Wait Until String
    Exception Test Wait Until String With Timeout

Test Without Login
    [Setup]    Initial Setting
    Wait Field Detected
    Test Wait Until String
    take screenshot
    Test Page Should Contain All Strings
    Test Page Should Contain Any String
    Test Page Should Contain Match
    Test Page Should Contain String X Times
    Test Page Should Match Regex
    Test Page Should Not Match Regex
    Test Page Should Not Contain All Strings
    Test Page Should Not Contain Any String
    Test Page Should Not Contain Match
    Test Page Should Not Contain String
    Test Read
    Test Write Bare
    Test Write Bare In Position
    Test Delete Char
    Test Delete Field
    Test Move Next Field
    Test Move Previous Field

Test With Login
    [Setup]    Initial Setting
    Test Send Enter
    Test Send PF

*** Keywords ***
Open Mainframe
    Open Connection    ${host}

Close Mainframe
    Close Connection

Initial Setting
    Empty Directory    ${folder}
    set screenshot folder    ${folder}
    Change Wait Time    0.4
    Change Wait Time After Write    0.4
    Sleep    1s

Test Wait Until String
    Wait Until String    ${welcome_title}    timeout=4

Test Page Should Contain All Strings
    Page Should Contain All Strings    ${list_strings}
    Page Should Contain All Strings    ${list_strings_wrong_case}    ignore_case=${True}

Test Page Should Contain Any String
    Page Should Contain Any String    ${list_strings_right_in_the_first}
    Page Should Contain Any String    ${list_strings_right_in_the_second}
    Page Should Contain Any String    ${list_strings_right_in_the_third}
    Page Should Contain Any String    ${list_strings_right_in_the_first_wrong_case}    ignore_case=${True}
    Page Should Contain Any String    ${list_strings_right_in_the_second_wrong_case}    ignore_case=${True}
    Page Should Contain Any String    ${list_strings_right_in_the_third_wrong_case}    ignore_case=${True}

Test Page Should Contain Match
    Page Should Contain Match    ${text_match}
    Page Should Contain Match    ${text_match_wrong_case}    ignore_case=${True}

Test Page Should Contain String X Times
    Page Should Contain String X Times    ${text_to_count}    4
    Page Should Contain String X Times    ${text_to_count_wrong_case}    4    ignore_case=${True}

Test Page Should Match Regex
    Page Should Match Regex    ${valid_regex}

Test Page Should Not Match Regex
    Page Should Not Match Regex    ${invalid_regex}

Test Page Should Not Contain All Strings
    Page Should Not Contain All Strings    ${list_strings_not_existants}
    Page Should Not Contain All Strings    ${list_strings_not_existants_ignore_case}    ignore_case=${True}

Test Page Should Not Contain Any String
    Page Should Not Contain Any String    ${list_strings_right_in_the_first_wrong_case}
    Page Should Not Contain Any String    ${list_strings_right_in_the_second_wrong_case}
    Page Should Not Contain Any String    ${list_strings_right_in_the_third_wrong_case}
    Page Should Not Contain Any String    ${list_strings_not_existants_ignore_case}    ignore_case=${True}

Test Page Should Not Contain Match
    Page Should Not Contain Match    ${text_not_match}
    Page Should Not Contain Match    ${text_not_match_wrong_case}    ignore_case=${True}

Test Page Should Not Contain String
    Page Should Not Contain String    ${welcome_wrong_case}
    Page Should Not Contain String    ${string_not_existant}    ignore_case=${True}

Test Read
    ${read_text}    Read    1    10    48
    Should Be Equal As Strings    ${welcome_title}    ${read_text}

Test Write Bare
    Write Bare    ${write_text}
    ${read_text}    Read    5    25    4
    Take Screenshot
    Should Be Equal As Strings    ${write_text}    ${read_text}
    Sleep    1s

Test Write Bare In Position
    Write Bare In Position    ${write_text}    5    30
    ${read_text}    Read    5    30    4
    Take Screenshot
    Should Be Equal As Strings    ${write_text}    ${read_text}
    Sleep    1s

Test Delete Char
    Delete Char    5    25
    ${read_text}    Read    5    25    8
    Take Screenshot
    Should Be Equal As Strings    ${text_after_delete_char}    ${read_text}
    Sleep    1s

Test Delete Field
    Delete Field
    ${read_text}    Read    5    25    8
    Take Screenshot
    Should Be Equal As Strings    ${text_after_delete_field}    ${read_text}
    Sleep    1s

Test Move Next Field
    Move Next Field
    Write Bare    ${write_text}
    ${read_text}    Read    5    25    4
    Should Be Equal As Strings    ${text_after_move_next_field}    ${read_text}
    Sleep    1s

Test Move Previous Field
    # Send two Move Previous Field because the first only put the cursor int he beginning of the password field
    Move Previous Field
    Move Previous Field
    Write Bare    ${write_text}
    ${read_text}    Read    5    25    4
    Should Be Equal As Strings    ${write_text}    ${read_text}
    Sleep    1s

Test Send Enter
    Wait Field Detected
    Page Should Contain String    ${welcome}
    Page Should Contain String    ${welcome_wrong_case}    ignore_case=${TRUE}
    Delete Field
    ${user}    Get Value From User    Write user
    ${password}    Get Value From User    Write user password
    write bare in position    ${user}    5    25
    Move Next Field
    write bare    ${password}
    send enter
    ${value}    read    1    33    15
    should be equal as strings    ${main_menu}    ${value}
    take screenshot

Test Send PF
    write    1
    Wait Field Detected
    take screenshot
    Page Should Contain String    ${user_task}
    send PF    12
    Wait Field Detected
    take screenshot
    Page Should Contain String    ${main_menu}
    write    90
    Wait Field Detected
    take screenshot
    # -------

Exception Test Read
    Wait Field Detected
    ${read_text}    Read    1    10    21
    Run Keyword And Expect Error    ${welcome_text_expected_error}    Should Be Equal As Strings    ${welcome_title}    ${read_text}
    Run Keyword And Expect Error    ${x_axis_exceed_expected_error}    Read    4    48    34
    Run Keyword And Expect Error    ${x_axis_exceed_expected_error}    Read    4    81    1
    Run Keyword And Expect Error    ${y_axis_exceed_expected_error}    Read    25    48    34

Exception Test Write In Position
    Run Keyword And Expect Error    ${x_axis_exceed_expected_error}    Write In Position    ${write_text}    10    81
    Run Keyword And Expect Error    ${y_axis_exceed_expected_error}    Write In Position    ${write_text}    25    10

Exception Test Write Bare In Position
    Run Keyword And Expect Error    ${x_axis_exceed_expected_error}    Write Bare In Position    ${write_text}    10    81
    Run Keyword And Expect Error    ${y_axis_exceed_expected_error}    Write Bare In Position    ${write_text}    25    10

Exception Test Page Should Contain String
    Verify String Not Found    Page Should Contain String    ${welcome_wrong_case}
    Verify String Not Found    Page Should Contain String    ${string_not_existant}    ignore_case=${True}

Exception Test Page Should Contain All Strings
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_case_in_the_first}    1
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_case_in_the_second}    2
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_case_in_the_third}    3
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_in_the_first}    1    ignore_case=${True}
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_in_the_second}    2    ignore_case=${True}
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_in_the_third}    3    ignore_case=${True}

Exception Test Page Should Contain Any String
    Verify List Not Found    Page Should Contain Any String    ${list_strings_all_wrong_case}
    Verify List Not Found    Page Should Contain Any String    ${list_strings_not_existants_ignore_case}    ignore_case=${True}

Exception Test Page Should Contain Match
    Verify Pattern Not Found    Page Should Contain Match    ${text_not_match_wrong_case}
    Verify Pattern Not Found    Page Should Contain Match    ${string_not_existant}    ignore_case=${True}

Exception Test Page Should Contain String X Times
    Verify String Does Not Appear X Times    Page Should Contain String X Times    ${text_to_count}    2    4
    Verify String Does Not Appear X Times    Page Should Contain String X Times    ${text_to_count_wrong_case}    2    4    ignore_case=${True}

Exception Test Page Should Match Regex
    Verify Pattern Not Found    Page Should Match Regex    ${invalid_regex}

Exception Test Page Should Not Contain String
    Verify String Found    Page Should Not Contain String    ${welcome}
    Verify String Found    Page Should Not Contain String    ${welcome_wrong_case}    ignore_case=${True}

Exception Test Page Should Not Contain All Strings
    Verify List Found    Page Should Not Contain All Strings    ${list_strings_right_in_the_first}    1
    Verify List Found    Page Should Not Contain All Strings    ${list_strings_right_in_the_second}    2
    Verify List Found    Page Should Not Contain All Strings    ${list_strings_right_in_the_third}    3

Exception Test Page Should Not Contain Any String
    Verify List Found    Page Should Not Contain Any String    ${list_strings_right_in_the_first}    1
    Verify List Found    Page Should Not Contain Any String    ${list_strings_right_in_the_second}    2
    Verify List Found    Page Should Not Contain Any String    ${list_strings_right_in_the_third}    3

Exception Test Wait Until String
    Verify Wait Until String    Wait Until String    ${string_not_existant}

Exception Test Wait Until String With Timeout
    Verify Wait Until String With Timeout    Wait Until String    ${string_not_existant}    timeout=2

Verify String Not Found
    [Arguments]    ${keyword}    ${string}    ${ignore_case}=${False}
    ${expected_error}=    Set Variable    The string "${string}" was not found
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}    ignore_case=${ignore_case}

Verify String Not Found In List
    [Arguments]    ${keyword}    ${string_list}    ${string_position}    ${ignore_case}=${False}
    ${not_found_string}=    Set Variable If    ${ignore_case}==${False}    ${string_list[${${string_position}-1}]}    ${string_list[${${string_position}-1}].lower()}
    ${expected_error}=    Set Variable    The string "${not_found_string}" was not found
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string_list}    ignore_case=${ignore_case}

Verify List Not Found
    [Arguments]    ${keyword}    ${list}    ${ignore_case}=${False}
    ${expected_error}=    Set Variable    The strings "${list}" was not found
    Run Keyword And Expect Error    EQUALS: ${expected_error}    ${keyword}    ${list}    ignore_case=${ignore_case}

Verify Pattern Not Found
    [Arguments]    ${keyword}    ${string}    ${ignore_case}=${False}
    ${not_found_string}=    Set Variable If    ${ignore_case}==${False}    ${string}    ${string.lower()}
    ${expected_error}=    Set Variable    No matches found for "${not_found_string}" pattern
    Run Keyword If    ${ignore_case}    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}    ignore_case=${ignore_case}
    ...    ELSE    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}

Verify String Does Not Appear X Times
    [Arguments]    ${keyword}    ${string}    ${wrong_number_of_times}    ${right_number_of_times}    ${ignore_case}=${False}
    ${expected_error}=    Set Variable    The string "${string}" was not found "${wrong_number_of_times}" times, it appears "${right_number_of_times}" times
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${text_to_count}    2    ignore_case=${ignore_case}

Verify String Found
    [Arguments]    ${keyword}    ${string}    ${ignore_case}=${False}
    ${expected_error}=    Set Variable    The string "${string}" was found
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}    ignore_case=${ignore_case}

Verify List Found
    [Arguments]    ${keyword}    ${string_list}    ${string_position}    ${ignore_case}=${False}
    ${expected_error}=    Set Variable    The string "${string_list[${${string_position}-1}]}" was found
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string_list}    ignore_case=${ignore_case}

Verify Wait Until String
    [Arguments]    ${keyword}    ${string}
    ${expected_error}=    Set Variable    String "${string}" not found in 5 seconds
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}

Verify Wait Until String With Timeout
    [Arguments]    ${keyword}    ${string}    ${timeout}
    ${expected_error}=    Set Variable    String "${string}" not found in ${timeout} seconds
    Run Keyword And Expect Error    ${expected_error}    ${keyword}    ${string}    ${timeout}
