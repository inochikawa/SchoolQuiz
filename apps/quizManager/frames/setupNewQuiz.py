from datetime import datetime, timezone
from uuid import uuid4

import customtkinter
import yaml

from data.models.quiz import Quiz
from data.services import AcademicYearService, GradeYearService, QuizService


class DateRangeFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self._fromEntry = customtkinter.CTkEntry(self, placeholder_text="Available from yyyy-mm-dd")
        self._fromEntry.grid(row=0, column=0, padx=10, pady=10, sticky="we")
        self._toEntry = customtkinter.CTkEntry(self, placeholder_text="Available to yyyy-mm-dd")
        self._toEntry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

    def getFromDate(self) -> datetime | None:
        localDateStr = self._fromEntry.get()

        if not localDateStr or localDateStr == "":
            return None

        return datetime.fromisoformat(localDateStr).astimezone(tz=timezone.utc)

    def getToDate(self) -> datetime | None:
        localDateStr = self._toEntry.get()

        if not localDateStr or localDateStr == "":
            return None

        return datetime.fromisoformat(localDateStr).astimezone(tz=timezone.utc)


class GradeYearFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master, orientation="horizontal", height=50, label_text="Grade", label_anchor="w")

        self._gradeYearCheckboxes = []

        academicYearService = AcademicYearService()
        gradesService = GradeYearService()

        grades = gradesService.searchByAcademicYear(academicYearService.getCurrentAcademicYear().year)
        grades.sort(key=lambda x: (x.number, x.code))

        for index, item in enumerate(grades):
            checkbox = customtkinter.CTkCheckBox(
                self,
                text=item.code,
                onvalue=item.id,
                offvalue=False)
            checkbox.grid(row=0, column=index, padx=(10, 0), pady=10, sticky="ne")
            self._gradeYearCheckboxes.append(checkbox)

    def getSelectedGradeYearIds(self) -> list[str]:
        return [x.get() for x in self._gradeYearCheckboxes if x.get()]


class TopicFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._topicEntry = customtkinter.CTkEntry(self, placeholder_text="Topic")
        self._topicEntry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    def getTopic(self) -> str:
        return self._topicEntry.get()


class SetupNewQuizFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.gradeYearFrame = GradeYearFrame(self)
        self.gradeYearFrame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.topicFrame = TopicFrame(self)
        self.topicFrame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.dateRangeFrame = DateRangeFrame(self)
        self.dateRangeFrame.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.questionsYamlTextbox = customtkinter.CTkTextbox(self)
        self.questionsYamlTextbox.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

        self.saveBtn = customtkinter.CTkButton(self, text="Save", command=self.onSaveCommand)
        self.saveBtn.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ws")

        self.statusLabel = customtkinter.CTkLabel(self, text="", fg_color="transparent")
        self.statusLabel.grid(row=5, column=0, padx=10, pady=(0, 10), sticky="ws")

    def onSaveCommand(self):
        self.setStatusLabelValue("Saving...")
        try:
            quizService = QuizService()
            content = self.questionsYamlTextbox.get("0.0", "end")
            selectedGradeIds = self.gradeYearFrame.getSelectedGradeYearIds()
            topic = self.topicFrame.getTopic()

            fromDate = self.dateRangeFrame.getFromDate()
            toDate = self.dateRangeFrame.getToDate()

            for gradeYearId in selectedGradeIds:

                quizItem = Quiz.fromDict(yaml.safe_load(content))

                quizItem.id = str(uuid4())
                quizItem.gradeYearId = gradeYearId
                quizItem.topic = topic
                quizItem.availableFromDate = fromDate
                quizItem.availableToDate = toDate

                for question in quizItem.questions:
                    question.id = str(uuid4())

                    if not question.points or question.points == 0:
                        question.points = 1

                    doesNotHaveCorrectAnswers = len([x for x in question.answerOptions if x.isCorrect]) == 0

                    if doesNotHaveCorrectAnswers:
                        raise Exception(f"Question {question.question} does not have correct answers. All of them are False.")

                    for answerOption in question.answerOptions:
                        answerOption.id = str(uuid4())

                        if not answerOption.text or answerOption.text == "":
                            raise Exception(f"Empty text in answerOption is not allowed in question {question.question}")

                quizService.saveQuiz(quizItem)

            if len(selectedGradeIds) > 0:
                self.setStatusLabelValue("Saved")
            else:
                self.setStatusLabelValue("Nothing to save")
        except Exception as error:
            self.setStatusLabelValue(f"Failed to save quiz. {error}")

    def setStatusLabelValue(self, text: str):
        if text and text != "":
            self.statusLabel.configure(text=text)
            return

        self.statusLabel.configure(text="")
