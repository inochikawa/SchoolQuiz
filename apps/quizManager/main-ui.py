import itertools
from datetime import datetime, timezone
from uuid import uuid4

import customtkinter
from data.services import QuizService, CompletedQuizService, UserProfileService, GradeYearService, AcademicYearService
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
        self.grid_rowconfigure(0)
        self.grid_rowconfigure(1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3)
        self.grid_rowconfigure(4)

        self.gradeYearCheckboxes = []
        self.gradeYearCheckboxesFrame = customtkinter.CTkFrame(self)
        self.gradeYearCheckboxesFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self._setupGradeYearCheckboxes()

        self.topicFrame = customtkinter.CTkFrame(self)
        self.topicFrame.grid_columnconfigure(0, weight=0)
        self.topicFrame.grid_columnconfigure(1, weight=1)
        self.topicFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self._setupTopicFrameChildren()

        self.questionsYamlTextbox = customtkinter.CTkTextbox(self)
        self.questionsYamlTextbox.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.questionsYamlTextbox.focus_set()

        self.saveBtn = customtkinter.CTkButton(self, text="Add new Quiz", command=self.onSaveCommand)
        self.saveBtn.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ws")

        self.statusLabel = customtkinter.CTkLabel(self, text="", fg_color="transparent")
        self.statusLabel.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ws")

    def onSaveCommand(self):
        self.setStatusLabelValue("")
        try:
            quizService = QuizService()
            content = self.questionsYamlTextbox.get("0.0", "end")
            selectedGradeIds = [x.get() for x in self.gradeYearCheckboxes if x.get()]

            for gradeYearId in selectedGradeIds:

                quizItem = Quiz.fromDict(yaml.safe_load(content))

                quizItem.id = str(uuid4())
                quizItem.gradeYearId = gradeYearId
                quizItem.topic = self.topicTextbox.get("0.0", "end")

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

        self.statusLabel.configure(text="")

    def _setupGradeYearCheckboxes(self):
        academicYearService = AcademicYearService()
        gradesService = GradeYearService()

        grades = gradesService.searchByAcademicYear(academicYearService.getCurrentAcademicYear().year)
        grades.sort(key=lambda x: (x.number, x.code))

        gradeRow = 0
        for gradeNumber, group in itertools.groupby(grades, lambda x: x.number):
            for itemIndex, item in enumerate(group):
                checkbox = customtkinter.CTkCheckBox(
                    self.gradeYearCheckboxesFrame,
                    text=item.code,
                    onvalue=item.id,
                    offvalue=False)
                checkbox.grid(row=gradeRow, column=itemIndex, padx=10, pady=10, sticky="nsew")

                self.gradeYearCheckboxes.append(checkbox)
            gradeRow += 1

    def _setupTopicFrameChildren(self):
        self.topicLabel = customtkinter.CTkLabel(self.topicFrame, text="Topic:")
        self.topicLabel.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.topicTextbox = customtkinter.CTkTextbox(self.topicFrame, height=20)
        self.topicTextbox.grid(row=0, column=1, padx=10, pady=10, sticky="ew")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("640x900")
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
