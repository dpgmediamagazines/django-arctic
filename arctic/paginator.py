from django.core.paginator import Paginator, Page, EmptyPage
from django.utils.functional import cached_property


class IndefinitePaginator(Paginator):
    has_next = False

    @cached_property
    def count(self):
        try:
            return super(IndefinitePaginator, self).count
        except ValueError:
            # count is unknown, but we still want pagination
            return -1

    @cached_property
    def num_pages(self):
        if self.count == -1:
            return -1
        return super(IndefinitePaginator, self).num_pages

    def page(self, number):
        number = self.validate_number(number)
        bottom = (number - 1) * self.per_page
        top = bottom + self.per_page
        # we don't know the total amount of items, so we ask for one extra item
        # if it exists then there's a next page
        object_list = self.object_list[bottom : top + 1]
        if len(object_list) > self.per_page:
            self.has_next = True
            object_list = object_list[:-1]
        return self._get_page(object_list, number, self)

    def _get_page(self, *args, **kwargs):
        return IndefinitePage(*args, **kwargs)

    def validate_number(self, number):
        try:
            return super(IndefinitePaginator, self).validate_number(number)
        except EmptyPage:
            if self.count == -1:
                return number
            raise


class IndefinitePage(Page):
    def __init__(self, object_list, number, paginator):
        self.object_list = object_list
        self.number = number
        self.paginator = paginator

    def has_next(self):
        return self.paginator.has_next

    def end_index(self):
        return self.start_index() + len(self.object_list) - 1
