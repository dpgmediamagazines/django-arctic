ARCTIC_SITE_NAME = 'Arctic Example'

# Menu format:
# (('menu label', 'named url', 'optional icon class', (optional submenu)))
ARCTIC_MENU = (
    ('Dashboard', 'index', 'fa-dashboard'),
    ('Articles', 'articles:list', 'fa-file-text-o', (
        ('List', 'articles:list', 'fa-list'),
        ('Create', 'articles:create', 'fa-pencil'),
    )),
    ('Categories', 'articles:category-list', 'fa-file-text-o', (
        ('List', 'articles:category-list', 'fa-list'),
        ('Create', 'articles:category-create', 'fa-pencil'),
    )),
    # ('Images', 'images:list', 'fa-picture-o', (
    #     ('Browse', 'images:list', 'fa-paper'),
    #     ('New', 'images:list', 'fa-pencil'),
    # )),
)


