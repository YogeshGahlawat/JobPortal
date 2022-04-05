from django.contrib import admin
from authentication.models import user

class user_admin(admin.ModelAdmin):
    list_display = [
        'username',
        'email',
        'joining_date'
    ]
    date_hierarchy = 'joining_date'
    empty_value_display = 'None'

admin.site.register(user, user_admin)