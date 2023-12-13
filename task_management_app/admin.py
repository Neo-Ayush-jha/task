from django.contrib import admin
from .models import *


class taskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "description",
        "status",
        "owner",
        "deadline",
    ]
    list_filter = ["id", "title", "owner","status"]
    search_fields = ("id", "title","owner", "status")


admin.site.register(Task, taskAdmin)
