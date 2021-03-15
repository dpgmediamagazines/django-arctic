# TODO: Move extra views into our own views. So we can override where needed
from extra_views import InlineFormSetFactory

from .models import Article, Image


class ArticleInline(InlineFormSetFactory):
    model = Article
    fields = "__all__"


class TagsInline(InlineFormSetFactory):
    model = Article.tags.through
    fields = "__all__"


class ImagesInline(InlineFormSetFactory):
    model = Image
    fields = "__all__"
    layout = {"blah": "bah"}
    sorting_field = "order"
    inline_extra = 1
    factory_kwargs = {"max_num": 7}
