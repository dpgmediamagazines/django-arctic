from django.core.paginator import Paginator, Page, EmptyPage
from django.utils.functional import cached_property


class IndefinitePaginator(Paginator):

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
        return self._get_page(self.object_list[bottom:top], number, self)

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

    def has_next(self):
        return self.number < self.paginator.num_pages or \
            self.paginator.num_pages == -1
