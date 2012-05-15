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

    >>> from purl import URL

    # String constructor
    >>> from_str = URL('https://www.google.com/search?q=testing')

    # Keyword constructor
    >>> from_kwargs = URL(scheme='https', host='www.google.com', path='/search', query='q=testing')

    # Combine
    >>> from_combo = URL('https://www.google.com').path('search').query_param('q', 'testing')

URL objects are immutable - all mutator methods return a new instance.

Interrogate::

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
to the jQuery API.  Eg::

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

Hence, you can build a URL up in steps::

    >>> u = URL().scheme('http').domain('www.example.com').path('/some/path').query_param('q', 'search term')
    >>> u.as_string()
    u'http://www.example.com/some/path?q=search+term'

Along with the above overloaded methods, there is also a ``add_path_segment``
method for adding a segment at the end of the current path::

    >>> new_url = u.add_path_segment('here')
    >>> new_url.as_string()
    u'http://www.example.com/some/path/here?q=search+term'

Couple of other things:

* Since the URL class is immutable it can be used as a key in a dictionary
* It can be picked and restored
* It supports equality operations

Changelog
---------

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

Clone and install testing dependencies::

    pip install -r requirements.txt

Ensure tests pass::

    ./runtests.sh

Hack away

Build status
------------

.. image:: https://secure.travis-ci.org/codeinthehole/purl.png

