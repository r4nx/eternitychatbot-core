#!/usr/bin/python
# -*- coding: utf-8 -*-

# bt_eternity - BitTorrent tracker Telegram bot
# Copyright (C) 2018  Ranx

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
