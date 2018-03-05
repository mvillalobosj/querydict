import itertools

from .field import Field


class QueryDict():
    def __init__(self):
        self.iterable = ()
        self.select_fields = []
        self.where_list = []

    def from_(self, source):
        if type(source) == list:
            self.iterable = itertools.chain(source)
        else:
            self.iterable = source
        return self

    def select(self, *fields):
        self.select_fields.extend([Field(field) for field in fields])
        return self

    def where(self, *lambdas):
        self.where_list.extend(lambdas)
        return self

    def all(self, order_by=None, desc=False):
        items = list(self)
        if order_by:
            items = sorted(
                items,
                key=lambda x: self._get_value(x, order_by),
                reverse=desc)
        return items

    def _keep(self, item):
        return all(clause(item) for clause in self.where_list)

    def _transform(self, item):
        if self.select_fields:
            new_item = {}
            for field in self.select_fields:
                if field.source == '*':
                    self.select_fields.extend(
                        [Field(key) for key in item.keys()]
                    )
                    continue
                try:
                    value = self._get_value(item, field.source)
                except:
                    value = self._eval(field, item, new_item)
                self._add_key(new_item, field.alias, value)
            item = new_item
        return item

    def _eval(self, field, item, new_item):
        for key, value in item.items():
            locals()[key] = value
        for key, value in new_item.items():
            locals()[key] = value

        try:
            return eval(field.source)
        except:
            return field.source

    def _add_key(self, item, key, value):
        key_list = key.split(".")
        if key_list[0] not in item:
            item[key_list[0]] = {}

        sub_dict = item
        for subkey in key_list[0:-1]:
            if subkey not in sub_dict:
                sub_dict[subkey] = {}
            sub_dict = sub_dict[subkey]

        sub_dict[key_list[-1]] = value

    def _get_value(self, item, key):
        key_list = key.split(".")
        value = item[key_list[0]]
        for subkey in key_list[1:]:
            value = value[subkey]
        return value

    def next(self):
        while(True):
            item = self._transform(self.iterable.__next__())

            if self._keep(item):
                return item

    def __next__(self):
        return self.next()

    def __iter__(self):
        return self
