querydict
=========

A Python library to easily analyze, transform, and filter your
dictionary lists.

## Quick Start

Given a list of dictionaries, you can query the keys.

::

    from querydict import select

    a = [
        {'user': 'mike', 'logins': 1},
        {'user': 'jack', 'logins': 2}
    ]

    results = select('user').from_(a).where(lambda x: x['logins'] < 2)

    for i in results:
        print(i)

    # outputs:
    # {'user': 'mike'}

Usage
-----

The resultant object from a query is a generator object. This allows the
source object to be a generator itself and it won’t consume the
generator.

To collapse the generator into a list you can use the ``all`` method.
This allows you to do sorting on the resultant list within the query.

::

    a = [
        {'user': 'mike', 'logins': 1},
        {'user': 'jack', 'logins': 2}
    ]

    results = select('user').from_(a).all(order_by='logins', desc=True) # all() converts into a list

    for i in results:
        print(i)

    # outputs:
    # {'user': 'mike'}
    # {'user': 'jack'}

``order_by`` and ``desc`` are optional. By default it will return
records in the same order that they are input.

Aliasing
~~~~~~~~

You can rename a field by using the ‘as’ keyword when selecting a field.
This allows you to do a basic transformation.

::

    a = [
        {'user': 'mike', 'logins': 1},
        {'user': 'jack', 'logins': 2}
    ]

    results = select('user as fname', 'logins as login_count').from_(a)

    for i in results:
        print(i)

    # outputs:
    # {'fname': 'mike', 'login_count': 1}
    # {'fname': 'jack', 'login_count': 2}

Injecting
~~~~~~~~~

If you specify a field that does not exist, that value will be inserted
into the resultant dictionary. If you do not specify an alias, the value
will also be used as a key.

::

    a = [
        {'user': 'mike', 'logins': 1},
        {'user': 'jack', 'logins': 2}
    ]

    results = select('user', 'logins', 5, test as foo).from_(a)

    for i in results:
        print(i)

    # outputs:
    # {'fname': 'mike', 'login_count': 1, '5': 5, 'foo': 'test'}
    # {'fname': 'jack', 'login_count': 2, '5': 5, 'foo': 'test'}

Nested Dictionaries
~~~~~~~~~~~~~~~~~~~

You can refer to nested dictionaries using a dot notation. This works
for both selecting a field and aliasing a field.

::

    a = [
        {'user': {'fname': 'mike'}, 'logins': 1},
        {'user': {'fname': 'jack'}, 'logins': 2}
    ]

    results = select('user.fname', 'logins as meta.logins').from_(a)

    for i in results:
        print(i)

    # outputs:
    # {'user': {'fname': 'mike'}, 'meta': {'logins': 1}}
    # {'user': {'fname': 'jack'}, 'meta': {'logins': 2}}

This allows you to freely unnest or nest fields in your dictionary.
Keeping a consistent key format will allow you to add more data to your
nested dictionary.

::

    a = [
        {'fname': 'mike', 'lname': 'v', 'logins': 1},
        {'fname': 'jack', 'lname': 'l', 'logins': 2}
    ]

    results = select('fname as user.fname', 'lname as user.lname').from_(a)

    for i in results:
        print(i)

    # outputs:
    # {'user': {'fname': 'mike', 'lname': 'v'}}
    # {'user': {'fname': 'jack', 'lname': 'l'}}

Field Operations
~~~~~~~~~~~~~~~~

By referring to fields in the dictionary, you can perform operations on
those fields in the select statement.

::

    a = [
        {'fname': 'mike', 'lname': 'v', 'logins': 1},
        {'fname': 'jack', 'lname': 'l', 'logins': 2}
    ]

    results = select('fname + ' ' + lname as full_name').from_(a)

    for i in results:
        print(i)

    # outputs:
    # {'full_name': 'mike v'}}
    # {'full_name': 'jack l'}}

This can even be used to chain operations in the same select statement:

::

    a = [
        {'user': 'mike', 'values': [10, 5, 3]},
        {'user': 'jack', 'values': [14, 10]}
    ]

    results = select('user', 'sum(values) as sum', 'len(values) as count', 'sum / count as average' ).from_(a)

    for i in results:
        print(i)

    # outputs:
    # {'user': 'mike', 'sum': 18, 'count': 3, 'average': 6.0}
    # {'user': 'jack', 'sum': 24, 'count': 2, 'average': 12.0}

NOTE: THIS IS CURRENTLY NOT WORKING AS EXPECTED FOR NESTED DICTIONARIES
