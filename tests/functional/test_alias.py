import pytest
from querydict import select


@pytest.mark.parametrize("test", [
    dict(
        select=['fname as first_name', 'lname as last_name'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'first_name': 'John', 'last_name': 'Doe'},
            {'first_name': 'Jane', 'last_name': 'Doe'}
        ]
    ),
    dict(
        select=['logins as login_count'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'login_count': 1},
            {'login_count': 3}
        ]
    ),
])
def test_select_specific_keys_with_alias(test):
    results = select(*test['select']).from_(test['input'])
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=['fname', 'lname', 'logins as login_count'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'login_count': 1},
        ],
        where=lambda x: x['login_count'] < 3
    ),
    dict(
        select=['fname as first_name'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'first_name': 'John'},
        ],
        where=lambda x: x['first_name'] == 'John'
    ),
    dict(
        select=['fname as first_name', 'lname as last_name'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'first_name': 'John', 'last_name': 'Doe'},
            {'first_name': 'Jane', 'last_name': 'Doe'}
        ],
        where=lambda x: x['last_name'] == 'Doe'
    )
])
def test_where_with_alias(test):
    results = select(
        *test['select']
    ).from_(
        test['input']
    ).where(
        test['where']
    )
    assert (not hasattr(results, '__len__'))

    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=['fname', 'logins as login_count'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2}
        ],
        expected=[
            {'fname': 'John', 'login_count': 1},
            {'fname': 'Bob', 'login_count': 2},
            {'fname': 'Jane', 'login_count': 3}
        ],
        order_by='login_count'
    )
])
def test_sort_with_alias(test):
    results = select(
        *test['select']
    ).from_(
        test['input']
    ).all(order_by=test['order_by'])
    assert results == test['expected']
