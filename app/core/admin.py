from django.contrib import admin  # noqa

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import UserProfile, Ingredient


class UserAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ['email', 'password']}),
        ('Personal info', {'fields': ['name']}),
        ("Access", {'fields': ['last_login']})
    )
    readonly_fields = ['last_login']
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name", "password1", "password2"],
            },
        ),
    ]


class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name']


admin.site.register(UserProfile, UserAdmin)
admin.site.register(Ingredient, IngredientAdmin)
