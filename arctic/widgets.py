from django import forms


class RichTextArea(forms.Textarea):
    """
    Richtext editor field. We currently use TinyMCE.
    """
    html = '<div class="richtexteditor" ' \
           'data-tinymce_plugins="{plugins}" ' \
           'data-tinymce_toolbar="{toolbar}">' \
           '<div></div>' \
           '<textarea class="hidden"></textarea>' \
           '</div>'

    def render(self, name, value, attrs=None, rte_plugins='', rte_toolbar=''):
        return self.html.format(plugins=rte_plugins, toolbar=rte_toolbar)
