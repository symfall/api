from django.conf import settings
from django.db.models import FileField
from django.forms import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


class ContentTypeRestrictedFileField(FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types.
            Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum
                                file size allowed for upload.
    """

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types", [])
        self.max_upload_size = kwargs.pop(
            "max_upload_size", settings.MAX_FILE_SIZE_UPLOAD
        )

        super().__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super().clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type

            # Check content types only when the list has data,
            # when its empty list allow upload file with any content_type
            if self.content_types and content_type not in self.content_types:
                raise forms.ValidationError(_("Filetype not supported."))

            if file.size() > self.max_upload_size:
                raise forms.ValidationError(
                    _(
                        f"Please keep filesize under "
                        f"{filesizeformat(self.max_upload_size)}. "
                        f"Current filesize {filesizeformat(file.size())}"
                    )
                )

        except AttributeError:
            pass

        return data
