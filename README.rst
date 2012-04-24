================================
purl - A simple Python URL class
================================

A simple, immutable URL class with a clean API for interrogation and
manipulation.

Install
-------

From PyPI (stable)::

    pip install purl

From Github (unstable)::

    pip install git+git://github.com/codeinthehole/purl.git#egg=purl

Use
---

Construct::

    from purl import URL

    # Explicit constructor
    u = URL(scheme='https', host='www.google.com', path='/search', query='q=testing')

    # Use factory
    u = URL.from_string('https://www.google.com/search?q=testing')

    # Combine
    u = URL.from_string('http://www.google.com').path('search') \
                                                .query_param('q', 'testing')

URL objects are immutable - all mutator methods return a new instance.

Interrogate::

    u.scheme()      # 'https'
    u.host()        # 'www.google.com' 
    u.domain()      # 'www.google.com' - alias of host
    u.port()        # None - only returns value if explicitly set
    u.path()        # '/search'
    u.query()       # 'q=testing'
    u.fragment()    # 'q=testing'

    u.path_segment(0)   # 'search'
    u.path_segments()   # ('search',)
    u.query_param('q')  # 'testing'
    u.query_param('q', as_list=True)  # ['testing']
    u.query_param('lang', default='GB')  # 'GB'
    u.query_params()    # {'q': 'testing'}

    u.subdomains()   # ['www', 'google', 'com']
    u.subdomain(0)   # 'www'

Note that each accessor method is overloaded to be a mutator method too, similar
to the jQuery API.  Eg::

    u = URL.from_string('https://github.com/codeinthehole')

    # Access
    u.path_segment(0) # returns 'codeinthehole'

    # Mutate (creates a new instance)
    new_url = u.path_segment(0, 'tangentlabs') # returns new URL object

Couple of other things:

* Since the URL class is immutable it can be used as a key in a dictionary
* It can be picked and restored
* It supports equality operations

Changelog
---------

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
* Added __slots__ so instances can be used as keys within dictionaries

Contribute
----------

Clone and install testing dependencies::

    pip install -r requirements.txt

Ensure tests pass::

    nosetests

Hack away

Build status
------------

.. image:: https://secure.travis-ci.org/codeinthehole/purl.png

