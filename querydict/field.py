class Field():
    def __init__(self, field_def):
        self.source, self.alias = self.parse_field_def(field_def)

    def parse_field_def(self, field):
        if field == '*':
            return '*', '*'
        if type(field) == str:
            field = field.split(' as ')

        if type(field) in [list, tuple]:
            if len(field) == 1:
                return field[0], field[0]
            elif len(field) == 2:
                return field[0], field[1]
        else:
            return str(field), str(field)

        raise TypeError("Invalid Field Definition")
