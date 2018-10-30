from __future__ import absolute_import, unicode_literals

from arctic.forms import SimpleSearchForm
from arctic.widgets import QuickFiltersSelect
from django import forms
from django.db.models import Q

from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        fields = [
            "title",
            "description",
            "category",
            "updated_at",
            "tags",
            "published",
        ]
        model = Article

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields["category"].empty_label = ""


class AdvancedArticleSearchForm(forms.Form):
    description = forms.CharField(
        max_length=100, required=False, label="Description"
    )

    def __init__(self, data):
        # Reset data, but store for get_search_filter
        self.stored_data = data
        super(AdvancedArticleSearchForm, self).__init__(data)

    def get_search_filter(self):
        value = self.cleaned_data.get("description")
        if value:
            return Q(description__icontains=value)
        return Q()


class FiltersAndSearchForm(SimpleSearchForm):
    field_order = ["published", "search"]
    FILTER_CHOICES = (("published", "Published"), ("drafts", "Drafts"))
    published = forms.ChoiceField(
        choices=FILTER_CHOICES,
        widget=QuickFiltersSelect(attrs={"class": "spacer", "submit": True}),
        required=False,
    )
    # date = forms.CharField(required=False,
    #                        widget=DateTimePickerInput(
    #                            attrs={'placeholder': 'Start date'}))

    def get_search_filter(self):
        q = super(FiltersAndSearchForm, self).get_search_filter()

        published_value = self.cleaned_data.get("published")
        if published_value in ("published", "drafts"):
            published = True if published_value == "published" else False

            q &= Q(published=published)
        return q
