from django.contrib import admin
from .models import User, Followers
from django.contrib.auth.admin import UserAdmin
my_models = [User, Followers]
admin.site.register(my_models)

# class MyUserAdmin(UserAdmin):
#     list_display = ('email', 'name', 'role')
#     search_fields = ('email', 'name')
#     readonly_fields = ('last_login', 'created_at')
#
#     filter_horizontal = ()
#     list_filter = ()
#     fieldsets = ()
#
# admin.site.register(User,MyUserAdmin)

