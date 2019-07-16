from django.contrib import admin

# Register your models here.
# from django.contrib.admin import ModelAdmin
# from django.db.models.base import ModelBase

from . import models


class UserAdmin(admin.ModelAdmin):
    pass


# def register(self, model_or_iterable, admin_class=None, **options):
#
#     # ...
#
#     admin_class = admin_class or ModelAdmin
#     if isinstance(model_or_iterable, ModelBase):
#         model_or_iterable = [model_or_iterable]
#     for model in model_or_iterable:
#         # ...
#         pass

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Avatar)
admin.site.register(models.PictureToPost)
admin.site.register(models.Post)
