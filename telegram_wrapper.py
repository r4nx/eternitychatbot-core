#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

import logging
import shlex
import sys
from time import sleep

import telebot

import util
from core import AIChatBot
from logger import initialize_logger
from premoderation import console_premoderation
from settings import SETTINGS

log = logging.getLogger()
tgbot = telebot.TeleBot(SETTINGS['BOT_TOKEN'])
chatbot = None
""":type : AIChatBot"""


def main():
    initialize_logger(log)
    sys.excepthook = error_handler

    global chatbot
    chatbot = AIChatBot(
        SETTINGS['BOT_NAME'],
        SETTINGS['DATABASE_FILE'],
        SETTINGS['SELF_TRAINING'],
        SETTINGS['LOW_CONFIDENCE_THRESHOLD'],
        SETTINGS['LOW_CONFIDENCE_RESPONSES'],
        console_premoderation if SETTINGS['PREMODERATION'] else None,
    )
    log.info('Bot started!')
    try:
        tgbot.polling()
    except (KeyboardInterrupt, EOFError, SystemExit):
        tgbot.stop_polling()


@tgbot.message_handler(commands=['learn'], func=lambda message: message.from_user.username in SETTINGS['ADMINS'])
def handle_learn(message):
    try:
        cmd = shlex.split(util.remove_nonascii(message.text, SETTINGS['ALLOWED_CHARACTERS']))
    except ValueError:
        tgbot.send_message(message.chat.id, 'Invalid arguments.')
        return
    if len(cmd) < 3:
        tgbot.send_message(message.chat.id, 'Not enough arguments.')
        return
    responses = cmd[2].split('^')
    [chatbot.learn(cmd[1], response) for response in responses]
    tgbot.send_message(message.chat.id, 'Learnt successfully.')


@tgbot.message_handler(commands=['remove'], func=lambda message: message.from_user.username in SETTINGS['ADMINS'])
def handle_remove(message):
    cmd = util.remove_nonascii(message.text, SETTINGS['ALLOWED_CHARACTERS']).split(' ', 1)
    if len(cmd) < 2:
        tgbot.send_message(message.chat.id, 'Not enough arguments.')
        return
    if not chatbot.statement_exists(cmd[1]):
        tgbot.send_message(message.chat.id, 'Statement not found.')
        return
    chatbot.remove_statement(cmd[1])
    tgbot.send_message(message.chat.id, 'Statement removed successfully.')


@tgbot.message_handler(commands=['exit', 'stop'], func=lambda message: message.from_user.username in SETTINGS['ADMINS'])
def handle_exit(message):
    tgbot.stop_polling()
    tgbot.send_message(message.chat.id, 'Polling stopped.')


@tgbot.message_handler(content_types=['text'],
                       func=lambda message:
                       (not SETTINGS['TESTING'] or message.chat.id == SETTINGS['TESTING_CHAT_ID'])
                       and not (message.forward_date or message.reply_to_message))
def handle_message(message):
    msg = util.remove_nonascii(message.text, SETTINGS['ALLOWED_CHARACTERS'])
    response = chatbot.get_response(msg, message)

    if not SETTINGS['PREMODERATION']:
        logging.info('Q: "{}" A: "{}" (Chat {})'.format(msg, response, message.chat.id))

    if response:
        if SETTINGS['DELAY']:
            sleep(SETTINGS['DELAY'] * len(response))
        tgbot.send_message(message.chat.id, response)
    elif not SETTINGS['PREMODERATION']:
        log.warning('Response is empty or whitespace, sending of the message was canceled.')


def error_handler(exctype, value, tb):
    log.error('An error has occurred.', exc_info=(exctype, value, tb))


if __name__ == '__main__':
    main()
