# TODO: Move extra views into our own views. So we can override where needed
from extra_views import InlineFormSet

from .models import Article, Image


class ArticleInline(InlineFormSet):
    model = Article
    fields = "__all__"


class TagsInline(InlineFormSet):
    model = Article.tags.through
    fields = "__all__"


class ImagesInline(InlineFormSet):
    verbose_name = 'Images'
    model = Image
    fields = "__all__"
