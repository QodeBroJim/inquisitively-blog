from django.contrib import admin

from .models import Signup, AccessTutorialSignup

@admin.register(AccessTutorialSignup)
class AccessTutorialSignupAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp', 'hobby', 'first_name', 'last_name',)
    list_filter = ('hobby', )
    ordering = ('-timestamp',)

admin.site.register(Signup)
