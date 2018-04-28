#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

from chatterbot import ChatBot
from chatterbot.response_selection import get_random_response

from logger import initialize_logger
from settings import SETTINGS

log = initialize_logger('trainer', 'telegramchatbot.log' if SETTINGS['LOG_FILE'] else '', SETTINGS['LOGGING_LEVEL'])


def main():
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
        chatbot.train(SETTINGS['CONVERSATIONS_FILE'])
    except FileNotFoundError:
        log.error('File not found!')
    log.info('Training finished!')


if __name__ == '__main__':
    main()
