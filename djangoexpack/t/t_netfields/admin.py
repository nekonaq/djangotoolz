from django.contrib import admin
from .models import Ax, Mx, Nx, Rx, Tx


@admin.register(Ax)
class AxAdmin(admin.ModelAdmin):
    pass


@admin.register(Nx)
class NxAdmin(admin.ModelAdmin):
    pass


@admin.register(Mx)
class MxAdmin(admin.ModelAdmin):
    pass


@admin.register(Rx)
class RxAdmin(admin.ModelAdmin):
    pass


@admin.register(Tx)
class TxAdmin(admin.ModelAdmin):
    pass
