ARCTIC_SITE_NAME = 'Arctic Example'

# Menu format:
# (('menu label', 'named url', 'optional icon class', (optional submenu)))
ARCTIC_MENU = (
    ('Dashboard', 'index', 'fa-dashboard'),
    ('Articles', None, 'fa-file-text-o', (
        ('List', 'articles:list'),
        ('Create', 'articles:create'),
    )),
    ('Categories', None, 'fa-sitemap', (
        ('List', 'articles:category-list'),
        ('Create', 'articles:category-create'),
    )),
    ('Tags', None, 'fa-tags', (
        ('List', 'articles:tag-list'),
        ('Create', 'articles:tag-create'),
    )),
    ('Users', None, 'fa-user', (
        ('List', 'users:list'),
        ('Create', 'users:create'),
    )),
    ('Countries', 'countries-list', 'fa-globe'),
)

ARCTIC_USER_ROLE_MODEL = 'arctic.UserRole'
ARCTIC_ROLE_MODEL = 'arctic.Role'

ARCTIC_ROLES = {
    'editor': (
        'view_dashboard',
        'view_article',
        'change_article',
        'add_article',
    ),
}

ARCTIC_AUTOCOMPLETE = {
    'categories': ('articles.Category', 'name')
}

# ARCTIC_SIDEBAR_BACKGROUND = '#BF1D1D'
# ARCTIC_HIGHLIGHT_COLOR = '#9ec3d5'

# ARCTIC_SIDEBAR_BACKGROUND = '#212050'
# ARCTIC_HIGHLIGHT_COLOR = '#76a2cb'
