import logging
import os

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from data.services import QuizService, UserProfileService


class CommandHandlerSetup:
    _quizService: QuizService
    _userProfileService: UserProfileService

    def __init__(self):
        self._quizService = QuizService()

    async def setupUserProfileOnStartCommand(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        quizzes = self._quizService.getAll()

        keyboard = [[InlineKeyboardButton(q.topic, callback_data=[123])] for q in quizzes]

        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Please choose:", reply_markup=reply_markup)
