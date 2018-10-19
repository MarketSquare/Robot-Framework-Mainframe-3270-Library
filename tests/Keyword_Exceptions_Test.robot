*** Settings ***
Library           Mainframe3270
Library           BuiltIn
Library           Dialogs
Library           Process
Library           OperatingSystem
Suite Teardown    Close Connection    
#Test Teardown     Run Keyword If Test Failed    Fatal Error

*** Variables ***
#host
${host}               pub400.com
${folder}      ${CURDIR}${/}screenshot
#Texts to read 
${welcome_title}      Welcome to PUB400.COM * your public IBM i server
@{list_strings_wrong_in_the_first}    WRONGSTRING    Subsystem    Display name
@{list_strings_wrong_on_the_second}   Server name    WRONGSTRING   Display name 
@{list_strings_wrong_on_the_third}    Server name   Subsystem    WRONGSTRING
${text_to_count}    IBM
${valid_regex}    USER\\d{4}
#Texts to read with wrong case
${welcome_title_wrong_case}    WELCOME TO PUB400.COM * YOUR PUBLIC IBM I SERVER
@{list_strings_wrong_case_in_the_first}    SERVER NAME    Subsystem    Display name
@{list_strings_wrong_case_on_the_second}   Server name    SUBSYSTEM   Display name 
@{list_strings_wrong_case_on_the_third}    Server name   Subsystem    DISPLAY NAME
@{list_strings_all_wrong_case}    SERVER NAME   SUBSYSTEM    DISPLAY NAME
${text_match_wrong_case}     *pub???.com*
${text_to_count_wrong_case}    ibm 
#Texts inexistents in mainframe
${wrong_string}      WRONGSTRING
@{list_wrong_string}    WRONGSTRING   WRONGSTRING    WRONGSTRING
${invalid_regex}    USER\\d{5}

*** Test Cases ***
Open Connection
    Open Connection    ${host}
    Wait Field Detected
    Set Screenshot Folder    ${folder}

Test Read
    ${read_text}    Read    1    10    21
    Run Keyword And Expect Error    Welcome to PUB400.COM * your public IBM i server != Welcome to PUB400.COM    Should Be Equal As Strings    ${welcome_title}    ${read_text}
    Run Keyword And Expect Error    You have exceeded the x-axis limit of the mainframe screen    Read    4    48    34

Test Page Should Contain String
    Run Keyword And Expect Error    The string "WELCOME TO PUB400.COM * YOUR PUBLIC IBM I SERVER" was not found    Page Should Contain String    ${welcome_title_wrong_case}
    Run Keyword And Expect Error    The string "WRONGSTRING" was not found    Page Should Contain String    ${wrong_string}    ignore_case=${True}

Test Page Should Contain All Strings
    Run Keyword And Expect Error    The string "SERVER NAME" was not found    Page Should Contain All Strings    ${list_strings_wrong_case_in_the_first}
    Run Keyword And Expect Error    The string "SUBSYSTEM" was not found    Page Should Contain All Strings    ${list_strings_wrong_case_on_the_second}
    Run Keyword And Expect Error    The string "DISPLAY NAME" was not found    Page Should Contain All Strings    ${list_strings_wrong_case_on_the_third}
    Run Keyword And Expect Error    The string "wrongstring" was not found    Page Should Contain All Strings    ${list_strings_wrong_in_the_first}    ignore_case=${True}
    Run Keyword And Expect Error    The string "wrongstring" was not found    Page Should Contain All Strings    ${list_strings_wrong_on_the_second}    ignore_case=${True}
    Run Keyword And Expect Error    The string "wrongstring" was not found    Page Should Contain All Strings    ${list_strings_wrong_on_the_third}    ignore_case=${True}

Test Page Should Contain Any String
    Run Keyword And Expect Error    The strings "[u'SERVER NAME', u'SUBSYSTEM', u'DISPLAY NAME']" was not found    Page Should Contain Any String    ${list_strings_all_wrong_case}
    Run Keyword And Expect Error    The strings "[u'WRONGSTRING', u'WRONGSTRING', u'WRONGSTRING']" was not found    Page Should Contain Any String    ${list_wrong_string}    ignore_case=${True}

Test Page Should Contain Match
    Run Keyword And Expect Error    No matches found for "*pub???.com*" pattern    Page Should Contain Match    ${text_match_wrong_case}
    Run Keyword And Expect Error    No matches found for "wrongstring" pattern    Page Should Contain Match    ${wrong_string}    ignore_case=${True}

Test Page Should Contain String X Times
    Run Keyword And Expect Error    The string "IBM" was not found "2" times, it appears "3" times    Page Should Contain String X Times    ${text_to_count}    2
    Run Keyword And Expect Error    The string "ibm" was not found "2" times, it appears "3" times    Page Should Contain String X Times    ${text_to_count_wrong_case}    2    ignore_case=${True}

Test Page Should Match Regex 
    Run Keyword And Expect Error    No matches found for "USER\\d{5}" pattern    Page Should Match Regex    ${invalid_regex}

*** Keywords ***