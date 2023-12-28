import re
from typing import List, Optional
from robot.api import logger
from robot.api.deco import keyword
from robot.utils import Matcher
from Mainframe3270.librarycomponent import LibraryComponent


class AssertionKeywords(LibraryComponent):
    @keyword("Page Should Contain String")
    def page_should_contain_string(
        self, txt: str, ignore_case: bool = False, error_message: Optional[str] = None
    ) -> None:
        """Assert that a given string exists on the mainframe screen.

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Contain String | something |
            | Page Should Contain String | someTHING | ignore_case=True |
            | Page Should Contain String | something | error_message=New error message |
        """
        message = f'The string "{txt}" was not found'
        if error_message:
            message = error_message
        if ignore_case:
            txt = txt.lower()
        result = self.mf.search_string(txt, ignore_case)
        if not result:
            raise Exception(message)
        logger.info(f'The string "{txt}" was found')

    @keyword("Page Should Not Contain String")
    def page_should_not_contain_string(
        self, txt: str, ignore_case: bool = False, error_message: Optional[str] = None
    ) -> None:
        """Assert that a given string does NOT exist on the mainframe screen.

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Not Contain String | something |
            | Page Should Not Contain String | someTHING | ignore_case=True |
            | Page Should Not Contain String | something | error_message=New error message |
        """
        message = f'The string "{txt}" was found'
        if error_message:
            message = error_message
        if ignore_case:
            txt = txt.lower()
        result = self.mf.search_string(txt, ignore_case)
        if result:
            raise Exception(message)

    @keyword("Page Should Contain Any String")
    def page_should_contain_any_string(
        self,
        list_string: List[str],
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Assert that one of the strings in a given list exists on the mainframe screen.

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Contain Any String | ${list_of_string} |
            | Page Should Contain Any String | ${list_of_string} | ignore_case=True |
            | Page Should Contain Any String | ${list_of_string} | error_message=New error message |
        """
        message = f'The strings "{list_string}" were not found'
        if error_message:
            message = error_message
        if ignore_case:
            list_string = [item.lower() for item in list_string]
        for string in list_string:
            result = self.mf.search_string(string, ignore_case)
            if result:
                break
        if not result:
            raise Exception(message)

    @keyword("Page Should Not Contain Any String")
    def page_should_not_contain_any_string(
        self,
        list_string: List[str],
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Assert that none of the strings in a given list exists on the mainframe screen. If one or more of the
        string are found, the keyword will raise an exception.

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Not Contain Any Strings | ${list_of_string} |
            | Page Should Not Contain Any Strings | ${list_of_string} | ignore_case=True |
            | Page Should Not Contain Any Strings | ${list_of_string} | error_message=New error message |
        """
        self._compare_all_list_with_screen_text(list_string, ignore_case, error_message, should_match=False)

    @keyword("Page Should Contain All Strings")
    def page_should_contain_all_strings(
        self,
        list_string: List[str],
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Assert that all the strings in a given list exist on the mainframe screen.

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Contain All Strings | ${list_of_string} |
            | Page Should Contain All Strings | ${list_of_string} | ignore_case=True |
            | Page Should Contain All Strings | ${list_of_string} | error_message=New error message |
        """
        self._compare_all_list_with_screen_text(list_string, ignore_case, error_message, should_match=True)

    @keyword("Page Should Not Contain All Strings")
    def page_should_not_contain_all_strings(
        self,
        list_string: List[str],
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Fails if one of the strings in a given list exists on the mainframe screen. If one of the string
        are found, the keyword will raise an exception.

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Not Contain All Strings | ${list_of_string} |
            | Page Should Not Contain All Strings | ${list_of_string} | ignore_case=True |
            | Page Should Not Contain All Strings | ${list_of_string} | error_message=New error message |
        """
        message = error_message
        if ignore_case:
            list_string = [item.lower() for item in list_string]
        for string in list_string:
            result = self.mf.search_string(string, ignore_case)
            if result:
                if message is None:
                    message = f'The string "{string}" was found'
                raise Exception(message)

    @keyword("Page Should Contain String X Times")
    def page_should_contain_string_x_times(
        self,
        txt: str,
        number: int,
        ignore_case: bool = False,
        error_message: Optional[str] = None,
    ) -> None:
        """Asserts that the entered string appears the desired number of times on the mainframe screen.

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
               | Page Should Contain String X Times | something | 3 |
               | Page Should Contain String X Times | someTHING | 3 | ignore_case=True |
               | Page Should Contain String X Times | something | 3 | error_message=New error message |
        """
        message = error_message
        number = number
        all_screen = self.mf.read_all_screen()
        if ignore_case:
            txt = txt.lower()
            all_screen = all_screen.lower()
        number_of_times = all_screen.count(txt)
        if number_of_times != number:
            if message is None:
                message = f'The string "{txt}" was not found "{number}" times, it appears "{number_of_times}" times'
            raise Exception(message)
        logger.info(f'The string "{txt}" was found "{number}" times')

    @keyword("Page Should Match Regex")
    def page_should_match_regex(self, regex_pattern: str) -> None:
        r"""Fails if string does not match pattern as a regular expression. Regular expression check is
        implemented using the Python [https://docs.python.org/2/library/re.html|re module]. Python's
        regular expression syntax is derived from Perl, and it is thus also very similar to the syntax used,
        for example, in Java, Ruby and .NET.

        Backslash is an escape character in the test data, and possible backslashes in the pattern must
        thus be escaped with another backslash (e.g. \\d\\w+).
        """
        page_text = self.mf.read_all_screen()
        if not re.findall(regex_pattern, page_text, re.MULTILINE):
            raise Exception(f'No matches found for "{regex_pattern}" pattern')

    @keyword("Page Should Not Match Regex")
    def page_should_not_match_regex(self, regex_pattern: str) -> None:
        r"""Fails if string does match pattern as a regular expression. Regular expression check is
        implemented using the Python [https://docs.python.org/2/library/re.html|re module]. Python's
        regular expression syntax is derived from Perl, and it is thus also very similar to the syntax used,
        for example, in Java, Ruby and .NET.

        Backslash is an escape character in the test data, and possible backslashes in the pattern must
        thus be escaped with another backslash (e.g. \\d\\w+).
        """
        page_text = self.mf.read_all_screen()
        if re.findall(regex_pattern, page_text, re.MULTILINE):
            raise Exception(f'There are matches found for "{regex_pattern}" pattern')

    @keyword("Page Should Contain Match")
    def page_should_contain_match(
        self, txt: str, ignore_case: bool = False, error_message: Optional[str] = None
    ) -> None:
        """Assert that the text displayed on the mainframe screen matches the given pattern.

        Pattern matching is similar to matching files in a shell, and it is always case-sensitive.
        In the pattern, * matches anything and ? matches any single character.

        Note that for this keyword the entire screen is considered a string. So if you want to search
        for the string "something" and it is somewhere other than at the beginning or end of the screen, it
        should be reported as follows: **something**

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Contain Match | **something** |
            | Page Should Contain Match | **so???hing** |
            | Page Should Contain Match | **someTHING** | ignore_case=True |
            | Page Should Contain Match | **something** | error_message=New error message |
        """
        message = error_message
        all_screen = self.mf.read_all_screen()
        if ignore_case:
            txt = txt.lower()
            all_screen = all_screen.lower()
        matcher = Matcher(txt, caseless=False, spaceless=False)
        result = matcher.match(all_screen)
        if not result:
            if message is None:
                message = f'No matches found for "{txt}" pattern'
            raise Exception(message)

    @keyword("Page Should Not Contain Match")
    def page_should_not_contain_match(
        self, txt: str, ignore_case: bool = False, error_message: Optional[str] = None
    ) -> None:
        """Assert that the text displayed on the mainframe screen does NOT match the given pattern.

        Pattern matching is similar to matching files in a shell, and it is always case-sensitive.
        In the pattern, * matches anything and ? matches any single character.

        Note that for this keyword the entire screen is considered a string. So if you want to search
        for the string "something" and it is somewhere other than at the beginning or end of the screen, it
        should be reported as follows: **something**

        The assertion is case-sensitive. If you want it to be case-insensitive, you can pass the argument
        ignore_case=True.

        You can change the exception message by setting a custom string to error_message.

        Example:
            | Page Should Not Contain Match | **something** |
            | Page Should Not Contain Match | **so???hing** |
            | Page Should Not Contain Match | **someTHING** | ignore_case=True |
            | Page Should Not Contain Match | **something** | error_message=New error message |
        """
        message = error_message
        all_screen = self.mf.read_all_screen()
        if ignore_case:
            txt = txt.lower()
            all_screen = all_screen.lower()
        matcher = Matcher(txt, caseless=False, spaceless=False)
        result = matcher.match(all_screen)
        if result:
            if message is None:
                message = f'There are matches found for "{txt}" pattern'
            raise Exception(message)

    def _compare_all_list_with_screen_text(
        self,
        list_string: List[str],
        ignore_case: bool,
        message: Optional[str],
        should_match: bool,
    ) -> None:
        if ignore_case:
            list_string = [item.lower() for item in list_string]
        for string in list_string:
            result = self.mf.search_string(string, ignore_case)
            if not should_match and result:
                if message is None:
                    message = f'The string "{string}" was found'
                raise Exception(message)
            elif should_match and not result:
                if message is None:
                    message = f'The string "{string}" was not found'
                raise Exception(message)
