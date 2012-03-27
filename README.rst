================================
purl - A simple Python URL class
================================


Install
-------

Still a work-in-progress - not on PyPi yet.

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

Interrogate::

    u.scheme()  # 'https'
    u.host()    # 'www.google.com' 
    u.port()    # 80
    u.path()    # '/search'
    u.query()   # 'q=testing'

    u.path_segment(0)   # 'search'
    u.path_segments()   # ('search',)
    u.query_param('q')  # 'testing'
    u.query_param('lang', default='GB')  # 'GB'

That that each accessor method is overloaded to be a mutator method too,
mimicing the jQuery API.  Eg::

    u = URL.from_string('https://github.com/codeinthehole')

    # Access
    u.path_segment(0) # returns 'codeinthehole'

    # Mutate
    u.path_segment(0, 'tangentlabs') # returns new URL object
