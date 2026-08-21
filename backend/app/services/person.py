from app.models.person import Person
from app.repositories.person import PersonRepository
from app.schemas.person import PersonCreate


class PersonService:
    def __init__(self, repository: PersonRepository) -> None:
        self.repository = repository

    async def create_person(
        self,
        person_data: PersonCreate,
        user_id: int,
    ) -> Person:
        person = Person(
            user_id=user_id,
            name=person_data.name,
            email=person_data.email,
            relationship_label=person_data.relationship_label,
            usual_response_days=person_data.usual_response_days,
            last_interaction=person_data.last_interaction,
        )

        return await self.repository.create(person)

    async def list_people(self, user_id: int) -> list[Person]:
        return await self.repository.get_all_for_user(user_id)
