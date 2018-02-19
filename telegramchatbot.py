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
previous_message = None
CONVERSATION_ID = 0


def main():
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
    if SETTINGS['PREMODERATION']:
        correct_response = input(
            ' = Premoderation =\n'
            'Chat: {} (ID {})\n'
            'Question: {}\n'
            'Response: {}\n'
            ' >> '.format(
                update.message.chat.first_name if update.message.chat.type == update.message.chat.PRIVATE else
                update.message.chat.title, update.message.chat.id, update.message.text, str(response)))
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
    global previous_message
    if SETTINGS['SELF_TRAINING'] and previous_message and '?' in previous_message:
        chatbot.learn_response(Statement(update.message.text), Statement(previous_message))
        chatbot.storage.add_to_conversation(CONVERSATION_ID, statement, Statement(update.message.text))
    previous_message = str(response)
    bot.send_message(chat_id=update.message.chat.id, text=str(response))


if __name__ == '__main__':
    main()
