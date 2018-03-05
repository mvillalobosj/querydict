import pytest
from querydict import select


@pytest.mark.parametrize("test", [
    dict(
        input=[
            {'user': {'fname': 'John', 'lname': 'Doe'}, 'logins': 1},
            {'user': {'fname': 'Jane', 'lname': 'Doe'}, 'logins': 3}
        ],
        expected=[
            {'user': {'fname': 'John', 'lname': 'Doe'}, 'logins': 1},
            {'user': {'fname': 'Jane', 'lname': 'Doe'}, 'logins': 3}
        ]
    )
])
def test_nested_select_returns_original(test):
    results = select().from_(test['input'])

    assert (not hasattr(results, '__len__'))

    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=['user.fname', 'user.lname'],
        input=[
            {'user': {'fname': 'John', 'lname': 'Doe'}, 'logins': 1},
            {'user': {'fname': 'Jane', 'lname': 'Doe'}, 'logins': 3}
        ],
        expected=[
            {'user': {'fname': 'John', 'lname': 'Doe'}},
            {'user': {'fname': 'Jane', 'lname': 'Doe'}}
        ]
    )
])
def test_select_specific_nested_keys(test):
    results = select(*test['select']).from_(test['input'])
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=['fname as user.fname', 'lname as user.lname'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'user': {'fname': 'John', 'lname': 'Doe'}},
            {'user': {'fname': 'Jane', 'lname': 'Doe'}}
        ]
    )
])
def test_alias_nested_keys(test):
    results = select(*test['select']).from_(test['input'])
    assert list(results) == test['expected']


@pytest.mark.parametrize("test", [
    dict(
        select=['*', '5 as inject.number'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1, 'inject': {'number': 5}},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3, 'inject': {'number': 5}}
        ]
    ),
    dict(
        select=['fname', 'test as inject.string_test'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'inject': {'string_test': 'test'}},
            {'fname': 'Jane', 'inject': {'string_test': 'test'}}
        ]
    ),
    dict(
        select=['fname', 'fname as user.first_name'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'user': {'first_name': 'John'}},
            {'fname': 'Jane', 'user': {'first_name': 'Jane'}}
        ]
    ),
    dict(
        select=['fname', 'bob.bill'],
        input=[
            {'fname': 'John', 'lname': 'Doe', 'logins': 1},
            {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
        ],
        expected=[
            {'fname': 'John', 'bob': {'bill': 'bob.bill'}},
            {'fname': 'Jane', 'bob': {'bill': 'bob.bill'}}
        ]
    )
])
def test_inject_nested_keys(test):
    results = select(*test['select']).from_(test['input'])
    assert list(results) == test['expected']


#@pytest.mark.parametrize("test", [
#    dict(
#        select=['*', "user.fname + ' ' + user.lname as full_name"],
#        input=[
#            {'user': {'fname': 'John', 'lname': 'Doe'}, 'logins': 1},
#            {'user': {'fname': 'Jane', 'lname': 'Doe'}, 'logins': 3}
#        ],
#        expected=[
#            {'user': {'fname': 'John', 'lname': 'Doe'}, 'logins': 1, 'full_name': 'John Doe'},
#            {'user': {'fname': 'Jane', 'lname': 'Doe'}, 'logins': 3, 'full_name': 'Jane Doe'}
#        ]
#    ),
#    dict(
#        select=['fname', 'calc.sum', 'calc.count', 'calc.sum / calc.count as average'],
#        input=[
#            {'fname': 'John', 'calc': {'sum': 100, 'count': 5}},
#            {'fname': 'Bill', 'calc': {'sum': 100, 'count': 10}}
#        ],
#        expected=[
#            {'fname': 'John', 'calc': {'sum': 100, 'count': 5}, 'average': 100 / 5},
#            {'fname': 'Bill', 'calc': {'sum': 100, 'count': 10}, 'average': 100 / 10},
#        ]
#    ),
#    dict(
#        select=['fname', 'sum(values) as sum', 'len(values) as count', 'sum / count as average'],
#        input=[
#            {'fname': 'John', 'calc': {'values': [10, 20, 30]}},
#            {'fname': 'Bill', 'calc': {'values': [1, 2, 3, 4, 5]}}
#        ],
#        expected=[
#            {'fname': 'John', 'sum': 60, 'count': 3, 'average': 60 / 3},
#            {'fname': 'Bill', 'sum': 15, 'count': 5, 'average': 15 / 5},
#        ]
#    )
#])
#def test_field_injection_calc(test):
#    results = select(*test['select']).from_(test['input'])
#    assert list(results) == test['expected']


