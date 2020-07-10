from django.dispatch import Signal

# admin を使ったユーザーによるモデル変更操作 (追加変更削除)
admin_addition = Signal(providing_args=['request', 'user', 'instance'])
admin_change = Signal(providing_args=['request', 'user', 'instance'])
admin_deletion = Signal(providing_args=['request', 'user', 'instance'])
