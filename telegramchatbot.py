#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.

from time import sleep

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from telegram.ext import Updater, MessageHandler, Filters

from settings import SETTINGS

chatbot = None


def main():
    global chatbot
    chatbot = ChatBot(
        SETTINGS['BOT_NAME'],
        logic_adapters=['chatterbot.logic.BestMatch'],
        filters=['chatterbot.filters.RepetitiveResponseFilter'],
        database=SETTINGS['DATABASE_FILE'],
        read_only=SETTINGS['READ_ONLY']
    )
    updater = Updater(token=SETTINGS['BOT_TOKEN'])
    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.text & ~ (Filters.forwarded | Filters.reply), echo)
    dispatcher.add_handler(echo_handler)
    try:
        updater.start_polling()
    except (KeyboardInterrupt, EOFError, SystemExit):
        updater.stop()


def echo(bot, update):
    """
    :type bot: telegram.bot.Bot
    :type update: telegram.update.Update
    """
    if SETTINGS['TESTING'] and not update.message.chat.id == SETTINGS['TESTING_CHAT_ID']:
        return
    response = str(chatbot.get_response(update.message.text))
    if SETTINGS['PREMODERATION']:
        correct_response = input(
            ' = Premoderation =\n'
            'Chat: {} (ID {})\n'
            'Question: {}\n'
            'Response: {}\n'
            ' >> '.format(update.message.chat.title, update.message.chat.id, update.message.text, response))
        print()
        if correct_response:
            if correct_response.lower().strip().startswith('remove$'):
                correct_response = correct_response.replace('remove$', '')
                chatbot.storage.remove(response)
            if correct_response.lower().strip() == 'pass':
                return
            response = correct_response
            chatbot.learn_response(Statement(response), Statement(update.message.text))
    else:
        sleep(SETTINGS['DELAY'] * len(response))
    bot.send_message(chat_id=update.message.chat.id, text=response)


if __name__ == '__main__':
    main()
