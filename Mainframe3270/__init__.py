# -*- encoding: utf-8 -*-
from .x3270 import x3270
from .version import VERSION


class Mainframe3270(x3270):
    ROBOT_LIBRARY_SCOPE = 'TEST SUITE'
    ROBOT_LIBRARY_VERSION = VERSION
