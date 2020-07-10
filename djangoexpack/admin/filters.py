from django.contrib import admin


class ActiveFieldListFilter(admin.BooleanFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.lookup_all_kwarg = 'all'
        self.lookup_all_val = params.get(self.lookup_all_kwarg) or not self.lookup_val

    # デフォルトで「有効」のものだけ表示する機能への対応
    # set_default_query() と共に使う
    def choices(self, changelist):
        yield {
            'selected': self.lookup_all_val,
            'query_string': changelist.get_query_string({self.lookup_all_kwarg: '1'}, [self.lookup_kwarg]),
            'display': "すべて",
        }
        for lookup, title in (
                ('1', "有効"),
                ('0', "無効")):
            yield {
                'selected': self.lookup_val == lookup and not self.lookup_val2,
                'query_string': changelist.get_query_string({self.lookup_kwarg: lookup}, [self.lookup_all_kwarg]),
                'display': title,
            }
