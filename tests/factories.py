import datetime

from factory import DjangoModelFactory, Sequence, SubFactory, fuzzy

from articles.models import Article, Category


class CategoryFactory(DjangoModelFactory):
    name = Sequence(lambda n: 'Category {}'.format(n))

    class Meta:
        model = Category


class ArticleFactory(DjangoModelFactory):
    title = Sequence(lambda n: 'Article {}'.format(n))
    category = SubFactory(CategoryFactory)
    updated_at = fuzzy.FuzzyNaiveDateTime(datetime.datetime(2016, 1, 1))

    class Meta:
        model = Article
