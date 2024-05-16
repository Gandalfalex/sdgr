from django.contrib import admin
from .models import MLModel


# Register your models here.
class MlModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'pyName', 'created_at')


# Register your models here.
admin.site.register(MLModel, MlModelAdmin)


