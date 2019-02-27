*** Settings ***
Resource          pub400_resources.txt  
Test Teardown     Run Keyword If Test Failed    Fatal Error
Force Tags        KET

*** Test Cases ***
Open Connection
    Wait Field Detected
    Set Screenshot Folder    ${folder}

Test Read
    ${read_text}    Read    1    10    21
    Run Keyword And Expect Error    ${welcome_text_expected_error}    Should Be Equal As Strings    ${welcome_title}    ${read_text}
    Run Keyword And Expect Error    ${x_axis_exceed_expected_error}    Read    4    48    34
    Run Keyword And Expect Error    ${x_axis_exceed_expected_error}    Read    4    81    1
    Run Keyword And Expect Error    ${y_axis_exceed_expected_error}    Read    25    48    34

Test Write In Position
    Run Keyword And Expect Error    ${x_axis_exceed_expected_error}    Write In Position    ${write_text}    10    81
    Run Keyword And Expect Error    ${y_axis_exceed_expected_error}    Write In Position    ${write_text}    25    10

Test Write Bare In Position
    Run Keyword And Expect Error    ${x_axis_exceed_expected_error}    Write Bare In Position    ${write_text}    10    81
    Run Keyword And Expect Error    ${y_axis_exceed_expected_error}    Write Bare In Position    ${write_text}    25    10

Test Page Should Contain String
    Verify String Not Found    Page Should Contain String    ${welcome_title_wrong_case}
    Verify String Not Found    Page Should Contain String    ${string_not_existant}    ignore_case=${True}

Test Page Should Contain All Strings
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_case_on_the_first}    1
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_case_on_the_second}    2
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_case_on_the_third}    3
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_on_the_first}    1    ignore_case=${True}
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_on_the_second}    2    ignore_case=${True}
    Verify String Not Found In List    Page Should Contain All Strings    ${list_strings_wrong_on_the_third}    3    ignore_case=${True}

Test Page Should Contain Any String
    Verify List Not Found    Page Should Contain Any String    ${list_strings_all_wrong_case}
    Verify List Not Found    Page Should Contain Any String    ${list_strings_not_existants_ignore_case}    ignore_case=${True}

Test Page Should Contain Match
    Verify Pattern Not Found    Page Should Contain Match    ${text_match_wrong_case}
    Verify Pattern Not Found    Page Should Contain Match    ${string_not_existant}    ignore_case=${True}

Test Page Should Contain String X Times
    Verify String Does Not Appear X Times    Page Should Contain String X Times    ${text_to_count}    2    3
    Verify String Does Not Appear X Times    Page Should Contain String X Times    ${text_to_count_wrong_case}    2    3    ignore_case=${True}

Test Page Should Match Regex
    Verify Pattern Not Found    Page Should Match Regex    ${invalid_regex}

Test Page Should Not Contain String
    Verify String Found    Page Should Not Contain String    ${welcome_title_short}
    Verify String Found    Page Should Not Contain String    ${welcome_title_short_wrong_case}    ignore_case=${True}

Test Page Should Not Contain All Strings
    Verify List Found    Page Should Not Contain All Strings    ${list_strings_right_on_the_first}    1
    Verify List Found    Page Should Not Contain All Strings    ${list_strings_right_on_the_second}    2
    Verify List Found    Page Should Not Contain All Strings    ${list_strings_right_on_the_third}    3

Test Page Should Not Contain Any String
    Verify List Found    Page Should Not Contain Any String     ${list_strings_right_on_the_first}    1
    Verify List Found    Page Should Not Contain Any String    ${list_strings_right_on_the_second}    2
    Verify List Found    Page Should Not Contain Any String    ${list_strings_right_on_the_third}    3

Test Wait Until String
    Verify Wait Until String    Wait Until String    ${string_not_existant}

Test Wait Until String With Timeout
    Verify Wait Until String With Timeout    Wait Until String    ${string_not_existant}    timeout=2
