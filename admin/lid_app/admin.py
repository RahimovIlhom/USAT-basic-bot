from django.contrib import admin
from .models import Lid, PostImage


class LidAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'phone', 'school', 'class_num', 'pinfl', 'created_time', ]


admin.site.register(Lid, LidAdmin)
admin.site.register(PostImage)
