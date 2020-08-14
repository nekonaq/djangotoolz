from django.conf import settings


class TableSpaceRouter:
    """
    モデルの Meta.db_tablespace の値でデータベースを切り替える
    """
    def db_for_read(self, model, **hints):
        if model._meta.db_tablespace:
            return model._meta.db_tablespace
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return obj1._meta.db_tablespace == obj2._meta.db_tablespace

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        ALLOW_MIGRATE[db] の値が:

        - list か tuple であれば、
          要素と同じ名前のモデルは migrate 対象にする。

        - list か tuple のいずれでもなければ、
          True である場合に migrate 対象にする

        ALLOW_MIGRATE[db] のデフォルトは True。つまり未定義なら migrate 対象になる。
        """
        allow = getattr(settings, 'DATABASE_ALLOW_MIGRATE', {}).get(db, True)
        if isinstance(allow, (list, tuple)):
            return model_name in allow
        return bool(allow)
