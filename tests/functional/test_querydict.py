import pytest
from querydict import select


@pytest.mark.parametrize("test", [
    dict(
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ]
    )
])
def test_select_returns_generator(test):
    results = select().from_(test['input'])

    assert (not hasattr(results, '__len__'))

    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ]
    )
])
def test_select_all_returns_list(test):
    a = [
        {'fname': 'John', 'lname': 'Doe', 'logins': 1},
        {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
    ]

    results = select().from_(a).all()

    assert (hasattr(results, '__len__'))

    for i, item in enumerate(results):
        assert item == a[i]


@pytest.mark.parametrize("test", [
    dict(
        select=['fname', 'lname'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe'},
            {'fname': 'Jane', 'lname': 'Doe'}
        ]
    ),
    dict(
        select=['logins'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'logins': 1},
            {'logins': 3}
        ]
    ),
])
def test_select_specific_keys(test):
    results = select(*test['select']).from_(test['input'])
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=['*'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ]
    )
])
def test_all_keys(test):
    results = select(*test['select']).from_(test['input'])
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=['*', '5 as number'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1, 'number': 5},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3, 'number': 5}
        ]
    ),
    dict(
        select=['fname', 'test as string_test'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'string_test': 'test'},
            {'fname': 'Jane', 'string_test': 'test'}
        ]
    ),
    dict(
        select=['fname', 'fname as first_name'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'first_name': 'John'},
            {'fname': 'Jane', 'first_name': 'Jane'}
        ]
    ),
    dict(
        select=['fname', 1],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', '1': 1},
            {'fname': 'Jane', '1': 1}
        ]
    )
])
def test_field_injection(test):
    results = select(*test['select']).from_(test['input'])
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=['*', "fname + ' ' + lname as full_name"],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1, 'full_name': 'John Doe'},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3, 'full_name': 'Jane Doe'}
        ]
    ),
    dict(
        select=['fname', 'sum', 'count', 'sum / count as average'],
        input=[
            {'fname': 'John', 'sum': 100, 'count': 5},
            {'fname': 'Bill', 'sum': 100, 'count': 10},
        ],
        expected=[
            {'fname': 'John', 'sum': 100, 'count': 5, 'average': 100 / 5},
            {'fname': 'Bill', 'sum': 100, 'count': 10, 'average': 100 / 10},
        ]
    ),
    dict(
        select=['fname', 'sum(values) as sum', 'len(values) as count', 'sum / count as average'],
        input=[
            {'fname': 'John', 'values': [10, 20, 30]},
            {'fname': 'Bill', 'values': [1, 2, 3, 4, 5]},
        ],
        expected=[
            {'fname': 'John', 'sum': 60, 'count': 3, 'average': 60 / 3},
            {'fname': 'Bill', 'sum': 15, 'count': 5, 'average': 15 / 5},
        ]
    )
])
def test_field_injection_calc(test):
    results = select(*test['select']).from_(test['input'])
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=[],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
        ],
        where=lambda x: x['logins'] < 3
    ),
    dict(
        select=[],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
        ],
        where=lambda x: x['fname'] == 'John'
    ),
    dict(
        select=[],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        where=lambda x: x['lname'] == 'Doe'
    ),
])
def test_where_filter(test):
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
        select=[],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
        ],
        expected=[
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
        ],
        where=[
            lambda x: x['logins'] < 3,
            lambda x: x['logins'] > 1
        ]
    )
])
def test_multiple_where_filter(test):
    results = select(
        *test['select']
    ).from_(
        test['input']
    ).where(
        *test['where']
    )
    assert (not hasattr(results, '__len__'))
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=[],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
        ],
        expected=[
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
        ],
        where=[
            lambda x: x['logins'] < 3,
            lambda x: x['logins'] > 1
        ]
    )
])
def test_chain_where_filter(test):
    results = select(
        *test['select']
    ).from_(
        test['input']
    ).where(
        test['where'][0]
    ).where(
        test['where'][1]
    )
    assert (not hasattr(results, '__len__'))
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        order_by='logins'
    )
])
def test_sort(test):
    results = select(
    ).from_(
        test['input']
    ).all(order_by=test['order_by'])
    assert results == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2}
        ],
        expected=[
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
            {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
            {'fname': 'John', 'lname': 'Doe', 'logins': 1}
        ],
        order_by='logins'
    )
])
def test_sort_descending(test):
    results = select(
    ).from_(
        test['input']
    ).all(order_by=test['order_by'], desc=True)
    assert results == test['expected']
