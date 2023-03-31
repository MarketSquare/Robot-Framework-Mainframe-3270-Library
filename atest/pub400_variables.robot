*** Variables ***
${VISIBLE}                                          True
${HOST}                                             pub400.com
${FOLDER}                                           ${CURDIR}${/}screenshots
# Text to write
${WRITE_TEXT}                                       TEST
${WRITE_TEXT_UTF8}                                  _ëçá
# Texts in the Mainframe
${WELCOME}                                          Welcome to PUB400.COM
${WELCOME_TITLE}                                    Welcome to PUB400.COM * your public IBM i server
${MAIN_MENU}                                        IBM i Main Menu
${USER_TASK}                                        User Tasks
${TEXT_MATCH}                                       *PUB???.COM*
${TEXT_TO_COUNT}                                    PUB400
${TEXT_NOT_MATCH}                                   *PUB???400.COM*
# Texts after write
${TEXT_AFTER_DELETE_CHAR}                           EST _ëçá
${TEXT_AFTER_DELETE_FIELD}                          ${SPACE * 8}
${TEXT_AFTER_MOVE_NEXT_FIELD}                       ${SPACE * 4}
# Texts in the Mainframe with wrong case
${WELCOME_TITLE_WRONG_CASE}                         WELCOME TO PUB400.COM * YOUR PUBLIC IBM I SERVER
${WELCOME_WRONG_CASE}                               WELCOME TO PUB400.COM
${TEXT_MATCH_WRONG_CASE}                            *pub???.com*
${TEXT_TO_COUNT_WRONG_CASE}                         pub400
${TEXT_NOT_MATCH_WRONG_CASE}                        *pub???400.com*
# Regex
${VALID_REGEX}                                      PUB\\d{3}
${INVALID_REGEX}                                    PUB\\d{4}
# List strings
@{LIST_STRINGS}                                     Server name    Subsystem    Display name
@{LIST_STRINGS_RIGHT_IN_THE_FIRST}                  Server name    WRONGSTRING    WRONGSTRING
@{LIST_STRINGS_RIGHT_IN_THE_SECOND}                 WRONGSTRING    Subsystem    WRONGSTRING
@{LIST_STRINGS_RIGHT_IN_THE_THIRD}                  WRONGSTRING    WRONGSTRING    Display name
@{LIST_STRINGS_NON_EXISTENT}                        SERVER NAME    SUBSYSTEM    DISPLAY NAME
# List strings wrong case
@{LIST_STRINGS_WRONG_CASE}                          SERVER NAME    SUBSYSTEM    DISPLAY NAME
@{LIST_STRINGS_RIGHT_IN_THE_FIRST_WRONG_CASE}       SERVER NAME    WRONGSTRING    WRONGSTRING
@{LIST_STRINGS_RIGHT_IN_THE_SECOND_WRONG_CASE}      WRONGSTRING    SUBSYSTEM    WRONGSTRING
@{LIST_STRINGS_RIGHT_IN_THE_THIRD_WRONG_CASE}       WRONGSTRING    WRONGSTRING    DISPLAY NAME
@{LIST_STRINGS_NON_EXITENT_IGNORE_CASE}             WRONGSTRING    WRONGSTRING    WRONGSTRING
# Text not existent in mainframe
${STRING_NON_EXISTENT}                              WRONGSTRING
# Expected errors
${WELCOME_TEXT_EXPECTED_ERROR}                      ${WELCOME_TITLE} != ${WELCOME}
${X_AXIS_EXCEEDED_EXPECTED_ERROR}                   You have exceeded the x-axis limit of the mainframe screen
${Y_AXIS_EXCEEDED_EXPECTED_ERROR}                   You have exceeded the y-axis limit of the mainframe screen
# list of wrong strings
@{LIST_STRINGS_WRONG_CASE_IN_THE_FIRST}             SERVER NAME    Subsystem    Display name
@{LIST_STRINGS_WRONG_CASE_IN_THE_SECONDS}           Server name    SUBSYSTEM    Display name
@{LIST_STRINGS_WRONG_CASE_IN_THE_THIRD}             Server name    Subsystem    DISPLAY NAME
@{LIST_STRINGS_WRONG_IN_THE_FIRST}                  WRONGSTRING    Subsystem    Display name
@{LIST_STRINGS_WRONG_IN_THE_SECOND}                 Server name    WRONGSTRING    Display name
@{LIST_STRINGS_WRONG_IN_THE_THIRD}                  Server name    Subsystem    WRONGSTRING
@{LIST_STRINGS_ALL_WRONG_CASE}                      SERVER NAME    SUBSYSTEM    DISPLAY NAME
