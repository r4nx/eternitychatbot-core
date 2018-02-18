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
CONVERSATION_ID = 0


def main():
    global chatbot
    global CONVERSATION_ID
    chatbot = ChatBot(
        SETTINGS['BOT_NAME'],
        logic_adapters=['chatterbot.logic.BestMatch'],
        filters=['chatterbot.filters.RepetitiveResponseFilter'],
        database=SETTINGS['DATABASE_FILE'],
        read_only=SETTINGS['READ_ONLY']
    )
    CONVERSATION_ID = chatbot.storage.create_conversation()
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
    statement, response = chatbot.generate_response(Statement(update.message.text), CONVERSATION_ID)
    if SETTINGS['PREMODERATION']:
        correct_response = input(
            ' = Premoderation =\n'
            'Chat: {} (ID {})\n'
            'Question: {}\n'
            'Response: {}\n'
            ' >> '.format(update.message.chat.title, update.message.chat.id, update.message.text, str(response)))
        print()
        if correct_response:
            if correct_response.lower().strip().startswith('remove$'):
                correct_response = correct_response.replace('remove$', '')
                chatbot.storage.remove(str(response))
            if correct_response.lower().strip() == 'pass':
                return
            response = Statement(correct_response)
            chatbot.learn_response(response, Statement(update.message.text))
            chatbot.storage.add_to_conversation(CONVERSATION_ID, statement, response)
    else:
        sleep(SETTINGS['DELAY'] * len(str(response)))
    bot.send_message(chat_id=update.message.chat.id, text=str(response))


if __name__ == '__main__':
    main()
