from django.contrib import admin


class SimpleTabularInline(admin.TabularInline):
    template = 'admin/edit_inline/simple.html'

    # インラインのヘッダから changelist へのリンク
    show_changelist_linkto = None

    # インライン追加・編集・削除しない
    extra = 0
    can_delete = False

    def has_change_permission(self, request, obj=None):
        return False

    has_add_permission = has_change_permission
