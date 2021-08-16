from django.db.models import IntegerChoices
from django.utils.translation import gettext_lazy as _


class STATUS(IntegerChoices):
    VIEWED = 1, _("viewed")
    NOT_VIEWED = 2, _("not viewed")
