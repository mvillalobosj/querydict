from querydict import select

if __name__ == '__main__':
    a = [
        {'fname': 'Mike', 'lname': 'Villalobos', 'logins': 1},
        {'fname': 'Henry', 'lname': 'Jordan', 'logins': 3},
        {'fname': 'John', 'lname': 'Berke', 'logins': 2}
    ]

    results = select(
        'fname as user.fname',
        'lname as user.lname',
        'logins'
    ).from_(
        a
    ).where(
        lambda x: x['logins'] >= 2,
        lambda x: x['logins'] <= 2
    ).all(order_by='logins', desc=True)

    for item in results:
        print(item)
