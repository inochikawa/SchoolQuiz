from datetime import datetime, timezone

from data.cosmosDb import QuizCosmosClient, AcademicYearsContainer
from data.cosmosDb.quizCosmosClient import getQuizCosmosClient
from data.models import AcademicYear


class AcademicYearService:
    _client: QuizCosmosClient = getQuizCosmosClient()

    def getCurrentAcademicYear(self) -> AcademicYear:
        utcNow = datetime.now(tz=timezone.utc)

        academicYear = self.searchByDate(utcNow)

        if academicYear:
            return academicYear

        formattedDate = utcNow.strftime("%Y-%m-%d %H:%M:%S")
        raise Exception(f"No academic year was found for date {formattedDate}")

    def searchByDate(self, searchDate: datetime) -> AcademicYear | None:
        query = "select * from c where c.startDate <= @searchDate and c.endDate >= @searchDate"
        container = self._client.getContainer(AcademicYearsContainer.name)

        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@searchDate", value=searchDate.isoformat())
        ])

        for item in items:
            return AcademicYear.fromDict(item)

        return None
