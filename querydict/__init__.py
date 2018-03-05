from .querydict import QueryDict


def select(*keys):
    qd = QueryDict()
    return qd.select(*keys)
