from django.contrib import admin

from .models import Author, Category, Comment, Post, PostView

admin.site.site_header = 'Inquisitively Dashboard'
admin.site.index_title = 'Inquisitively Administration'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'categoryslug': ('title',)}
    ordering = ('title',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'timestamp', 'categories', 'status')
    list_filter = ('status', 'timestamp', 'categories', )
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author', )
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content', 'post', 'timestamp', 'user')
    ordering = ('-timestamp',)

    
admin.site.register(PostView)
admin.site.register(Author)