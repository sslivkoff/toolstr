
def indent_to_str(indent):
    """convert input into an indent, whether a str or an int number of spaces

    useful for user facing functions with flexible input constraints
    """
    if indent is None:
        return ''
    elif isinstance(indent, int):
        return ' ' * indent
    elif isinstance(indent, str):
        return indent
    else:
        raise Exception('unknown indent format')

