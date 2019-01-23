*** Settings ***
Library           Mainframe3270
Library           BuiltIn
Library           Dialogs
Library           Process
Library           OperatingSystem
Suite Teardown    Close Connection    
Test Teardown     Run Keyword If Test Failed    Fatal Error

*** Variables ***
#host
${host}               pub400.com
#folders
${folder}      ${CURDIR}${/}screenshot
${new_folder}      ${folder}${/}new_folder
#Credentials
${user}    USER0112
${password}    user0112
#Texts to write
${write_text}         TEST
#Texts to read with correct case
${welcome_title}    Welcome to PUB400.COM * your public IBM i server
${main_menu_title}    IBM i Main Menu
${main_menu_help_title}    IBM i Main Menu - Help
${text_after_delete_char}     EST TEST
${text_after_delete_field}     ${SPACE * 8}
${text_after_move_next_field}     ${SPACE * 4}
${text_match}     *PUB???.COM*
${text_to_count}    IBM
${valid_regex}    USER\\d{4}
@{list_strings}     Server name    Subsystem    Display name
@{list_strings_right_in_the_first}    Subsystem    WRONGSTRING    WRONGSTRING
@{list_strings_right_on_the_second}    WRONGSTRING    Subsystem    WRONGSTRING
@{list_strings_right_on_the_third}    WRONGSTRING    WRONGSTRING   Subsystem
#Texts to read with wrong case
${welcome_title_wrong_case}    WELCOME TO PUB400.COM * YOUR PUBLIC IBM I SERVER
${text_match_wrong_case}     *pub???.com*
${text_to_count_wrong_case}    ibm 
@{list_strings_wrong_case}     SERVER NAME    SUBSYSTEM    DISPLAY NAME
@{list_strings_right_in_the_first_wrong_case}    SUBSYSTEM    WRONGSTRING    WRONGSTRING
@{list_strings_right_on_the_second_wrong_case}    WRONGSTRING    SUBSYSTEM    WRONGSTRING
@{list_strings_right_on_the_third_wrong_case}    WRONGSTRING    WRONGSTRING   SUBSYSTEM
#Texts not existants to read with correct case
@{list_strings_not_existants}     SERVER NAME    SUBSYSTEM    DISPLAY NAME
${text_not_match}     *PUB???400.COM*
${invalid_regex}    USER\\d{5}
#Texts not existants to read with wrong case
@{list_strings_not_existants_ignore_case}     WRONGSTRING    WRONGSTRING    WRONGSTRING
${text_not_match_wrong_case}     *pub???400.com*
${string_not_existant}     WRONGSTRING


*** Test Cases ***
# Because of a situation on the open400 public mainframe we can not create a new connection to perform each test, 
# we know that this is not the best way to do keyword tests, but that's what we can do right now. When possible we will improve the tests.
Test Open Connection
    Open Connection    ${host}
    Sleep    1s
    Page Should Contain String    ${welcome_title}

Test Wait Field Detected
    Wait Field Detected

Test Read
    ${read_text}    Read    1    10    48
    Should Be Equal As Strings    ${welcome_title}    ${read_text}

Test Page Should Contain String
    Page Should Contain String    ${welcome_title}
    Page Should Contain String    ${welcome_title_wrong_case}    ignore_case=${True}

Test Page Should Contain All Strings
    Page Should Contain All Strings    ${list_strings}
    Page Should Contain All Strings    ${list_strings_wrong_case}    ignore_case=${True}

Test Page Should Contain Any String
    Page Should Contain Any String    ${list_strings_right_in_the_first}
    Page Should Contain Any String    ${list_strings_right_on_the_second}
    Page Should Contain Any String    ${list_strings_right_on_the_third}
    Page Should Contain Any String    ${list_strings_right_in_the_first_wrong_case}    ignore_case=${True}
    Page Should Contain Any String    ${list_strings_right_on_the_second_wrong_case}    ignore_case=${True}
    Page Should Contain Any String    ${list_strings_right_on_the_third_wrong_case}    ignore_case=${True}

Test Page Should Contain Match
    Page Should Contain Match    ${text_match}
    Page Should Contain Match    ${text_match_wrong_case}    ignore_case=${True}

Test Page Should Contain String X Times
    Page Should Contain String X Times    ${text_to_count}    3
    Page Should Contain String X Times    ${text_to_count_wrong_case}    3    ignore_case=${True}

Test Page Should Match Regex 
    Page Should Match Regex    ${valid_regex}

