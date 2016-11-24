import datetime

from django.contrib.auth import get_user_model
from factory import DjangoModelFactory, Sequence, \
    SubFactory, fuzzy, PostGenerationMethodCall, post_generation

from arctic.models import Role, UserRole
from articles.models import Article, Category, Tag


class CategoryFactory(DjangoModelFactory):
    name = Sequence(lambda n: 'Category {}'.format(n))

    class Meta:
        model = Category


class TagFactory(DjangoModelFactory):
    term = Sequence(lambda n: 'Tag {}'.format(n))

    class Meta:
        model = Tag


class ArticleFactory(DjangoModelFactory):
    title = Sequence(lambda n: 'Article {}'.format(n))
    category = SubFactory(CategoryFactory)
    updated_at = fuzzy.FuzzyNaiveDateTime(datetime.datetime(2016, 1, 1))

    class Meta:
        model = Article


class UserFactory(DjangoModelFactory):
    email = Sequence(lambda n: 'user{}@test.com'.format(n))
    username = Sequence(lambda n: 'user{}'.format(n))
    password = PostGenerationMethodCall('set_password', 'password')
    is_active = True

    @post_generation
    def set_urole(self, create, *args, **kwargs):
        if create:
            UserRole.objects.create(
                user=self, role=Role.objects.get(name='editor'))

    class Meta:
        model = get_user_model()
