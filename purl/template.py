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
    (key, modifier_char) where modifier is a function that applies the
    appropriate modification to the variable.
    """
    pairs = []
    for word in string.split(','):
        parts = word.split(':', 2)
        key, modifier_char = parts[0], None

        if len(parts) > 1:
            # Look up the appropriate modifier function
            modifier_char = parts[1]

        if word[len(word) - 1] == '*':
            key = word[:len(word) - 1]
            modifier_char = '*'

        pairs.append((key, modifier_char))
    return pairs


def _split_operator(string):
    return _split_basic(string[1:])

# Utils

def flatten(container):
    list_ = []
    for pair in container:
        list_.extend(pair)
    return list_


def _replace(variables, match):
    expression = match.group(1)

    # Escaping functions (don't need to be in method body)
    escape_all = functools.partial(quote, safe="/")
    escape_reserved = functools.partial(quote, safe="/!,.;")

    # Format functions
    # TODO need a better way of handling = formatting
    def format_default(modifier_char, separator, escape, key, value):

        join_char = ","
        if modifier_char == '*':
            join_char = separator

        # Containers need special handling
        if isinstance(value, (list, tuple)):
            try:
                dict(value)
            except:
                # Scalar container
                return join_char.join(map(escape, value))
            else:
                # Tuple container
                if modifier_char == '*':
                    items = ["%s=%s" % (k, escape(v)) for (k,v) in value]
                    return join_char.join(items)
                else:
                    items = flatten(value)
                    return join_char.join(map(escape, items))

        return escape(value)

    def format_pair(modifier_char, separator, escape, key, value):
        """
        Format a key, value pair but don't include the equals sign
        when there is no value
        """
        if not value:
            return key
        return '%s=%s' % (key, escape(value))

    def format_pair_equals(modifier_char, separator, escape, key, value):
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
    for key, modifier_char in split(expression):
        # Modifier chars are pesky as they affect different things.  Some cause
        # the variable to be truncated.  Other's affect list formatting.
        if key in variables:
            variable = variables[key]
            if modifier_char and modifier_char.isdigit():
                variable = variable[:int(modifier_char)]
            replacement = format(modifier_char, separator, escape, key, variable)
            replacements.append(replacement)
    return prefix + separator.join(replacements)