Test Page Should Not Contain All Strings
    Page Should Not Contain All Strings    ${list_strings_not_existants}
    Page Should Not Contain All Strings    ${list_strings_not_existants_ignore_case}    ignore_case=${True}

Test Page Should Not Contain Any String
    Page Should Not Contain Any String    ${list_strings_right_in_the_first_wrong_case}
    Page Should Not Contain Any String    ${list_strings_right_on_the_second_wrong_case}
    Page Should Not Contain Any String    ${list_strings_right_on_the_third_wrong_case}
    Page Should Not Contain Any String    ${list_strings_not_existants_ignore_case}    ignore_case=${True}

Test Page Should Not Contain Match 
    Page Should Not Contain Match    ${text_not_match}
    Page Should Not Contain Match    ${text_not_match_wrong_case}    ignore_case=${True}

Test Page Should Not Contain String
    Page Should Not Contain String    ${welcome_title_wrong_case}
    Page Should Not Contain String    ${string_not_existant}    ignore_case=${True}

Test Page Should Not Match Regex
    Page Should Not Match Regex    ${invalid_regex}

Test Set Screenshot Folder
    Empty Directory    ${folder}
    Create Directory    ${new_folder}
    Set Screenshot Folder    ${new_folder}
    Take Screenshot
    ${count}    Count Items In Directory    ${new_folder}
    Should Be Equal As Integers    ${count}    1
    File Should Exist    ${new_folder}${/}screenshot_*.html
    Set Screenshot Folder    ${folder}
    Sleep    1s

Test Take Screenshot
    Set Screenshot Folder    ${folder}
    Take Screenshot
    ${count}    Count Items In Directory    ${folder}
    Should Be Equal As Integers    ${count}    2
    File Should Exist    ${folder}${/}screenshot_*.html
    Sleep    1s

Test Write Bare
    Write Bare    ${write_text}
    ${read_text}    Read    5    25    4
    Take Screenshot
    Should Be Equal As Strings    ${write_text}    ${read_text}
    Sleep    1s

Test Write Bare In Position
    Write Bare In Position   ${write_text}    5    30
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

Test Send Enter
    Write Bare In Position   ${user}    5    25
    Write Bare In Position   ${password}    6    25
    Send Enter
    Check if user is allocated to another job
    Check if user have messages to read
    Wait Field Detected
    ${read_text}    Read    1    33    15
    Take Screenshot
    Should Be Equal As Strings    ${main_menu_title}    ${read_text}
    Logout

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

Test Write
    Write Bare In Position   ${user}    5    25
    Move Next Field    
    Write    ${password}
    Check if user is allocated to another job
    Check if user have messages to read
    Wait Field Detected
    ${read_text}    Read    1    33    15
    Take Screenshot
    Should Be Equal As Strings    ${main_menu_title}    ${read_text}
    Logout

Test Write In Position
    Write Bare In Position   ${user}    5    25
    Write In Position    ${password}    6    25
    Check if user is allocated to another job
    Check if user have messages to read
    Wait Field Detected
    ${read_text}    Read    1    33    15
    Take Screenshot
    Should Be Equal As Strings    ${main_menu_title}    ${read_text}
    Logout

Test Send PF
    Logon
    Send PF    1
    ${read_text}    Read    1    30    22
    Take Screenshot
    Should Be Equal As Strings    ${main_menu_help_title}    ${read_text}
    Send Enter
    Logout

Test Execute Command
    Logon
    Execute Command    PF(1)
    ${read_text}    Read    1    30    22
    Take Screenshot
    Should Be Equal As Strings    ${main_menu_help_title}    ${read_text}
    Send Enter
    Logout

Test Wait Until String
    Logon
    Wait Until String    ${main_menu_title}    5
    Logout

*** Keywords ***
Logon
    Page Should Contain String    ${welcome_title}
    Write Bare In Position   ${user}    5    25
    Write Bare In Position   ${password}    6    25
    Send Enter
    Check if user is allocated to another job
    Check if user have messages to read
    Wait Field Detected  

Logout
    Write Bare    90
    Send Enter
    Sleep    1s

Check if user is allocated to another job
    ${status}=    Run Keyword And Return Status    Page Should Contain String    is allocated to another job
    Run Keyword If    ${status}    Send Enter 

Check if user have messages to read
    ${status}=    Run Keyword And Return Status    Page Should Contain String    Display Messages
    Run Keyword If    ${status}    Send Enter 