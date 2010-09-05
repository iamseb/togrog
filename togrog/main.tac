#!/usr/bin/env python
# coding: utf-8
# Copyright Seb Potter 2010

from togrog import settings
from togrog.application import start_app

import sys
sys.path.insert(0, '.')

application = start_app(settings)