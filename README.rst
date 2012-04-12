================================
purl - A simple Python URL class
================================

A simple, immutable URL class with a clean API for interrogation and
manipulation.

.. image:: https://secure.travis-ci.org/codeinthehole/purl.png

Install
-------

Still a work-in-progress - not on PyPi yet, but you can install directly from
Github::

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
    u.port()        # 80
    u.path()        # '/search'
    u.query()       # 'q=testing'
    u.fragment()    # 'q=testing'

    u.path_segment(0)   # 'search'
    u.path_segments()   # ('search',)
    u.query_param('q')  # 'testing'
    u.query_param('q', as_list=True)  # ['testing']
    u.query_param('lang', default='GB')  # 'GB'
    u.query_params()    # {'q': 'testing'}

    u.subdmains()   # ['www', 'google', 'com']
    u.subdmain(0)   # 'www'

Note that each accessor method is overloaded to be a mutator method too, similar
to the jQuery API.  Eg::

    u = URL.from_string('https://github.com/codeinthehole')

    # Access
    u.path_segment(0) # returns 'codeinthehole'

    # Mutate (creates a new instance)
    new_url = u.path_segment(0, 'tangentlabs') # returns new URL object

Contribute
----------

Clone and install testing dependencies::

    pip install -r requirements.txt

Ensure tests pass::

    nosetests

Hack away

