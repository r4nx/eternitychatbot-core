#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

import logging


def initialize_logger(name, log_file, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Console log handler
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if log_file:
        # File log handler
        handler = logging.FileHandler(log_file, delay=True)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - [%(asctime)s] %(filename)s[L:%(lineno)d] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
