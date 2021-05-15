================================
purl - A simple Python URL class
================================

A simple, immutable URL class with a clean API for interrogation and
manipulation.  Supports Pythons 3.3, 3.4, 3.5, 3.6, 3.7, 3.8 and pypy.

Also supports template URLs as per `RFC 6570`_

Contents:

.. contents:: :local:
    :depth: 1

.. image:: https://secure.travis-ci.org/codeinthehole/purl.png
    :target: https://travis-ci.org/codeinthehole/purl

.. image:: https://img.shields.io/pypi/v/purl.svg
    :target: https://crate.io/packages/purl/

.. _`RFC 6570`: http://tools.ietf.org/html/rfc6570

Docs
----

http://purl.readthedocs.org/en/latest/

Install
-------

From PyPI (stable)::

    $ pip install purl

From Github (unstable)::

    $ pip install git+git://github.com/codeinthehole/purl.git#egg=purl

Use
---

Construct:

.. code:: python

    >>> from purl import URL

    # String constructor
    >>> from_str = URL('https://www.google.com/search?q=testing')

    # Keyword constructor
    >>> from_kwargs = URL(scheme='https', host='www.google.com', path='/search', query='q=testing')

    # Combine
    >>> from_combo = URL('https://www.google.com').path('search').query_param('q', 'testing')

URL objects are immutable - all mutator methods return a new instance.

Interrogate:

.. code:: python

    >>> u = URL('https://www.google.com/search?q=testing')
    >>> u.scheme()
    'https'
    >>> u.host()
    'www.google.com'
    >>> u.domain()
    'www.google.com'
    >>> u.username()
    >>> u.password()
    >>> u.netloc()
    'www.google.com'
    >>> u.port()
    >>> u.path()
    '/search'
    >>> u.query()
    'q=testing'
    >>> u.fragment()
    ''
    >>> u.path_segment(0)
    'search'
    >>> u.path_segments()
    ('search',)
    >>> u.query_param('q')
    'testing'
    >>> u.query_param('q', as_list=True)
    ['testing']
    >>> u.query_param('lang', default='GB')
    'GB'
    >>> u.query_params()
    {'q': ['testing']}
    >>> u.has_query_param('q')
    True
    >>> u.has_query_params(('q', 'r'))
    False
    >>> u.subdomains()
    ['www', 'google', 'com']
    >>> u.subdomain(0)
    'www'

Note that each accessor method is overloaded to be a mutator method too, similar
to the jQuery API.  Eg:

.. code:: python

    >>> u = URL.from_string('https://github.com/codeinthehole')

    # Access
    >>> u.path_segment(0)
    'codeinthehole'

    # Mutate (creates a new instance)
    >>> new_url = u.path_segment(0, 'tangentlabs')
    >>> new_url is u
    False
    >>> new_url.path_segment(0)
    'tangentlabs'

Hence, you can build a URL up in steps:

.. code:: python

    >>> u = URL().scheme('http').domain('www.example.com').path('/some/path').query_param('q', 'search term')
    >>> u.as_string()
    'http://www.example.com/some/path?q=search+term'

Along with the above overloaded methods, there is also a ``add_path_segment``
method for adding a segment at the end of the current path:

.. code:: python

    >>> new_url = u.add_path_segment('here')
    >>> new_url.as_string()
    'http://www.example.com/some/path/here?q=search+term'

Couple of other things:

* Since the URL class is immutable it can be used as a key in a dictionary
* It can be pickled and restored
* It supports equality operations
* It supports equality operations

URL templates can be used either via a ``Template`` class:

.. code:: python

    >>> from purl import Template
    >>> tpl = Template("http://example.com{/list*}")
    >>> url = tpl.expand({'list': ['red', 'green', 'blue']})
    >>> url.as_string()
    'http://example.com/red/green/blue'

or the ``expand`` function:

.. code:: python

    >>> from purl import expand
    >>> expand(u"{/list*}", {'list': ['red', 'green', 'blue']})
    '/red/green/blue'

A wide variety of expansions are possible - refer to the RFC_ for more details.

.. _RFC: http://tools.ietf.org/html/rfc6570

Changelog
---------

v1.5 - 2019-03-10
~~~~~~~~~~~~~~~~~

* Allow `@` in passwords.

v1.4 - 2018-03-11
~~~~~~~~~~~~~~~~~

* Allow usernames and passwords to be removed from URLs.

v1.3.1
~~~~~~

* Ensure paths always have a leading slash.

v1.3
~~~~

* Allow absolute URLs to be converted into relative.

v1.2
~~~~

* Support password-less URLs.
* Allow slashes to be passed as path segments.

v1.1
~~~~

* Support setting username and password via mutator methods

v1.0.3
~~~~~~

* Handle some unicode compatibility edge-cases

v1.0.2
~~~~~~

* Fix template expansion bug with no matching variables being passed in. This
  ensures ``purl.Template`` works correctly with the URLs returned from the
  Github API.

v1.0.1
~~~~~~

* Fix bug with special characters in paths not being escaped.

v1.0
~~~~

* Slight tidy up. Document support for PyPy and Python 3.4.

v0.8
~~~~

* Support for RFC 6570 URI templates

v0.7
~~~~

* All internal strings are unicode.
* Support for unicode chars in path, fragment, query, auth added.

v0.6
~~~~

* Added ``append_query_param`` method
* Added ``remove_query_param`` method

v0.5
~~~~

* Added support for Python 3.2/3.3 (thanks @pmcnr and @mitchellrj)

v0.4.1
~~~~~~

* Added API docs
* Added to readthedocs.org

v0.4
~~~~

* Modified constructor to accept full URL string as first arg
* Added ``add_path_segment`` method

v0.3.2
~~~~~~

* Fixed bug port number in string when using from_string constructor

v0.3.1
~~~~~~

* Fixed bug with passing lists to query param setter methods

v0.3
~~~~

* Added support for comparison and equality
* Added support for pickling
* Added ``__slots__`` so instances can be used as keys within dictionaries

Contribute
----------

Clone, create a virtualenv then install purl and the packages required for
testing::

    $ git clone git@github.com:codeinthehole/purl.git
    $ cd purl
    $ mkvirtualenv purl  # requires virtualenvwrapper
    (purl) $ make

Ensure tests pass using::

    (purl) $ pytest

or::

    $ tox
