#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

import logging

from settings import SETTINGS


def initialize_logger(logger):
    logger.setLevel(SETTINGS['CONSOLE_LOGGING_LEVEL'])

    handler = logging.StreamHandler()
    handler.setLevel(SETTINGS['CONSOLE_LOGGING_LEVEL'])
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if SETTINGS['LOG_FILE']:
        handler = logging.FileHandler('telegramchatbot.log', delay=True)
        handler.setLevel(SETTINGS['FILE_LOGGING_LEVEL'])
        formatter = logging.Formatter('%(levelname)s - [%(asctime)s] %(filename)s[L:%(lineno)d] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
