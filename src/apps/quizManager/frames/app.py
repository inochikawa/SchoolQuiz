import customtkinter

from .quizzesReport import QuizzesReportFrame
from .setupNewQuiz import SetupNewQuizFrame


class AppContentTabs(customtkinter.CTkTabview):
    def __init__(self, master):
        super().__init__(master)
        self.newQuizTab = self.add("Setup new Quiz")
        self.quizzesReportTab = self.add("Quizzes report")

        self._configureTabFrames([
            self.quizzesReportTab,
            self.newQuizTab
        ])

    @staticmethod
    def _configureTabFrames(frames: list[customtkinter.CTkFrame]):
        for f in frames:
            f.grid_columnconfigure(0, weight=1)
            f.grid_rowconfigure(0, weight=1)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("900x900")
        self.title("Quiz manager")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._appContentTabs = AppContentTabs(self)
        self._appContentTabs.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self._saveNewQuizFrame = SetupNewQuizFrame(self._appContentTabs.newQuizTab)
        self._saveNewQuizFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

        self._quizzesReportFrame = QuizzesReportFrame(self._appContentTabs.quizzesReportTab)
        self._quizzesReportFrame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
