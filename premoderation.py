#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This document is the property of Ranx.
# It is considered confidential and proprietary.

# This document may not be reproduced or transmitted in any form,
# in whole or in part, without the express written permission of Ranx.


def console_premoderation(question, response, payload):
    correct_response = input(
        ' = Premoderation =\n'
        'Question: {}\n'
        'Response: {}\n'
        'Chat: {} (ID {})\n'
        ' >> '.format(
            question,
            response,
            payload.chat.first_name if payload.chat.type == 'private' else payload.chat.title, payload.chat.id,
        )
    )
    if correct_response.lower().strip() == 'pass':
        return
    elif not correct_response or correct_response.isspace():
        return response
    return correct_response
