ARCTIC_SITE_NAME = 'Arctic Example'
ARCTIC_FORM_DISPLAY = 'float-label'

# Menu format:
# (('menu label', 'named url', 'optional icon class',
#   (optional submenu), (optional related_urls)) )
ARCTIC_MENU = (
    ('Dashboard', 'index', 'fa-dashboard'),
    ('Articles', None, 'fa-file-text-o', (
        ('List', 'articles:list', ('articles:detail', 'articles:delete')),
        ('Create', 'articles:create'),
    )),
    ('Categories', None, 'fa-sitemap', (
        ('List', 'articles:category-list',
         ('articles:category-detail', 'articles:category-delete')),
        ('Create', 'articles:category-create'),
    )),
    ('Tags', None, 'fa-tags', (
        ('List', 'articles:tag-list',
         ('articles:tag-detail', 'articles:tag-delete')),
        ('Create', 'articles:tag-create'),
    )),
    ('Users', None, 'fa-user', (
        ('List', 'users:list', ('users:detail', )),
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
