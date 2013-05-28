import re
import functools

try:
    from urllib.parse import quote
except ImportError:
    # Python 2
    from urllib import quote


__all__ = ['expand']


def expand(template, variables=None):
    """
    Expand a URL template
    """
    if variables is None:
        variables = {}
    regexp = re.compile("{([^\}]+)}")
    return regexp.sub(functools.partial(_replace, variables), template)



# Modifiers

identity = lambda x: x

def truncate(string, num_chars):
    return string[:num_chars]


def _split_basic(string):
    """
    Split a string into a list of tuples of the form
    (key, modifier) where modifier is a function that applies the
    appropriate modification to the variable.
    """
    pairs = []
    for word in string.split(','):
        parts = word.split(':', 2)
        key, modifier = parts[0], identity

        if len(parts) > 1:
            # Look up the appropriate modifier function
            modifier_char = parts[1]
            if modifier_char.isdigit():
                modifier = functools.partial(truncate, num_chars=int(modifier_char))

        if word[len(word) - 1] == '*':
            key = word[:len(word) - 1]

        pairs.append((key, modifier))
    return pairs


def _split_operator(string):
    return _split_basic(string[1:])


def _replace(variables, match):
    expression = match.group(1)

    # Escaping functions (don't need to be in method body)
    escape_all = functools.partial(quote, safe="/")
    escape_reserved = functools.partial(quote, safe="/!")

    # Format functions
    def format_default(escape, key, value):
        if isinstance(value, (list, tuple)):
            return ",".join(map(escape, value))
        return escape(value)

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
        '+': ('', ',', _split_operator, escape_reserved, format_default),
        '#': ('#', ',', _split_operator, escape_reserved, format_default),
        '.': ('.', '.', _split_operator, escape_all, format_default),
        '/': ('/', '/', _split_operator, escape_all, format_default),
        ';': (';', ';', _split_operator, escape_all, format_pair),
        '?': ('?', '&', _split_operator, escape_all, format_pair_equals),
        '&': ('&', '&', _split_operator, escape_all, format_pair_equals),
    }
    default = ('', ',', _split_basic, escape_all, format_default)
    prefix, separator, split, escape, format = operators.get(
        expression[0], default)

    replacements = []
    for key, modifier in split(expression):
        if key in variables:
            variable = modifier(variables[key])
            replacement = format(escape, key, variable)
            replacements.append(replacement)
    return prefix + separator.join(replacements)
