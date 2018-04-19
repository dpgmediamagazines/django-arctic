# Working with Forms

Arctic Forms, like the ListViews, add features not present in the standard 
django generics, there are three different views available: `CreateView`, 
`UpdateView` and `FormView`, they all share similar features.

It is recomended to use the project created in the [Lists](lists.md) chapter as
a base to try the examples on this one.

## Actions

By default the Forms include a `Submit` button, but more can be added by using 
the `actions` property, for example:

    actions = [
        ('Back to list', 'articles:list'),
    ]

This will create an extra button that links to the article list, more can be 
added and they will all be displayed as secondary links at the end of the form.

## Layouts

## Inlines

## Widgets