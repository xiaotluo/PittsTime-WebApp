from django.contrib import admin

# Register your models here.
from . import models
# admin.site.register(models.User)
admin.site.register(models.Profile)
admin.site.register(models.Blog)
admin.site.register(models.Picture)
admin.site.register(models.Comment)
