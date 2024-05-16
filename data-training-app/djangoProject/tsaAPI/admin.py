from django.contrib import admin

from tsaAPI.models import TSDModel


# Register your models here.
class TSDModelsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'pyName', 'created_at')


# Register your models here.
admin.site.register(TSDModel, TSDModelsAdmin)
