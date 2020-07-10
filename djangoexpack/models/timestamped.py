from django.utils.translation import gettext_lazy as _
from django.db import models
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField


class TimeStampedModelMixin(models.Model):
    class Meta:
        abstract = True

    create_time = CreationDateTimeField(verbose_name=_("Creation Time"))
    update_time = ModificationDateTimeField(verbose_name=_("Update Time"))

    def save(self, **kwargs):
        self.update_modified = kwargs.pop('update_modified', getattr(self, 'update_modified', True))
        super().save(**kwargs)
