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


from random import choice

from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.response_selection import get_random_response


class AIChatBot:
    def __init__(self, bot_name, db_file, self_training, low_confidence_threshold, low_confidence_responses,
                 premoderation_callback=None):
        """Create new AIChatBot instance.

        Args:
            bot_name (str): Bot name.
            db_file (str): Database file.
            self_training (bool): Will bot train itself.
            low_confidence_threshold (int): Confidence threshold, if lower - low_confidence_responses will be used.
            low_confidence_responses (list): Responses that will be used if confidence is lower than threshold.
            premoderation_callback (function): Premoderation function, set None to disable.
        """
        self.__chatbot = ChatBot(
            bot_name,
            logic_adapters=['chatterbot.logic.BestMatch'],
            response_selection_method=get_random_response,
            filters=['chatterbot.filters.RepetitiveResponseFilter'],
            database=db_file
        )
        self.__conversation_id = self.__chatbot.storage.create_conversation()
        self.previous_response = None

        self.__self_training = self_training
        self.__low_confidence_threshold = low_confidence_threshold
        self.__low_confidence_responses = low_confidence_responses
        self.__premoderation_callback = premoderation_callback

    def get_response(self, question, premoderation_payload):
        """Get response to the message.

        Args:
            question (str): Message.
            premoderation_payload: Data to pass to premoderation_callback.

        Returns:
            str: Response.

        """
        # Get supposed response
        question = Statement(question)
        response = self.__chatbot.generate_response(question, self.__conversation_id)[1]
        """:type : Response"""

        # Choose random response if confidence is lower than threshold
        if response.confidence < self.__low_confidence_threshold and self.__low_confidence_responses:
            response = Statement(choice(self.__low_confidence_responses))

        if self.__premoderation_callback:
            response = self.__premoderation_callback(question.text, response.text, premoderation_payload)
            if not response:
                return
            response = Statement(response)
            response.confidence = 1
            self.__chatbot.learn_response(response, question)
            self.__chatbot.storage.add_to_conversation(self.__conversation_id, question, response)

        if self.__self_training and self.previous_response and '?' in self.previous_response.text and \
                self.previous_response.confidence >= self.__low_confidence_threshold:
            self.__chatbot.learn_response(question, self.previous_response)
            self.__chatbot.storage.add_to_conversation(self.__conversation_id, self.previous_response, question)
        self.previous_response = response

        return response.text

    def learn(self, question, response):
        """Learn a response.

        Args:
            question (str): Question.
            response (str): Response

        """
        question = Statement(question)
        response = Statement(response)
        self.__chatbot.learn_response(response, question)
        self.__chatbot.storage.add_to_conversation(self.__conversation_id, question, response)

    def statement_exists(self, statement_text):
        """Check if statement exists.

        Args:
            statement_text (str): Statement text.

        Returns:
            bool

        """
        return True if self.__chatbot.storage.find(statement_text) else False

    def remove_statement(self, statement_text):
        """Remove statement from database.

        Args:
            statement_text (str): Statement text.

        """
        self.__chatbot.storage.remove(statement_text)
