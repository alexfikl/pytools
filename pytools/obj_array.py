import numpy




def is_obj_array(val):
    try:
        return isinstance(val, numpy.ndarray) and val.dtype == object
    except AttributeError:
        return False




def to_obj_array(ary):
    ls = log_shape(ary)
    result = numpy.empty(ls, dtype=object)

    from pytools import indices_in_shape
    for i in indices_in_shape(ls):
        result[i] = ary[i]

    return result




def is_field_equal(a, b):
    if is_obj_array(a):
        return is_obj_array(b) and (a.shape == b.shape) and (a == b).all()
    else:
        return not is_obj_array(b) and a == b




def make_obj_array(res_list):
    result = numpy.empty((len(res_list),), dtype=object)
    for i, v in enumerate(res_list):
        result[i] = v

    return result




def setify_field(f):
    from hedge.tools import is_obj_array
    if is_obj_array(f):
        return set(f)
    else:
        return set([f])




def hashable_field(f):
    if is_obj_array(f):
        return tuple(f)
    else:
        return f




def field_equal(a, b):
    a_is_oa = is_obj_array(a)
    assert a_is_oa == is_obj_array(b)

    if a_is_oa:
        return (a == b).all()
    else:
        return a == b




def join_fields(*args):
    res_list = []
    for arg in args:
        if isinstance(arg, list):
            res_list.extend(arg)
        elif isinstance(arg, numpy.ndarray):
            if log_shape(arg) == ():
                res_list.append(arg)
            else:
                res_list.extend(arg)
        else:
            res_list.append(arg)

    return make_obj_array(res_list)




def log_shape(array):
    """Returns the "logical shape" of the array.

    The "logical shape" is the shape that's left when the node-depending
    dimension has been eliminated."""

    try:
        if array.dtype.char == "O":
            return array.shape
        else:
            return array.shape[:-1]
    except AttributeError:
        return ()




def with_object_array_or_scalar(f, field):
    ls = log_shape(field)
    if ls != ():
        from pytools import indices_in_shape
        result = numpy.zeros(ls, dtype=object)
        for i in indices_in_shape(ls):
            result[i] = f(field[i])
        return result
    else:
        return f(field)




def cast_field(field, dtype):
    return with_object_array_or_scalar(
            lambda f: f.astype(dtype), field)





