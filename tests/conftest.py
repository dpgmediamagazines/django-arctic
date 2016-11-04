from django.contrib.auth import get_user_model

User = get_user_model()


def get_form(form):
    """
    This is a hack to make sure get_form returns what you expect
    the Django way. I don't know why get_form does not work yet.
    """
    def _get_form():
            return {field.name: field for field in form}
    return _get_form
