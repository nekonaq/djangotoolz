from django.core import checks
from django.db import models
# 参考: https://gist.github.com/gipi/2401143


class CustomTypeFieldMixin(object):
    empty_strings_allowed = True

    def __init__(self, *args, **kwargs):
        self.content_type = kwargs.pop('content_type', None) or getattr(self, 'content_type', None)
        # NOTE: CharField はデフォルトで blank=False, null=False
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *self._check_content_type(**kwargs),
            *super().check(**kwargs),
        ]

    def _check_content_type(self):
        if not self.content_type:
            return [
                checks.Error(
                    "{} must define a 'content_type' attribute.".format(self.__class__),
                    obj=self,
                    id='fields.E401',
                ),
            ]
        return []

    def contribute_to_class(self, klass, name):
        super().contribute_to_class(klass, name)
        setattr(klass, self.name, self)

    def _get_flatchoices(self):
        flat = []
        for choice, value in self.choices:
            if isinstance(value, (list, tuple)):
                flat.extend(self._get_flatchoices(value))
            else:
                flat.append((choice, value))
                if not isinstance(choice, str):
                    flat.append((str(choice), value))
        return flat
    flatchoices = property(_get_flatchoices)

    def __get__(self, instance, owner=None):
        if instance is None:
            return self

        try:
            return instance.__dict__[self.name]
        except KeyError:
            raise AttributeError(
                "'{instance.__module__}.{instance.__class__.__name__}'"
                " object has no attribute '{self.name}'".format(
                    instance=instance, self=self)
            )

    def __set__(self, instance, value):
        # NOTE: 値 None と空文字は同等に扱い、instance には空文字列を格納、
        # データベースの対応カラムは varchar not null で空文字列として格納する。

        # NOTE: self.content_type が netaddr.IPAddress() の場合、引数 value が netaddr.IPAddress()
        # でもうまく動いてくれる。

        # NOTE: ここでの値変換には to_python() を使わない。
        # to_python() が content_type ではなく int に変換してくれるという点が重要。
        instance.__dict__[self.name] = (
            None if value is None or value == ''
            else self.content_type(value)
        )


class CustomTypeCharField(CustomTypeFieldMixin, models.CharField):
    pass


class CustomTypeIntegerField(CustomTypeFieldMixin, models.IntegerField):
    content_type = int
