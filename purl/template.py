import re
import functools

try:
    from urllib.parse import quote
except ImportError:
    # Python 2
    from urllib import quote


def expand(template, variables=None):
    """
    Expand a URL template
    """
    if variables is None:
        variables = {}
    regexp = re.compile("{([^\}]+)}")
    return regexp.sub(functools.partial(_replace, variables), template)


def _replace(variables, match):
    expression = match.group(1)

    # Escaping functions (don't need to be in method body)
    escape_all = functools.partial(quote, safe="/")
    escape_reserved = functools.partial(quote, safe="/!")

    # Splitting functions
    split_basic = lambda x: x.split(',')
    split_operator = lambda x: x[1:].split(',')

    # Format functions
    format_default = lambda escape, k, v: escape(v)

    def format_pair(escape, key, value):
        """
        Format a key, value pair but don't include the equals sign
        when there is no value
        """
        if not value:
            return key
        return '%s=%s' % (key, escape(value))

    def format_pair_equals(escape, key, value):
        """
        Format a key, value pair including the equals sign
        when there is no value
        """
        if not value:
            value = ''
        return '%s=%s' % (key, escape(value))

    # operator -> (prefix, separator, split, escape)
    # TODO module level
    operators = {
        '+': ('', ',', split_operator, escape_reserved, format_default),
        '#': ('#', ',', split_operator, escape_reserved, format_default),
        '.': ('.', '.', split_operator, escape_all, format_default),
        '/': ('/', '/', split_operator, escape_all, format_default),
        ';': (';', ';', split_operator, escape_all, format_pair),
        '?': ('?', '&', split_operator, escape_all, format_pair_equals),
        '&': ('&', '&', split_operator, escape_all, format_pair_equals),
    }
    default = ('', ',', split_basic, escape_all, format_default)
    prefix, separator, split, escape, format = operators.get(
        expression[0], default)

    replacements = []
    for key in split(expression):
        if key in variables:
            value = format(escape, key, variables[key])
            replacements.append(value)
    return prefix + separator.join(replacements)
