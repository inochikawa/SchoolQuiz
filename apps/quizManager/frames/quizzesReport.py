from datetime import datetime, timezone, timedelta

import os
import csv
import customtkinter
import subprocess

from data.services import CompletedQuizService, UserProfileService, GradeYearService


class QuizzesReportFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        defaultDate = customtkinter.StringVar(value=datetime.now().date().isoformat())
        self.dateEntry = customtkinter.CTkEntry(self, placeholder_text="Report for date yyyy-mm-dd", textvariable=defaultDate)
        self.dateEntry.grid(row=0, column=0, padx=10, pady=10, sticky="we")

        self.generateReportBtn = customtkinter.CTkButton(self, text="Generate report", command=self.generateReport)
        self.generateReportBtn.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="we")

        self.openFileBtn: customtkinter.CTkButton | None = None

        self.statusLabel = customtkinter.CTkLabel(self, text="")
        self.statusLabel.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ws")

        self.reportFilePath: str | None = None

    def placeOpenReportBtn(self):
        self.openFileBtn = customtkinter.CTkButton(self, text="Open report", command=self.openReportFile)
        self.openFileBtn.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="we")

    def destroyOpenReportBtn(self):
        if not self.openFileBtn:
            return

        self.openFileBtn.destroy()

    def generateReport(self):
        self.resetFrameData()
        self.setStatusLabelValue("")

        try:
            reportDateStr = self.dateEntry.get()

            service = CompletedQuizService()
            userService = UserProfileService()
            gradeYearService = GradeYearService()

            startDate = datetime.fromisoformat(reportDateStr).date() if reportDateStr and reportDateStr != "" else datetime.now(tz=timezone.utc).date()
            endDate = startDate + timedelta(days=1)

            items = service.searchByCompletedDate(startDate, endDate)

            formattedRows = []

            for x in items:
                userProfile = userService.searchById(x.userId)
                gradeYear = gradeYearService.searchById(userProfile.gradeYearId)
                row = {
                    "academicYear": gradeYear.academicYear,
                    "gradeCode": gradeYear.code,
                    "user": userProfile.fullName,
                    "topic": x.topic,
                    "mark": x.mark,
                    "completedDate": x.completedDate.strftime("%Y-%m-%d %H:%M"),
                }
                formattedRows.append(row)

            filePath = "./localOutput/quizzes-report-" + startDate.isoformat() + ".csv"

            fileMode = "w" if os.path.isfile(filePath) else "x"

            with open(filePath, fileMode) as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["academicYear", "gradeCode", "user", "topic", "mark", "completedDate"])
                writer.writeheader()
                writer.writerows(formattedRows)

            self.reportFilePath = filePath
            self.setStatusLabelValue(f"Report saved: {filePath}")
            self.placeOpenReportBtn()

        except Exception as error:
            self.setStatusLabelValue(f"Error: {error}")
            self.resetFrameData()

    def openReportFile(self):
        if not self.reportFilePath:
            self.setStatusLabelValue("No file report found")
            return

        subprocess.run(['open', self.reportFilePath], check=True)

    def setStatusLabelValue(self, text: str):
        if text and text != "":
            self.statusLabel.configure(text=text)
            return

        self.statusLabel.configure(text="")

    def resetFrameData(self):
        self.reportFilePath = None
        self.destroyOpenReportBtn()
