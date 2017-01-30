Django URL Objects = URLjects
=============================

[![Travis CL](https://img.shields.io/travis/Visgean/urljects.svg)](https://travis-ci.org/Visgean/urljects)
[![Documentation Status](https://readthedocs.org/projects/urljects/badge/?version=latest)](https://urljects.readthedocs.org/en/latest/)
[![Pypi](https://img.shields.io/pypi/v/urljects.svg)](https://pypi.python.org/pypi/urljects)
[![Code Health](https://landscape.io/github/Visgean/urljects/master/landscape.svg?style=flat)](https://landscape.io/github/Visgean/urljects/master)
[![Requirements Status](https://requires.io/github/Visgean/urljects/requirements.svg?branch=master)](https://requires.io/github/Visgean/urljects/requirements/?branch=master)
[![Coverage Status](https://coveralls.io/repos/Visgean/urljects/badge.svg?branch=master&service=github)](https://coveralls.io/github/Visgean/urljects?branch=master)


Getting rid of ``urls.py``
--------------------------

With the use of ``include_view()`` you can avoid ``urls.py`` and include
your app's views directly in root ``urls.py``.

```python
    # inside your root urls.py
    urlpatterns = [
        # old style
        url("myapp/", include("myapp.urls")),
        # new urljects style
        url("myapp/", view_include("myapp.views"))
    ]
```

Soo how to define URLs directly into views?
""""""""""""""""""""""""""""""""""""""""""""

I am glad you asked! For class based views simply inherit from ``URLView``.

```python
class ItemDetail(URLView, DetailView):
    name = 'detail'
    url = U / 'detail' / slug
```

a lot of people enjoy functional views, for those there is ``url_view`` decorator.

```python
@url_view(U / 'category' / rest)
def detail(request, rest)
    ...
```

After that you can user ``view_include`` instead of creating ``urls.py`` and
then old-style ``include`` them afterwards.


Keeping ``urls.py``
-------------------

Quite often you need some ``urls.py`` - for example your root urls. Then you can
use patterns like ``slug`` or ``rest`` as shown above inside your ``urls.py``.
We even provide modified ``url`` function to strip away the boilerplate of
``.as_view()``,

```python
from urljects import U, slug, url

url_patterns = (
    url(U / 'detail' / slug, view=DetailView),
    # instead of
    url(r'^detail/(?P<slug>[\w-]+)' , view=DetailView.as_view(),
        name='detail'),
)
```

The name of the view has been taken from ``DetailView.url_name``.
There are also some common regular patterns like slugs and UUIDs so that you
can focus on more important stuff than on debugging regular expressions.

