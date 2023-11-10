import re


class Formatter(str):
    def __init__(self, to_format):
        self.string = to_format

    def format(self, /, **kwargs):
        string = self.string
        for name, value in kwargs.items():
            string = re.sub(rf'\$\({name}\)', value, string)  # noqa
        return self.__class__(string)

    def __repr__(self):
        return self.string

    def __str__(self):
        return self.string

    def __hash__(self):
        return self.string.__hash__()
