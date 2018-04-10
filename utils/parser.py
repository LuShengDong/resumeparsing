# -*- coding: utf-8 -*-
import inspect


class Parser:
    def __init__(self):
        self.on_load()

    def on_load(self):
        pass


    def parse(self, sentence):
        mems = inspect.getmembers(self)
        for name, method in mems:
            if name[:6] == 'parse_':
                key = name.split('_')[1]
                value = method(sentence)
                if value is not None:
                    yield key, value


if __name__ == '__main__':
    p = Parser()
    print(list(p.parse('123123')))
