from django.urls import reverse


def test_article_list(admin_client, article):
    response = admin_client.get(reverse('articles:list'))
    assert response.status_code == 200
    list_items = response.context['list_items'][0]['fields']
    item_dict = {}
    for item in list_items:
        try:
            field = item['field']
            value = item['value']
        except (KeyError, TypeError):
            # Not a dict, so continue
            continue

        item_dict[field] = value

    assert item_dict['tags'][0] == 'Tag 0'
    assert item_dict['category'] == 'Category 0'
    assert item_dict['title'] == 'Article 0'
    assert item_dict['description'] == ''
