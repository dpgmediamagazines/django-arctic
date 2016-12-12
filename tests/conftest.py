import pytest
from django.contrib.auth import get_user_model

from tests.factories import ArticleFactory, TagFactory

User = get_user_model()


class FormCustomMock(object):
    """
    Custom mock to mimic the get_form() method for the Create and
    Update View. It needs to support self.get_form().fields and
    self.get_form()['fieldname']
    """
    fields = None

    def __init__(self, form):
        self.fields = {field.name: field for field in form}

    def __getitem__(self, key):
        return self.fields[key]

    def get_form(self):
        return self


def get_form(form):
    """
    Helper function to make sure you don't need to know how the
    FormCustomMock works

    Call this one, when you want to have the get_form-method
    """
    form_mock = FormCustomMock(form)
    return form_mock.get_form


@pytest.fixture
def tag():
    return TagFactory()


@pytest.fixture
def article(tag):
    article = ArticleFactory()
    article.tags.add(tag)
    return article
