import pytest

from arctic.generics import ListView
from .conftest import article, request


@pytest.fixture
def virtual_fields_example_1():
    class TestListView(ListView):
        paginate_by = 2
        fields = ['title', 'description', 'published', 'content_type']
        permission_required = "articles_view"
        queryset = article()

    return TestListView()


@pytest.mark.django_db
def test_virtual_fields_example_1(virtual_fields_example_1):
    with pytest.raises(AttributeError):
        self = virtual_fields_example_1
        self.request = request('/articles/')
        objects = self.get_object_list()
        self.get_list_items([objects])


@pytest.fixture
def virtual_fields_example_2():
    class TestListView(ListView):
        paginate_by = 2
        fields = ['title', 'description', 'published', 'virtual_field']
        permission_required = "articles_view"
        queryset = article()

        def get_field_virtual_field(self, row):
            return 'Virtual Field: ' + row.title

    return TestListView()


@pytest.mark.django_db
def test_virtual_fields_example_2(virtual_fields_example_2):
    self = virtual_fields_example_2
    self.request = request('/articles/')
    objects = self.get_object_list()
    res = self.get_list_items([objects])

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


@pytest.mark.django_db
def test_virtual_fields_example_3(virtual_fields_example_3):
    with pytest.raises(AttributeError):
        self = virtual_fields_example_3
        self.request = request('/articles/')
        objects = self.get_object_list()
        self.get_list_items([objects])
