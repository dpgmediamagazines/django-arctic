# TODO: Move extra views into our own views. So we can override where needed
from extra_views import InlineFormSet

from .models import Article


class ArticleInline(InlineFormSet):
    model = Article
    extra = 0
    fields = "__all__"


class TagsInline(InlineFormSet):
    model = Article.tags.through
    extra = 3
    fields = "__all__"
