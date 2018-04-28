#!/usr/bin/python
# -*- coding: utf-8 -*-

# telegramchatbot - AI Telegram Chatbot
# Copyright (C) 2018  Ranx

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


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
