from data.cosmosDb import QuizCosmosClient, GradeYearsContainer
from data.cosmosDb.quizCosmosClient import getQuizCosmosClient
from data.models import GradeYear
from azure.cosmos.exceptions import CosmosResourceNotFoundError


class GradeYearService:
    _cosmosClient: QuizCosmosClient = getQuizCosmosClient()

    def save(self, item: GradeYear) -> None:
        container = self._cosmosClient.getContainer(GradeYearsContainer.name)
        container.upsert_item(item.toDict())

    def get(self, gradeId: str, academicYear: int) -> GradeYear | None:
        container = self._cosmosClient.getContainer(GradeYearsContainer.name)

        try:
            item = container.read_item(gradeId, str(academicYear))
            return GradeYear.fromDict(item)
        except CosmosResourceNotFoundError:
            return None

    def searchById(self, gradeId: str) -> GradeYear | None:
        container = self._cosmosClient.getContainer(GradeYearsContainer.name)

        query = "select * from c where c.id = @gradeId"
        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@gradeId", value=gradeId)
        ])

        for item in items:
            return GradeYear.fromDict(item)

        return None

    def searchByCodeAndAcademicYear(self, code: str, academicYear: int | None) -> GradeYear | None:
        container = self._cosmosClient.getContainer(GradeYearsContainer.name)

        query = "select * from c where c.code = @code"

        if academicYear is not None:
            query = query + " and c.academicYear = @academicYear"

        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@code", value=code),
            dict(name="@academicYear", value=str(academicYear)),
        ])

        for item in items:
            return GradeYear.fromDict(item)

        return None

    def searchByAcademicYear(self, academicYear: int | None) -> list[GradeYear]:
        container = self._cosmosClient.getContainer(GradeYearsContainer.name)

        query = "select * from c where c.academicYear = @academicYear"

        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@academicYear", value=str(academicYear)),
        ])

        return [GradeYear.fromDict(x) for x in items]

    def getAll(self) -> list[GradeYear]:
        container = self._cosmosClient.getContainer(GradeYearsContainer.name)
        items = container.read_all_items()
        return [GradeYear.fromDict(x) for x in items]
