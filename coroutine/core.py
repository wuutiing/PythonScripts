# encoding: utf8

'''
author: wuting
contact: quzhouwuting@163.com
create_date: 2017-06-26
'''

import functools

def coroutine(func):
    @functools.wraps(func)
    def wrapper(*args, **kws):
        generator = func(*args, **kws)
        next(generator)
        return generator
    return wrapper


class Ensurer:
    def __init__(self, validates, doc=None):
        self.validates = validates
        self.doc = doc


def ensure_preoperty(Class):
    def mk_property(prop_name, attribute):
        private_name = "__" + prop_name
        def getter(self):
            return getattr(self, private_name)

        def setter(self, value):
            if type(attribute.validates) is list:
                for validate in attribute.validates:
                    if callable(validate):
                        validate(prop_name, value)
            elif callable(attribute.validates):
                attribute.validates(prop_name, value)
            setattr(self, private_name, value)
        return property(getter, setter, doc=attribute.doc)

    for name, attr in Class.__dict__.items():
        if isinstance(attr, Ensurer):
            setattr(Class, name, mk_property(name, attr))
    return Class

def not_null(prop_name, value):
    if value is None:
        raise ValueError("{} is not allowed None".format(prop_name))

def int_only(prop_name, value):
    if not (type(value) is int or value is None):
        raise ValueError("{} is only allowed int now {}".format(prop_name, value))

def str_only(prop_name, value):
    if not (type(value) is str or value is None):
        raise ValueError("{} is only allowed str, now {}".format(prop_name, value))


