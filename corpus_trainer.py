#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
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

import sys

from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response

from logger import initialize_logger
from settings import SETTINGS

log = initialize_logger('trainer', 'telegramchatbot.log' if SETTINGS['LOG_FILE'] else '', SETTINGS['LOGGING_LEVEL'])


def main():
    sys.excepthook = error_handler
    if len(sys.argv) < 2:
        log.error('Not enough arguments! Usage: {} <conversations_file>'.format(__name__))
        return

    chatbot = ChatBot(
        SETTINGS['BOT_NAME'],
        logic_adapters=['chatterbot.logic.BestMatch'],
        response_selection_method=get_random_response,
        filters=['chatterbot.filters.RepetitiveResponseFilter'],
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
        database=SETTINGS['DATABASE_FILE']
    )
    log.info('Training started!')
    try:
        chatbot.train(sys.argv[0])
    except FileNotFoundError:
        log.error('File not found!')
    log.info('Training finished!')


def error_handler(exctype, value, tb):
    log.error('An error has occurred.', exc_info=(exctype, value, tb))


if __name__ == '__main__':
    main()
