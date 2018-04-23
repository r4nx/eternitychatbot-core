#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

import logging
from random import choice
from time import sleep

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from telegram.ext import Updater, MessageHandler, Filters

from settings import SETTINGS

chatbot = None
previous_response = None
CONVERSATION_ID = 0


def main():
    initialize_logger()
    global chatbot
    global CONVERSATION_ID
    chatbot = ChatBot(
        SETTINGS['BOT_NAME'],
        logic_adapters=['chatterbot.logic.BestMatch'],
        filters=['chatterbot.filters.RepetitiveResponseFilter'],
        database=SETTINGS['DATABASE_FILE']
    )
    CONVERSATION_ID = chatbot.storage.create_conversation()
    updater = Updater(token=SETTINGS['BOT_TOKEN'])
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & ~ (Filters.forwarded | Filters.reply) &
                                  Filters.chat(SETTINGS['TESTING_CHAT_ID']) if SETTINGS['TESTING'] else None, echo)
    dispatcher.add_handler(echo_handler)
    logging.info('Bot started!')
    try:
        updater.start_polling()
    except (KeyboardInterrupt, EOFError, SystemExit):
        updater.stop()


def echo(bot, update):
    """
    :type bot: telegram.bot.Bot
    :type update: telegram.update.Update
    """
    statement, response = chatbot.generate_response(Statement(update.message.text), CONVERSATION_ID)
    if response.confidence <= SETTINGS['LOW_CONFIDENCE_THRESHOLD']:
        response = Statement(choice(SETTINGS['LOW_CONFIDENCE_RESPONSES']))
    global previous_response
    if SETTINGS['PREMODERATION']:
        correct_response = input(
            ' = Premoderation =\n'
            'Chat: {} (ID {})\n'
            'Question: {}\n'
            'Response: {}\n'
            ' >> '.format(
                update.message.chat.first_name if update.message.chat.type == update.message.chat.PRIVATE else
                update.message.chat.title, update.message.chat.id, update.message.text, response.text))
        print()
        if correct_response:
            if correct_response.lower().strip().startswith('remove$'):
                correct_response = correct_response.replace('remove$', '')
                chatbot.storage.remove(response.text)
            if not correct_response or correct_response.isspace() or correct_response.lower().strip() == 'pass':
                return
            response = Statement(correct_response)
            chatbot.learn_response(response, Statement(update.message.text))
            chatbot.storage.add_to_conversation(CONVERSATION_ID, statement, response)
    else:
        logging.info('(Chat {}) Q: "{}" A: "{}"'.format(update.message.chat.id, update.message.text, response.text))
        if not response.text or response.text.isspace():
            logging.warning('Response is empty or whitespace, sending of the message was canceled.')
            previous_response = None
            return
        sleep(SETTINGS['DELAY'] * len(response.text))
    if SETTINGS['SELF_TRAINING']:
        if previous_response and '?' in previous_response:
            chatbot.learn_response(Statement(update.message.text), Statement(previous_response))
            chatbot.storage.add_to_conversation(CONVERSATION_ID, statement, Statement(update.message.text))
        previous_response = response.text
    bot.send_message(chat_id=update.message.chat.id, text=response.text)


def initialize_logger():
    logger = logging.getLogger()
    logger.setLevel(SETTINGS['CONSOLE_LOG_LEVEL'])

    handler = logging.StreamHandler()
    handler.setLevel(SETTINGS['CONSOLE_LOG_LEVEL'])
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if SETTINGS['FILE_LOG_ENABLED']:
        handler = logging.FileHandler('telegramchatbot.log', encoding=None, delay=True)
        handler.setLevel(SETTINGS['FILE_LOG_LEVEL'])
        formatter = logging.Formatter('%(levelname)s - [%(asctime)s] %(filename)s[L:%(lineno)d] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)


if __name__ == '__main__':
    main()
