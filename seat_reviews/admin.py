from django.contrib import admin
from .models import Review, Comment
# from django.forms import TextInput, Textarea
# from django.db import models

admin.site.register(Review)
admin.site.register(Comment)
# def images(obj):
#     return obj.image_previews
#
#
# def href_url(obj):
#     return obj.href_url
#
#
# @admin.register(AdminPost)
# class PostAdmin(admin.ModelAdmin):
#     formfield_overrides = {
#         models.CharField: {'widget': TextInput(attrs={'size': '1'})},
#         models.TextField: {'widget': Textarea(attrs={'rows': 2, 'cols': 40})},
#     }
#     list_display = ['concert_hall', 'image_previews', 'href_url',
#                     'text', 'floor', 'area', 'seat_row', 'seat_num', 'date']
#     list_editable = ['floor', 'area', 'seat_row', 'seat_num']