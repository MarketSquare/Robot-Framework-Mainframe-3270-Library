*** Variables ***
${host}           pub400.com
${folder}         ${CURDIR}${/}screenshots
# Text to write
${write_text}         TEST
${write_text_utf8}         _ëçá
# Texts in the Mainframe
${welcome}        Welcome to PUB400.COM
${welcome_title}    Welcome to PUB400.COM * your public IBM i server
${main_menu}       IBM i Main Menu
${user_task}       User Tasks
${text_match}     *PUB???.COM*
${text_to_count}    PUB400
${text_not_match}     *PUB???400.COM*
# Texts after write
${text_after_delete_char}     EST _ëçá
${text_after_delete_field}     ${SPACE * 8}
${text_after_move_next_field}     ${SPACE * 4}
# Texts in the Mainframe with wrong case
${welcome_title_wrong_case}    WELCOME TO PUB400.COM * YOUR PUBLIC IBM I SERVER
${welcome_wrong_case}    WELCOME TO PUB400.COM
${text_match_wrong_case}     *pub???.com*
${text_to_count_wrong_case}    pub400
${text_not_match_wrong_case}     *pub???400.com*
# Regex
${valid_regex}    PUB\\d{3}
${invalid_regex}    PUB\\d{4}
# List strings
@{list_strings}     Server name    Subsystem    Display name
@{list_strings_right_in_the_first}    Server name    WRONGSTRING    WRONGSTRING
@{list_strings_right_in_the_second}    WRONGSTRING    Subsystem    WRONGSTRING
@{list_strings_right_in_the_third}     WRONGSTRING    WRONGSTRING    Display name
@{list_strings_not_existants}     SERVER NAME    SUBSYSTEM    DISPLAY NAME
# List strings wrong case
@{list_strings_wrong_case}     SERVER NAME    SUBSYSTEM    DISPLAY NAME
@{list_strings_right_in_the_first_wrong_case}    SERVER NAME    WRONGSTRING    WRONGSTRING
@{list_strings_right_in_the_second_wrong_case}    WRONGSTRING    SUBSYSTEM    WRONGSTRING
@{list_strings_right_in_the_third_wrong_case}    WRONGSTRING    WRONGSTRING   DISPLAY NAME
@{list_strings_not_existants_ignore_case}     WRONGSTRING    WRONGSTRING    WRONGSTRING
# Text not existent in mainframe
${string_not_existant}     WRONGSTRING
# Expected errors
${welcome_text_expected_error}    ${welcome_title} != ${welcome}
${x_axis_exceed_expected_error}    You have exceeded the x-axis limit of the mainframe screen
${y_axis_exceed_expected_error}    You have exceeded the y-axis limit of the mainframe screen
# list of wrong strings
@{list_strings_wrong_case_in_the_first}    SERVER NAME    Subsystem    Display name
@{list_strings_wrong_case_in_the_second}   Server name    SUBSYSTEM   Display name
@{list_strings_wrong_case_in_the_third}    Server name   Subsystem    DISPLAY NAME
@{list_strings_wrong_in_the_first}    WRONGSTRING    Subsystem    Display name
@{list_strings_wrong_in_the_second}   Server name    WRONGSTRING   Display name
@{list_strings_wrong_in_the_third}    Server name   Subsystem    WRONGSTRING
@{list_strings_all_wrong_case}    SERVER NAME   SUBSYSTEM    DISPLAY NAME