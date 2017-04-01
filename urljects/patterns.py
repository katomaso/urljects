import re
import warnings

beginning = r'^'
end = r'$'
html = r'\.html$'
json = r'\.json$'

slug = r'(?P<slug>[\w-]+)'
pk = r'(?P<pk>\d+)'
uuid4 = r'(?P<uuid4>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})'  # noqa
rest = r'(?P<rest>[\w\-\_\.\@\:/]*)'  # match anything acceptable in URL

year = r'(?P<year>\d{4})'
month = r'(?P<month>0?([1-9])|10|11|12)'
day = r'(?P<day>(0|1|2)?([1-9])|[1-3]0|31)'

SEPARATOR = '/'  # separator for parts of the url

RE_TYPE = re._pattern_type   # pylint:disable=protected-access


class URLPattern(object):
    """The main urljects object able to join strings and regular expressions.

    The value of this object will always be regular expression usable in django
    url.
    """
    name_re = re.compile(r'P<([\w_-]+)>')

    def __init__(self, value=None, separator=SEPARATOR, ends=True):
        """
        :param value: Initial value of the URL
        :param separator: used to separate parts of the url, usually /
        :param ends: open urls should be used only for included urls
        """
        self.parts = [value.strip(separator)] if value else []
        self.separator = separator
        self.ends = ends
        if value:
            warnings.warn(DeprecationWarning(
                "'value' in URLPattern constructor will be removed"))
            self.add_part(value)

    def add_part(self, part):
        """Append new pattern to the URL.

        :param part: string or compiled pattern
        """
        if isinstance(part, RE_TYPE):
            part = part.pattern

        # stripping separator enables translated urls with hint what
        # string is actual url and which is a normal word
        # url(U / _('/my-profile'), private.Home, name="admin-home"),
        self.parts.append(part.strip(self.separator))
        return self

    def get_value(self, ends_override=None):
        """Finish the url pattern by adding starting and optionally ending.

        :param ends_override: overrides ``self.ends``
        :return: raw string
        """
        value = self.separator.join(filter(None, self.parts))
        ends = ends_override if ends_override is not None else self.ends

        if not value:  # use case: wild card imports
            if ends:
                return r'^$'
            return r'^'

        if value[0] != beginning:
            value = beginning + value

        if ends and value[-1] != end:
            value += end

        # included views usually ends with separator
        if not ends and value[-1] != self.separator:
            value += self.separator

        return value

    def __div__(self, other):
        """PY2 division."""
        return self.add_part(other)

    def __truediv__(self, other):
        """PY3 division."""
        return self.add_part(other)

    def __mod__(self, other):
        """Use % operator ro rename last pattern."""
        last_pattern = self.parts.pop()
        return self.add_part(self.name_re.sub('P<' + other + '>', last_pattern))

    def __repr__(self):
        return self.get_value() or ''


class URLFactory(object):
    """Create new URLPattern on every beginning of a new URL."""

    def __div__(self, other):
        return URLPattern().add_part(other)
    __truediv__ = __div__

    def get_value(self, ends_override=None):
        """Dispatch the call to URLPattern instance."""
        return URLPattern().add_part('').get_value(ends_override)
    __repr__ = get_value
    __str__ = get_value


U = URLFactory()
