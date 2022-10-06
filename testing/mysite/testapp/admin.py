from django.contrib import admin

# Register your models here.
from .models import Object, VariantFactory, Variant


class ObjectAdmin(admin.ModelAdmin):

    list_display = ("__str__",)


class VariantFactoryAdmin(admin.ModelAdmin):

    list_display = ("__str__",)


class VariantAdmin(admin.ModelAdmin):

    list_display = ("__str__",)


admin.site.register(Object, ObjectAdmin)
admin.site.register(VariantFactory, VariantFactoryAdmin)
admin.site.register(Variant, VariantAdmin)
