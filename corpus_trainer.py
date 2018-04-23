#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

import logging

from chatterbot import ChatBot

from logger import initialize_logger
from settings import SETTINGS

log = logging.getLogger()


def main():
    initialize_logger(log)
    chatbot = ChatBot(
        SETTINGS['BOT_NAME'],
        logic_adapters=['chatterbot.logic.BestMatch'],
        filters=['chatterbot.filters.RepetitiveResponseFilter'],
        trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
        database=SETTINGS['DATABASE_FILE']
    )
    log.info('Training started!')
    chatbot.train(SETTINGS['CONVERSATIONS_FILE'])
    log.info('Training finished!')


if __name__ == '__main__':
    main()
