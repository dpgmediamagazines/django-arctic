import pytest

from django.forms import Form

from arctic.generics import View


class FormWithAssets(Form):
    class Media:
        css = {
            'all': ('form-common.css', 'view-common.css')
        }
        js = ('form1-1.js', 'form-common.js')


class AnotherFormWithAssets(Form):
    class Media:
        css = {
            'all': ('form-common.css', 'form2.css')
        }
        js = ('form2-1.js', 'form-common.js')


class ViewWithAssets(View):
    class Media:
        css = {
            'all': ('view.css', 'view-common.css')
        }
        js = ('view.js',)


class ViewWithAssetsAndForms(ViewWithAssets):
    form1 = FormWithAssets
    form2 = AnotherFormWithAssets


@pytest.mark.django_db
class TestViewAssets(object):
    """
    Test media assets in views, including eventual form assets.
    """

    def test_view_with_assets(self):
        view = ViewWithAssets()
        response = """<link href="/static/view.css" type="text/css" media="all" rel="stylesheet" />
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet" />
<script type="text/javascript" src="/static/view.js"></script>"""  # noqa

        assert str(view.media) == response

    def test_view_with_assets_and_forms(self):
        view = ViewWithAssetsAndForms()
        response = """<link href="/static/view.css" type="text/css" media="all" rel="stylesheet" />
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet" />
<link href="/static/form-common.css" type="text/css" media="all" rel="stylesheet" />
<link href="/static/form2.css" type="text/css" media="all" rel="stylesheet" />
<script type="text/javascript" src="/static/view.js"></script>
<script type="text/javascript" src="/static/form1-1.js"></script>
<script type="text/javascript" src="/static/form-common.js"></script>
<script type="text/javascript" src="/static/form2-1.js"></script>"""  # noqa

        assert str(view.media) == response

    def test_view_without_assets(self):
        view = View()

        assert str(view.media) == ''
