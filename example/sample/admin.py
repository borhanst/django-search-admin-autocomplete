from django.contrib import admin
from search_admin_autocomplete.admin import SearchAutoCompleteAdmin
from .models import DummyModel, Client, Category


class DummyModelAdmin(SearchAutoCompleteAdmin):
    search_fields = ['name', 'description']


class ClientSearchAdmin(SearchAutoCompleteAdmin):
    search_fields = ['name', 'email']


class CategorySearchAdmin(SearchAutoCompleteAdmin):
    search_fields = ['title', 'slug']


class RelatedFieldSearchAdmin(SearchAutoCompleteAdmin):
    """Example using related field lookups."""
    search_fields = ['name', 'client__name', 'category__title']


admin.site.register(DummyModel, DummyModelAdmin)
admin.site.register(Client, ClientSearchAdmin)
admin.site.register(Category, CategorySearchAdmin)
