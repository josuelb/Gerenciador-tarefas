import factory
import factory.fuzzy

from gnc_todo.models import TodosModel, TodoState, UsersModel


class UserFactory(factory.Factory):
    class Meta:
        model = UsersModel

    username = factory.Sequence(lambda n: f'test{n}')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')


class TodoFactory(factory.Factory):
    class Meta:
        model = TodosModel

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1