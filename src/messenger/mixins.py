from django.db import models


class TimestampMixin(models.Model):
    """
    Mixin classes for time stamp
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
