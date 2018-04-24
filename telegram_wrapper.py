#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

import logging
import sys
from time import sleep

import telebot

from core import AIChatBot
from logger import initialize_logger
from settings import SETTINGS

log = logging.getLogger()
tgbot = telebot.TeleBot(SETTINGS['BOT_TOKEN'])
chatbot = None
""":type : AIChatBot"""


def main():
    initialize_logger(log)
    sys.excepthook = error_handler

    def premoderation(message, response, payload):
        correct_response = input(
            ' = Premoderation =\n'
            'Chat: {} (ID {})\n'
            'Question: {}\n'
            'Response: {}\n'
            ' >> '.format(
                payload.chat.first_name if payload.chat.type == 'private' else payload.chat.title, payload.chat.id,
                message, response))
        if correct_response.lower().strip().startswith('remove$'):
            correct_response = correct_response[7:]
            chatbot.remove_statement(response)
        if correct_response.lower().strip() == 'pass':
            return None
        elif not correct_response or correct_response.isspace():
            return response
        return correct_response

    global chatbot
    chatbot = AIChatBot(
        SETTINGS['BOT_NAME'],
        SETTINGS['DATABASE_FILE'],
        SETTINGS['SELF_TRAINING'],
        SETTINGS['LOW_CONFIDENCE_THRESHOLD'],
        SETTINGS['LOW_CONFIDENCE_RESPONSES'],
        premoderation if SETTINGS['PREMODERATION'] else None,
    )
    log.info('Bot started!')
    try:
        tgbot.polling()
    except (KeyboardInterrupt, EOFError, SystemExit):
        tgbot.stop_polling()


@tgbot.message_handler(content_types=['text'],
                       func=lambda message:
                       (not SETTINGS['TESTING'] or message.chat.id == SETTINGS['TESTING_CHAT_ID'])
                       and not (message.forward_date or message.reply_to_message))
def handle_message(message):
    response = chatbot.get_response(message.text, message)

    if not SETTINGS['PREMODERATION']:
        logging.info('Q: "{}" A: "{}" (Chat {})'.format(message.text, response, message.chat.id))

    if response:
        if SETTINGS['DELAY']:
            sleep(SETTINGS['DELAY'] * len(response))
        tgbot.send_message(message.chat.id, response)
    else:
        log.warning('Response is empty or whitespace, sending of the message was canceled.')


def error_handler(exctype, value, tb):
    log.error('An error has occurred.', exc_info=(exctype, value, tb))


if __name__ == '__main__':
    main()
