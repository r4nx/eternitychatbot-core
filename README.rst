===============
telegramchatbot
===============

telegramchatbot is a simple chatbot which can be accessed via Telegram. Create your own bot, its really easy!
If you are interested, follow the instructions below.

1. `Structure`_
2. `Settings`_
3. `Running the bot`_
4. `Telegram commands`_
5. `Premoderation`_

*********
Structure
*********

telegramchatbot consists of 2 main parts: core and Telegram wrapper. The core is independent from Telegram or other files,
you can use it for your own chatbot implementation in other messenger, for example. Telegram wrapper is like input/output
controller: it handles messages, pass them to the core and than sends output back to the user. telegramchatbot also contains
additional files: corpus_trainer.py can train your bot with conversations file, other files' names speak for themselves.

********
Settings
********

To set up your bot open settings.py in any text editor and change settings to your needs.

======================== ================================================================
Option                   Description
======================== ================================================================
BOT_NAME                 Bot name
BOT_TOKEN                Bot access token (can be obtained via `@botfather <https://t.me/botfather>`_)
DATABASE_FILE            Database file that contains all the bot's knowledge
CONVERSATIONS_FILE       Conversations file for training, **important:** put ``./`` before file name
SELF_TRAINING            Does bot remembers your answers to its questions
PREMODERATION            Does premoderation enabled
DELAY                    Delay before sending response (second per character)
LOG_FILE                 Does write log to the file
LOGGING_LEVEL            Logging level
LOW_CONFIDENCE_THRESHOLD Coefficient of uncertainty, when the bot will use the answers below instead of its own
LOW_CONFIDENCE_RESPONSES Responses that will be used when bot uncertain
ALLOWED_CHARACTERS       Characters that won't be filtered (by default only ASCII characters allowed)
TESTING                  If enabled, bot will respond only in certain chat
TESTING_CHAT_ID          ID of chat where bot will respond
ADMINS                   Usernames of admins that can use bot commands (/learn, /remove, etc)
======================== ================================================================

Example settings
================

.. code-block:: python

    SETTINGS = {
        'BOT_NAME': 'Example bot',
        'BOT_TOKEN': '123456789:uiogrgGUIRiOGrg_groe-rio52qeriowkpj',
        'DATABASE_FILE': 'Bot.db',
        'CONVERSATIONS_FILE': './conversations.yml',
        'SELF_TRAINING': True,
        'PREMODERATION': True,
        'DELAY': 0,
        'LOG_FILE': True,
        'LOGGING_LEVEL': logging.INFO,
        'LOW_CONFIDENCE_THRESHOLD': 0.4,
        'LOW_CONFIDENCE_RESPONSES': ['I don\' understand you :/', 'What are you talking about?'],
        'ALLOWED_CHARACTERS': 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ',
        'TESTING': True,
        'TESTING_CHAT_ID': 987654321,
        'ADMINS': ['user123', 'anotheruser']
    }

***************
Running the bot
***************

1. Install `Python 3 <https://python.org>`_
2. Install all the requirements with ``pip install -r requirements.txt``
3. Go to `@botfather <https://t.me/botfather>`_ and create new bot, than copy access token
4. Set up the bot
5. Launch the bot with ``python telegram_wrapper.py`` or just double click

*****************
Telegram commands
*****************

============================ ================================
Command                      Description
============================ ================================
/learn <question> <response> Learn new response to the question, **important:** enclose parameter in double quotes if it contains spaces.
/remove <statement>          Remove statement (question or response) from the database
/exit                        Shutdown bot (you also need to send another message of any content after that command to shutdown it)
============================ ================================

*************
Premoderation
*************

Premoderation is a really simple thing: when someone sends message to your bot, this message will appear in your console
with some other information such as supposed response and chat title. You have 3 ways: press enter key to accept
bot response, enter your own response (bot will learn it) or enter ``pass`` to pass the question and don't send any response.
