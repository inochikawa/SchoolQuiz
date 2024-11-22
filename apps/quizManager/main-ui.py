from uuid import uuid4

import customtkinter
from data.services import QuizService, CompletedQuizService, UserProfileService, GradeYearService
from data.models.quiz import Quiz
from data.models.quiz import QuizAnswerOption
from data.models.quiz import QuizQuestion
from data.models.quiz import MediaItem
from data.models.quiz import MediaItemType
import yaml


class AppHeaderFrame(customtkinter.CTkFrame):
    def __init__(self, master, onSaveNewQuizBtnCommand, onMakeQuizReportCommand):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.saveNewQuizBtn = customtkinter.CTkButton(self, text="Save new Quiz", command=onSaveNewQuizBtnCommand)
        self.quizReportBtn = customtkinter.CTkButton(self, text="Quiz Report", command=onMakeQuizReportCommand)

        self.saveNewQuizBtn.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.quizReportBtn.grid(row=0, column=1, padx=10, pady=10, sticky="w")


class SaveNewQuizFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1)
        self.grid_rowconfigure(2)

        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.textbox.focus_set()

        self.saveBtn = customtkinter.CTkButton(self, text="Add new Quiz", command=self.onSaveCommand)
        self.saveBtn.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ws")

        self.statusLabel = customtkinter.CTkLabel(self, text="", fg_color="transparent")
        self.statusLabel.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ws")

    def onSaveCommand(self):
        try:
            quizService = QuizService()
            content = self.textbox.get("0.0", "end")

            quizItem = Quiz.fromDict(yaml.safe_load(content))

            quizItem.id = str(uuid4())

            for question in quizItem.questions:
                question.id = str(uuid4())

                if not question.points or question.points == 0:
                    question.points = 1

                for answerOption in question.answerOptions:
                    answerOption.id = str(uuid4())

            quizService.saveQuiz(quizItem)

            self.setStatusLabelValue("Saved")
        except:
            self.setStatusLabelValue("Failed to save quiz. Please use correct YAML syntax")

    def setStatusLabelValue(self, text: str):
        statusText = "Status: "
        if text and text != "":
            self.statusLabel.configure(text=statusText + text)
            return

        return


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("640x720")
        self.title("Quiz manager")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.headerFrame = AppHeaderFrame(self, self.onSaveNewQuizBtnCommand, self.onMakeQuizReportCommand)
        self.headerFrame.grid(row=0, column=0, padx=10, pady=10, sticky="new")
        self.saveNewQuizFrame = None

    def onSaveNewQuizBtnCommand(self):
        self.saveNewQuizFrame = SaveNewQuizFrame(self)
        self.saveNewQuizFrame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def onMakeQuizReportCommand(self):
        self.saveNewQuizFrame.destroy()


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
