from django.contrib import admin

from .models import Blogpost, Querysearch, Commentsblog

admin.site.register(Blogpost)
admin.site.register(Querysearch)
admin.site.register(Commentsblog)