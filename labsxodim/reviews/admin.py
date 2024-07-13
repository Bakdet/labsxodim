from django.contrib import admin

# Register your models here.
from .models import Item
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Item, ItemAdmin)