from django.contrib import admin

from .models import Article,Profile,Relation
# Register your models here.
admin.site.register(Article)
admin.site.register(Profile)
admin.site.register(Relation)

