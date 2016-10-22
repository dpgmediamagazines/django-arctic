import pytest

from arctic.generics import ListView
from .conftest import article


@pytest.fixture
def virtual_fields_example_1():
    class TestListView(ListView):
        paginate_by = 2
        fields = ['title', 'description', 'published', 'content_type']
        permission_required = "articles_view"
        queryset = article()

    return TestListView()


def test_virtual_fields_example_1(article, virtual_fields_example_1):
    list_view = virtual_fields_example_1

    with pytest.raises(AttributeError) as excinfo:
        list_view.get_list_items([article])

    message = "'Article' object has no attribute 'content_type'"
    assert str(excinfo.value) == message


@pytest.fixture
def virtual_fields_example_2():
    class TestListView(ListView):
        paginate_by = 2
        fields = ['title', 'description', 'published', 'virtual_field']
        permission_required = "articles_view"
        queryset = article()

        def get_virtual_field_field(self, row):
            return 'Virtual Field: ' + row.title

    return TestListView()


def test_virtual_fields_example_2(article, virtual_fields_example_2):
    list_view = virtual_fields_example_2
    res = list_view.get_list_items([article])

    assert res[0][0] is None
    assert res[0][1] == 'title1'
    assert res[0][2] == 'description1'
    assert res[0][3] == 'published1'
    assert res[0][4] == 'Virtual Field: title1'


@pytest.fixture
def virtual_fields_example_3():
    class TestListView(ListView):
        paginate_by = 2
        fields = ['title', 'description', 'published', 'virtual_field']
        permission_required = "articles_view"
        queryset = article()

    return TestListView()


def test_virtual_fields_example_3(article, virtual_fields_example_3):
    list_view = virtual_fields_example_3

    with pytest.raises(AttributeError) as excinfo:
        list_view.get_list_items([article])

    message = "'Article' object has no attribute 'virtual_field'"
    assert str(excinfo.value) == message
