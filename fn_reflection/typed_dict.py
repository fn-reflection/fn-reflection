import numba


def i4_0d_dict(**kvs):
    d = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                               value_type=numba.types.int32)
    d.update(kvs)
    return d


def i4_1d_dict(**kvs):
    d = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                               value_type=numba.types.int32[:])
    d.update(kvs)
    return d


def i8_0d_dict(**kvs):
    d = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                               value_type=numba.types.int64)
    d.update(kvs)
    return d


def i8_1d_dict(**kvs):
    d = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                               value_type=numba.types.int64[:])
    d.update(kvs)
    return d


def f4_0d_dict(**kvs):
    d = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                               value_type=numba.types.float32)
    d.update(kvs)
    return d


def f4_1d_dict(**kvs):
    d = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                               value_type=numba.types.float32[:])
    d.update(kvs)
    return d


def f8_0d_dict(**kvs):
    d = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                               value_type=numba.types.float64)
    d.update(kvs)
    return d


def f8_1d_dict(**kvs):
    d = numba.typed.Dict.empty(key_type=numba.types.unicode_type,
                               value_type=numba.types.float64[:])
    d.update(kvs)
    return d


i4_dict = i4_0d_dict
i8_dict = i8_0d_dict
f4_dict = f4_0d_dict
f8_dict = f8_0d_dict