from django.contrib import admin

# Register your models here.
from .models import Object


class ObjectAdmin(admin.ModelAdmin):

    list_display = ("__str__",)


admin.site.register(Object, ObjectAdmin)
