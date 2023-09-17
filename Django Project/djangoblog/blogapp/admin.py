from django.contrib import admin
from .models import author,category,article


class authorModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__","details"]
    class Meta:
        Model=author
admin.site.register(author, authorModel)

class categoryModel(admin.ModelAdmin):
    list_display = ["__str__"]
    search_fields = ["__str__"]
    list_per_page = 10
    class Meta:
        Model=category
admin.site.register(category,categoryModel)
class articleModel(admin.ModelAdmin):
    list_display = ["__str__","posted_on"]
    search_fields = ["__str__","details"]
    list_per_page = 10
    list_filter = ["posted_on","category"]
    class Meta:
        Model=article
admin.site.register(article,articleModel)
# Register your models here.