# @pytest.mark.parametrize("test", [
#     dict(
#         select=[],
#         input=[
#             {'user': {'fname': 'John', 'lname': 'Doe', 'logins': 1}},
#             {'user': {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}}
#         ],
#         expected=[
#             {'user': {'fname': 'John', 'lname': 'Doe', 'logins': 1}}
#         ],
#         where=lambda x: x['user.logins'] < 3
#     ),
#     dict(
#         select=[],
#         input=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
#         ],
#         expected=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#         ],
#         where=lambda x: x['fname'] == 'John'
#     ),
#     dict(
#         select=[],
#         input=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
#         ],
#         expected=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
#         ],
#         where=lambda x: x['lname'] == 'Doe'
#     ),
# ])
# def test_where_filter(test):
#     results = select(
#         *test['select']
#     ).from_(
#         test['input']
#     ).where(
#         test['where']
#     )
#     assert (not hasattr(results, '__len__'))

#     assert list(results) == test['expected']


# @pytest.mark.parametrize("test", [
#     dict(
#         select=[],
#         input=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
#             {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
#         ],
#         expected=[
#             {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
#         ],
#         where=[
#             lambda x: x['logins'] < 3,
#             lambda x: x['logins'] > 1
#         ]
#     )
# ])
# def test_multiple_where_filter(test):
#     results = select(
#         *test['select']
#     ).from_(
#         test['input']
#     ).where(
#         *test['where']
#     )
#     assert (not hasattr(results, '__len__'))
#     assert list(results) == test['expected']


# @pytest.mark.parametrize("test", [
#     dict(
#         select=[],
#         input=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
#             {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
#         ],
#         expected=[
#             {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
#         ],
#         where=[
#             lambda x: x['logins'] < 3,
#             lambda x: x['logins'] > 1
#         ]
#     )
# ])
# def test_chain_where_filter(test):
#     results = select(
#         *test['select']
#     ).from_(
#         test['input']
#     ).where(
#         test['where'][0]
#     ).where(
#         test['where'][1]
#     )
#     assert (not hasattr(results, '__len__'))
#     assert list(results) == test['expected']


# @pytest.mark.parametrize("test", [
#     dict(
#         input=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
#             {'fname': 'Bob', 'lname': 'Test', 'logins': 2}
#         ],
#         expected=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#             {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3}
#         ],
#         order_by='logins'
#     )
# ])
# def test_sort(test):
#     results = select(
#     ).from_(
#         test['input']
#     ).all(order_by=test['order_by'])
#     assert results == test['expected']


# @pytest.mark.parametrize("test", [
#     dict(
#         input=[
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1},
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
#             {'fname': 'Bob', 'lname': 'Test', 'logins': 2}
#         ],
#         expected=[
#             {'fname': 'Jane', 'lname': 'Doe', 'logins': 3},
#             {'fname': 'Bob', 'lname': 'Test', 'logins': 2},
#             {'fname': 'John', 'lname': 'Doe', 'logins': 1}
#         ],
#         order_by='logins'
#     )
# ])
# def test_sort_descending(test):
#     results = select(
#     ).from_(
#         test['input']
#     ).all(order_by=test['order_by'], desc=True)
#     assert results == test['expected']
