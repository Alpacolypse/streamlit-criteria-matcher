import operator

OPERATORS = {
    "==": operator.eq,
    ">": operator.gt,
    "<": operator.lt,
    ">=": operator.ge,
    "<=": operator.le,
    "!=": operator.ne,
}


def get_op(operator_str: str):
    return OPERATORS.get(operator_str)
