from data.cosmosDb import QuizCosmosClient
from data.models import GradeYear
from azure.cosmos.exceptions import CosmosResourceNotFoundError


class GradeYearService:
    _cosmosClient: QuizCosmosClient = QuizCosmosClient()

    def save(self, item: GradeYear) -> None:
        container = self._cosmosClient.getGradeYearsContainerClient()
        container.upsert_item(item.toDict())

    def get(self, gradeId: str, academicYear: int) -> GradeYear | None:
        container = self._cosmosClient.getGradeYearsContainerClient()

        try:
            item = container.read_item(gradeId, str(academicYear))
            return GradeYear.fromDict(item)
        except CosmosResourceNotFoundError:
            return None

    def searchById(self, gradeId: str) -> GradeYear | None:
        container = self._cosmosClient.getGradeYearsContainerClient()

        query = "select * from c where c.id = @gradeId"
        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@gradeId", value=gradeId)
        ])

        for item in items:
            return GradeYear.fromDict(item)

        return None

    def searchByCode(self, code: str, academicYear: str | None) -> GradeYear | None:
        container = self._cosmosClient.getGradeYearsContainerClient()

        query = "select * from c where c.code = @code"

        if academicYear is not None:
            query = query + " and c.academicYear = @academicYear"

        items = container.query_items(query=query, enable_cross_partition_query=True, parameters=[
            dict(name="@code", value=code),
            dict(name="@academicYear", value=academicYear),
        ])

        for item in items:
            return GradeYear.fromDict(item)

        return None

    def getAll(self) -> list[GradeYear]:
        container = self._cosmosClient.getGradeYearsContainerClient()

        result = []
        items = container.read_all_items()

        for item in items:
            result.append(GradeYear.fromDict(item))

        return result
