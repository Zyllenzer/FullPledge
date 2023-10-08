from django.contrib import admin
from .models import UserSite, NonFictionBook, TodoList,Role,BookUpdate, TodoUpdate, SiteVisited
# Register your models here.

admin.site.register(UserSite)
admin.site.register(NonFictionBook)
admin.site.register(TodoList)
admin.site.register(Role)
admin.site.register(BookUpdate)
admin.site.register(TodoUpdate)

class MyModelAdmin(admin.ModelAdmin):
    list_display = ("id",'date_visited', 'number_visitor')  
admin.site.register(SiteVisited, MyModelAdmin)