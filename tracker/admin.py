from django.contrib import admin
from tracker.models import Trip, Group, Expenses, Tags, Blog, Comment

# Register your models here.
admin.site.register(Trip)
admin.site.register(Group)
admin.site.register(Expenses)
admin.site.register(Tags)
admin.site.register(Blog)
admin.site.register(Comment)

