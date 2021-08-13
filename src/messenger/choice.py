from rest_framework.fields import (
    ChoiceField,
    flatten_choices_dict,
    to_choices_dict,
)


class ChoiceField(ChoiceField):  # pylint: disable=E0102
    def _get_choices(self):
        return self._choices

    def _set_choices(self, choices):
        self.grouped_choices = to_choices_dict(  # pylint: disable=W0201
            choices
        )
        self._choices = flatten_choices_dict(  # pylint: disable=W0201
            self.grouped_choices
        )

        # Map the string representation of choices to the underlying value.
        # Allows us to deal with eg. integer choices while supporting either
        # integer or string input, but still get the correct datatype out.
        self.choice_strings_to_values = {  # pylint: disable=W0201
            str(key): value for key, value in self.choices.items()
        }

    choices = property(_get_choices, _set_choices)
