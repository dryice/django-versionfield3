from builtins import str

from django import forms
from django.forms.widgets import TextInput
from django.core.exceptions import ValidationError

from .version import Version
from .constants import DEFAULT_NUMBER_BITS
from .utils import convert_version_int_to_string


class VersionField(forms.IntegerField):
    widget = TextInput

    def __init__(self, number_bits=DEFAULT_NUMBER_BITS, **kwargs):
        self.number_bits = number_bits
        return super(VersionField, self).__init__(**kwargs)

    def to_python(self, value):
        """
        Verifies that value can be converted to a Version object
        """
        if not value:
            return None

        if isinstance(value, str):
            try:
                return int(Version(value, self.number_bits))
            except ValueError:
                max_value = '.'.join([str(2 ** e - 1) for e in self.number_bits])
                raise ValidationError("Max version is {0}".format(max_value))

        return Version(convert_version_int_to_string(value, self.number_bits), self.number_bits)

    def widget_attrs(self, widget):
        attrs = super(VersionField, self).widget_attrs(widget)
        attrs['pattern'] = '^' + (r'(\d+\.)?' * (len(self.number_bits) - 1)) + r'(\*|\d+)$'
        return attrs
