from django.contrib import admin

from teasers.models import Category, Price, Teaser

admin.site.register(Price)
admin.site.register(Category)
admin.site.register(Teaser)
