import pytest

from django.forms import Form
from django.forms.widgets import Media

from arctic.generics import View, FormView


class FormWithAssets(Form):
    class Media:
        css = {
            'all': ('form-common.css', 'view-common.css')
        }
        js = ('form1-1.js', 'form-common.js')


class FormWithOutAssets(Form):
    pass


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


class ViewWithForm(FormView, View):
    form_class = FormWithAssets


class FormViewWithOutFormAssets(FormView, View):
    form_class = FormWithOutAssets

    class Media:
        css = {
            'all': ('view.css', 'view-common.css')
        }
        js = ('view.js',)


class FormViewWithAssets(FormView, View):
    form_class = FormWithAssets

    class Media:
        css = {
            'all': ('view.css', 'view-common.css')
        }
        js = ('view.js',)


class FormViewWithAssetsAndExtraAssets(FormView, View):
    form_class = FormWithAssets

    class Media:
        css = {
            'all': ('view.css', 'view-common.css')
        }
        js = ('view.js',)

    def get_media_assets(self):
        return Media(js=['extra.js'])


class ViewWithAssetsAndForms(ViewWithAssets):
    form1 = FormWithAssets
    form2 = AnotherFormWithAssets


@pytest.mark.django_db
class TestViewAssets(object):
    """
    Test media assets in views, including eventual form assets.
    """

    def test_regular_view_with_assets(self):
        view = ViewWithAssets()
        response = """<link href="/static/view.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet">
<script type="text/javascript" src="/static/view.js"></script>"""  # noqa

        assert str(view.media).replace(' />', '>') == response

    def _regular_view_with_media(self, settings):
        settings.ARCTIC_COMMON_MEDIA_ASSETS = {
            'css': {
                'all': ['common.css']
            }
        }
        view = ViewWithAssets()
        response = """<link href="/static/common.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet">
<script type="text/javascript" src="/static/view.js"></script>"""  # noqa

        assert str(view.media).replace(' />', '>') == response

    def test_view_with_assets_and_forms(self):
        view = ViewWithAssetsAndForms()
        response = """<link href="/static/view.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet">
<script type="text/javascript" src="/static/view.js"></script>"""  # noqa

        assert str(view.media).replace(' />', '>') == response

    def test_form_view_with_form(self, rf):
        view = ViewWithForm()
        request = rf.get('/')
        view.request = request
        response = """<link href="/static/form-common.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet">
<script type="text/javascript" src="/static/form1-1.js"></script>
<script type="text/javascript" src="/static/form-common.js"></script>"""  # noqa

        assert str(view.media).replace(' />', '>') == response

    def _form_view_with_form_and_common_assets(self, rf, settings):
        settings.ARCTIC_COMMON_MEDIA_ASSETS = {
            'js': ['common.js']
        }
        view = ViewWithForm()
        request = rf.get('/')
        view.request = request
        response = """<link href="/static/form-common.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet">
<script type="text/javascript" src="/static/common.js"></script>
<script type="text/javascript" src="/static/form1-1.js"></script>
<script type="text/javascript" src="/static/form-common.js"></script>"""  # noqa

        assert str(view.media).replace(' />', '>') == response

    def _form_view_with_assets_and_form(self, rf):
        view = FormViewWithAssets()
        request = rf.get('/')
        view.request = request
        response = """<link href="/static/view.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/form-common.css" type="text/css" media="all" rel="stylesheet">
<script type="text/javascript" src="/static/view.js"></script>
<script type="text/javascript" src="/static/form1-1.js"></script>
<script type="text/javascript" src="/static/form-common.js"></script>"""  # noqa

        assert str(view.media).replace(' />', '>') == response

    def _form_view_with_assets_and_form_and_extra_assets(self, rf):
        view = FormViewWithAssetsAndExtraAssets()
        request = rf.get('/')
        view.request = request
        response = """<link href="/static/view.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/form-common.css" type="text/css" media="all" rel="stylesheet">
<script type="text/javascript" src="/static/view.js"></script>
<script type="text/javascript" src="/static/form1-1.js"></script>
<script type="text/javascript" src="/static/form-common.js"></script>
<script type="text/javascript" src="/static/extra.js"></script>"""  # noqa

        assert str(view.media).replace(' />', '>') == response

    def test_form_view_without_form_assets(self, rf):
        view = FormViewWithOutFormAssets()
        request = rf.get('/')
        view.request = request
        response = """<link href="/static/view.css" type="text/css" media="all" rel="stylesheet">
<link href="/static/view-common.css" type="text/css" media="all" rel="stylesheet">
<script type="text/javascript" src="/static/view.js"></script>"""  # noqa

        assert str(view.media).replace(' />', '>') == response

    def test_view_without_assets(self):
        view = View()

        assert str(view.media) == ''
