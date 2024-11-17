import os
from datetime import datetime, timezone

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, MenuButtonCommands
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from data.bilders import CompletedQuizBuilder
from data.models import UserProfile, UserAnswer
from data.models.quiz import Quiz, CompletedQuiz
from data.services import UserProfileService, GradeYearService, QuizService, AcademicYearService, CompletedQuizService
from extensions import readFile, writeToFile
import yaml


class QuizBotClient:
    _application: Application
    _telegramToken: str
    _userProfileService: UserProfileService
    _gradeYearService: GradeYearService
    _quizzesService: QuizService

    def __init__(self):
        self._telegramToken = os.environ["TELEGRAM_TOKEN"]
        self._userProfileService = UserProfileService()
        self._gradeYearService = GradeYearService()
        self._quizzesService = QuizService()
        self._academicYearService = AcademicYearService()
        self._completedQuizService = CompletedQuizService()
        self._setupTelegramApp()

    def start(self):
        self._application.run_polling(allowed_updates=Update.ALL_TYPES)

    def _setupTelegramApp(self) -> None:
        self._application = Application.builder().token(self._telegramToken).build()

        self._application.add_handler(ConversationHandler(
            entry_points=[
                CommandHandler(BotCommand.START, self._startCommandHandler),
                CommandHandler(BotCommand.HELP, callback=self._helpCommandHandler)
            ],
            states={
                BotUserSetupState.HOME: [
                    MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=self._helpCommandHandler),
                    CommandHandler(BotCommand.HELP, callback=self._helpCommandHandler),
                    CommandHandler(BotCommand.USER_SETUP, self._userSetupCommandHandler),
                    CommandHandler(BotCommand.WHO_AM_I, self._whoAmICommandHandler),
                    CommandHandler(BotCommand.QUIZ, callback=self._showQuizzesCommandHandler),
                    CommandHandler(BotCommand.COMPLETED_QUIZZES, callback=self._showCompletedQuizzesCommandHandler)
                ],
                BotUserSetupState.USER_SETUP: [ConversationHandler(
                    entry_points=[MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=self._selectGradeYearIdCommandHandler)],
                    states={
                        BotUserSetupState.UserSetupState.ASK_FOR_GRADE_YEAR_ID: [
                            MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=self._selectGradeYearIdCommandHandler)
                        ],
                        BotUserSetupState.UserSetupState.ASK_FOR_FIRST_NAME: [
                            MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=self._selectUserFirstNameCommandHandler)
                        ],
                        BotUserSetupState.UserSetupState.ASK_FOR_LAST_NAME: [
                            MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=self._selectUserLastNameCommandHandler)
                        ],
                    },
                    fallbacks=[],
                    map_to_parent={
                        BotUserSetupState.UserSetupState.USER_IS_CONFIGURED: BotUserSetupState.HOME
                    }
                )],
                BotUserSetupState.QUIZ: [ConversationHandler(
                    entry_points=[
                        MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=self._selectQuizCommandHandler),
                        CommandHandler(BotCommand.Quiz.EXIT, callback=self._exitFromQuizCommandHandler)
                    ],
                    states={
                        BotUserSetupState.QuizState.SELECT_QUIZ: [
                            MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=self._selectQuizCommandHandler),
                            CommandHandler(BotCommand.Quiz.EXIT, callback=self._exitFromQuizCommandHandler)
                        ],
                        BotUserSetupState.QuizState.CONTINUE_QUIZ: [
                            MessageHandler(filters=filters.TEXT & ~filters.COMMAND, callback=self._continueQuizCommandHandler),
                            CommandHandler(BotCommand.Quiz.EXIT, callback=self._exitFromQuizCommandHandler)
                        ],
                    },
                    fallbacks=[],
                    map_to_parent={
                        BotUserSetupState.QuizState.QUIZ_IS_COMPLETED: BotUserSetupState.HOME,
                        BotUserSetupState.QuizState.QUIZ_IS_CANCELLED: BotUserSetupState.HOME
                    }
                )],

            },
            fallbacks=[CommandHandler(BotCommand.START, self._startCommandHandler)]
        ))

    async def _whoAmICommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userId = str(update.message.from_user.id)

        userProfile = self._userProfileService.searchById(userId)

        if userProfile is None:
            await update.effective_message.reply_text(f"Схоже я тебе ще не знаю 🤔\n\nСкористайся командою /{BotCommand.USER_SETUP} щоб налаштувати свій акаунт")
            return BotUserSetupState.HOME

        await update.message.reply_text(text=self._getUserProfileSummaryText(userProfile))

        return BotUserSetupState.HOME

    def _getUserProfileSummaryText(self, userProfile: UserProfile):
        academicYear = self._academicYearService.getCurrentAcademicYear()
        gradeYear = self._gradeYearService.get(userProfile.gradeYearId, academicYear.year)
        return (f"{userProfile.fullName}\n{gradeYear.code} клас\n\n"
                f"Якщо треба змінити свої дані - скористайся командою /{BotCommand.USER_SETUP}\n"
                f"Якщо хочеш вже почати роботу над тестами - тицяй /{BotCommand.QUIZ}")

    async def _userSetupCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userInfo = update.message.from_user
        userId = str(userInfo.id)

        userProfile = self._userProfileService.searchById(userId)

        if userProfile is None:
            userProfile = UserProfile(id=userId, firstName=userInfo.first_name, lastName=userInfo.last_name, gradeYearId="", userName=update.message.from_user.name)

        context.user_data[UserDataKey.USER_PROFILE] = userProfile

        academicYear = self._academicYearService.getCurrentAcademicYear()
        gradeYears = self._gradeYearService.searchByAcademicYear(academicYear.year)

        buttons = [[KeyboardButton(text=x.code) for x in gradeYears]]
        keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

        await update.message.reply_text(text="Вкажи будь ласка свій клас", reply_markup=keyboard)

        return BotUserSetupState.USER_SETUP

    async def _selectGradeYearIdCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userProfile = context.user_data[UserDataKey.USER_PROFILE]
        gradeYearCode = update.effective_message.text

        academicYear = self._academicYearService.getCurrentAcademicYear()
        gradeYear = self._gradeYearService.searchByCodeAndAcademicYear(gradeYearCode, academicYear=academicYear.year)

        if gradeYear is None:
            gradeYears = self._gradeYearService.searchByAcademicYear(academicYear=academicYear.year)
            buttons = [[KeyboardButton(text=x.code) for x in gradeYears]]
            keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

            await update.effective_message.reply_text(text=f"Хм.. Схоже {gradeYearCode} не існує 🤔. Спробуй ще раз.", reply_markup=keyboard)
            return BotUserSetupState.UserSetupState.ASK_FOR_GRADE_YEAR_ID

        self._userProfileService.delete(userProfile.id, userProfile.gradeYearId)
        userProfile.gradeYearId = gradeYear.id
        self._userProfileService.save(userProfile)

        keyboard: ReplyKeyboardMarkup | None = None
        if userProfile.firstName:
            buttons = [[KeyboardButton(text=userProfile.firstName)]]
            keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

        await update.effective_message.reply_text(text=f"Тепер вкажи яке твоє ім'я", reply_markup=keyboard)

        return BotUserSetupState.UserSetupState.ASK_FOR_FIRST_NAME

    async def _selectUserFirstNameCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userProfile = context.user_data[UserDataKey.USER_PROFILE]
        userProfile.firstName = update.effective_message.text

        self._userProfileService.save(userProfile)

        keyboard: ReplyKeyboardMarkup | None = None

        if userProfile.lastName:
            buttons = [[KeyboardButton(text=userProfile.lastName)]]
            keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

        await update.effective_message.reply_text(text=f"І яке твоє прізвище?", reply_markup=keyboard)

        return BotUserSetupState.UserSetupState.ASK_FOR_LAST_NAME

    async def _selectUserLastNameCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userProfile = context.user_data[UserDataKey.USER_PROFILE]
        userProfile.lastName = update.effective_message.text

        self._userProfileService.save(userProfile)
        await update.effective_message.reply_text(text=f"Дякую!")
        await update.effective_message.reply_text(text=f"Твій профіль\n\n{self._getUserProfileSummaryText(userProfile)}")

        return BotUserSetupState.UserSetupState.USER_IS_CONFIGURED

    async def _startCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        startMessageContent = f"Вітаю у боті для проходження різних тестів з інформатики 👀\n\nТисни /{BotCommand.HELP} що переглянути доступні команди."
        await update.effective_message.reply_text(startMessageContent)

        return BotUserSetupState.HOME

    async def _showCompletedQuizzesCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userProfile = self._userProfileService.searchById(str(update.message.from_user.id))

        if not userProfile:
            await update.effective_message.reply_text(text=f"Я не знаю хто ти 💀.\n\n"
                                                           f"Скористайся командою /{BotCommand.USER_SETUP} щоб засетапити свій профіль")
            return BotUserSetupState.HOME

        completedQuizzes = self._completedQuizService.searchByUser(userProfile.id)

        if len(completedQuizzes) == 0:
            await update.effective_message.reply_text(text="Ти ще нічого не проходив\n\n"
                                                           f"Почати проходити тести - /{BotCommand.QUIZ}")
            return BotUserSetupState.HOME

        for quiz in completedQuizzes:
            await update.effective_message.reply_text(text=f"Тест '{quiz.topic}' пройдено {quiz.completedDate.strftime('%d/%m/%Y')}\n"
                                                           f"Оцінка: {quiz.mark} {quiz.fancyMarkSign}")

        return BotUserSetupState.HOME

    async def _showQuizzesCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userProfile = self._userProfileService.searchById(str(update.message.from_user.id))

        if not userProfile:
            await update.effective_message.reply_text(text=f"Я не знаю хто ти 💀.\n\n"
                                                           f"Скористайся командою /{BotCommand.USER_SETUP} щоб засетапити свій профіль")
            return BotUserSetupState.HOME

        completedQuizzesIds = [x.id for x in self._completedQuizService.searchByUser(userProfile.id)]

        quizzes = [x for x in self._quizzesService.searchByGradeYear(userProfile.gradeYearId) if x.isAvailable and x.id not in completedQuizzesIds]

        if len(quizzes) == 0:
            await update.effective_message.reply_text(text="Тестів ще немає для тебе, можеш видихнути 🙂‍↕️")
            return BotUserSetupState.HOME

        buttons = [[KeyboardButton(text=x.topic) for x in quizzes]]
        keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

        await update.effective_message.reply_text(text=f"Вибери тест", reply_markup=keyboard)
        return BotUserSetupState.QUIZ

    async def _exitFromQuizCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        await update.effective_message.reply_text(text="Виходимо з тестування. \nТвій процес не збережено 😀.")
        return BotUserSetupState.QuizState.QUIZ_IS_CANCELLED

    def _buildQuizAnswerBotResponse(self, quiz: Quiz, questionIndex: int) -> (str, ReplyKeyboardMarkup):
        question = quiz.questions[questionIndex]

        buttons = [[KeyboardButton(text=x.text)] for x in question.answerOptions]
        keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)

        return f"{question.question} (+{question.points} б)", keyboard

    async def _selectQuizCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        quizTopic = update.message.text
        userProfile = self._userProfileService.searchById(str(update.message.from_user.id))
        quiz = self._quizzesService.searchByGradeYearAndTopic(userProfile.gradeYearId, quizTopic)

        if quiz is None:
            await self._showQuizzesCommandHandler(update, context)
            return BotUserSetupState.QuizState.SELECT_QUIZ

        questionIndex = 0

        context.user_data[UserDataKey.QUIZ] = quiz
        context.user_data[UserDataKey.QUESTION_INDEX] = questionIndex
        context.user_data[UserDataKey.QUIZ_TIMESTAMP] = datetime.now(timezone.utc).timestamp()

        questionDetails = self._buildQuizAnswerBotResponse(quiz, questionIndex)

        await update.effective_message.reply_text(text=questionDetails[0], reply_markup=questionDetails[1])
        return BotUserSetupState.QuizState.CONTINUE_QUIZ

    async def _continueQuizCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        userAnswer = update.effective_message.text
        quiz: Quiz = context.user_data.get(UserDataKey.QUIZ)
        questionIndex = context.user_data.get(UserDataKey.QUESTION_INDEX, 0)
        question = quiz.questions[questionIndex]
        quizTimestamp = context.user_data.get(UserDataKey.QUIZ_TIMESTAMP, 0)

        for answerOption in question.answerOptions:
            if answerOption.text == userAnswer:
                userAnswers = context.user_data.get(UserDataKey.ANSWERS, [])
                userAnswers.append(UserAnswer(quizId=quiz.id, questionId=question.id, answerIds=[answerOption.id], quizTimestamp=quizTimestamp))
                context.user_data[UserDataKey.ANSWERS] = userAnswers

                # Continue to the next question
                questionIndex = questionIndex + 1

        # If last question -> complete state
        if questionIndex == len(quiz.questions):
            userAnswers = context.user_data.get(UserDataKey.ANSWERS, [])

            completedQuiz = CompletedQuizBuilder.buildFromQuizAndUserAnswers(quiz, userAnswers, str(update.effective_message.from_user.id))
            self._completedQuizService.save(completedQuiz)

            await update.effective_message.reply_markdown_v2(f"Вітаю, ти закінчив тест {quiz.topic}\\!\n\nТвоя оціка ||{completedQuiz.mark}|| {completedQuiz.fancyMarkSign}\\!")

            await update.effective_message.reply_text("Твої відповіді ⬇️")

            for question in completedQuiz.questions:
                await update.effective_message.reply_text(f"Питання:\n{question.question}"
                                                          f"\n\nПравильна відповідь:\n{'\n'.join([f' - {x}' for x in question.correctAnswers])}"
                                                          f"\n\nТвоя відповідь:\n{'\n'.join([f' - {x}' for x in question.userAnswers])}")

            return BotUserSetupState.QuizState.QUIZ_IS_COMPLETED

        context.user_data[UserDataKey.QUESTION_INDEX] = questionIndex
        questionDetails = self._buildQuizAnswerBotResponse(quiz, questionIndex)
        await update.effective_message.reply_text(text=questionDetails[0], reply_markup=questionDetails[1])
        return BotUserSetupState.QuizState.CONTINUE_QUIZ

    async def _helpCommandHandler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        helpMessageContent = readFile("bot-help.md")
        await update.effective_message.reply_markdown_v2(helpMessageContent)
        return BotUserSetupState.HOME


class BotUserSetupState:
    HOME = 0
    QUIZ = 1
    USER_SETUP = 2

    class QuizState:
        CONTINUE_QUIZ = 101
        SELECT_QUIZ = 102
        QUIZ_IS_COMPLETED = 103
        QUIZ_IS_CANCELLED = 104

    class UserSetupState:
        ASK_FOR_GRADE_YEAR_ID = 201
        USER_IS_CONFIGURED = 202
        ASK_FOR_FIRST_NAME = 203
        ASK_FOR_LAST_NAME = 204


class UserDataKey:
    USER_PROFILE = "user-profile"
    QUIZ_TIMESTAMP = "quizTimestamp"
    ANSWERS = "answers"
    QUIZ = "quiz"
    QUESTION_INDEX = "questionIndex"


class BotCommand:
    START = "start"
    HELP = "help"
    USER_SETUP = "user_setup"
    WHO_AM_I = "who_am_i"
    QUIZ = "quiz"
    COMPLETED_QUIZZES = "completed_quizzes"

    class Quiz:
        EXIT = "exit"
