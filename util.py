#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

import string


def remove_nonascii(s, allowed_chars=''):
    printable = set(string.printable + allowed_chars)
    return ''.join(filter(lambda x: x in printable, s))
