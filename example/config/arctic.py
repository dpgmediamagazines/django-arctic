from django.utils.translation import ugettext_lazy as _


ARCTIC_SITE_NAME = _("Arctic Example")
ARCTIC_FORM_DISPLAY = "float-label"

# Menu format:
# (('menu label', 'named url', 'optional icon class',
#   (optional submenu), (optional related_urls)) )
ARCTIC_MENU = (
    (_("Dashboard"), "index", "fa-dashboard"),
    (
        _("Articles"),
        None,
        "fa-file-text-o",
        (
            (
                _("List"),
                "articles:list",
                ("articles:detail", "articles:delete"),
            ),
            (_("Create"), "articles:create"),
        ),
    ),
    (
        _("Categories"),
        None,
        "fa-sitemap",
        (
            (
                _("List"),
                "articles:category-list",
                ("articles:category-detail", "articles:category-delete"),
            ),
            (_("Create"), "articles:category-create"),
        ),
    ),
    (
        _("Tags"),
        None,
        "fa-tags",
        (
            (
                _("List"),
                "articles:tag-list",
                ("articles:tag-detail", "articles:tag-delete"),
            ),
            (_("Create"), "articles:tag-create"),
        ),
    ),
    (
        _("Users"),
        None,
        "fa-user",
        (
            (_("List"), "users:list", ("users:detail",)),
            (_("Create"), "users:create"),
        ),
    ),
    (_("Countries"), "countries-list", "fa-globe"),
)

ARCTIC_USER_ROLE_MODEL = "arctic.UserRole"
ARCTIC_ROLE_MODEL = "arctic.Role"

ARCTIC_ROLES = {
    "editor": (
        "view_dashboard",
        "view_article",
        "change_article",
        "add_article",
    )
}

ARCTIC_AUTOCOMPLETE = {"categories": ("articles.Category", "name")}

ARCTIC_DARK_MODE = True
# ARCTIC_DARK_MODE = 'toggle'

# ARCTIC_SIDEBAR_BACKGROUND = '#BF1D1D'
# ARCTIC_HIGHLIGHT_COLOR = '#9ec3d5'

# ARCTIC_SIDEBAR_BACKGROUND = '#212050'
# ARCTIC_HIGHLIGHT_COLOR = '#76a2cb'

# ARCTIC_SIDEBAR_BACKGROUND_DARK = '#FF0000'
# ARCTIC_SIDEBAR_COLOR_DARK = '#00FF00'
# ARCTIC_SIDEBAR_ALT_COLOR_DARK = '#0000FF'
