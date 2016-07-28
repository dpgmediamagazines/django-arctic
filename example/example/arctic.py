ARCTIC_SITE_NAME = 'Arctic Example'

# Menu format:
# (('menu label', 'named url', 'optional icon class', (optional submenu)))
ARCTIC_MENU = (
    ('Dashboard', 'index', 'fa-dashboard'),
    ('Articles', 'articles:list', 'fa-file-text-o', (
        ('List', 'articles:list', 'fa-list'),
        ('Create', 'articles:create', 'fa-pencil'),
    )),
    ('Categories', 'articles:category-list', 'fa-sitemap', (
        ('List', 'articles:category-list', 'fa-list'),
        ('Create', 'articles:category-create', 'fa-pencil'),
    )),
    ('Tags', 'articles:tag-list', 'fa-tags', (
        ('List', 'articles:tag-list', 'fa-paper'),
        ('Create', 'articles:tag-create', 'fa-pencil'),
    )),
    ('Users', 'users:list', 'fa-user', (
        ('List', 'users:list', 'fa-paper'),
    )),
)

ARCTIC_ROLES = {
    'editor': (
        'articles_view',
        'articles_create',
    ),
}

# ARCTIC_TOPBAR_BACKGROUND_COLOR = '#BF1D1D'
# ARCTIC_HIGHLIGHT_COLOR = '#9ec3d5'