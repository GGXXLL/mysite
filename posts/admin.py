from django.contrib import admin

from .models import Part, Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment


class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['part', 'title', 'text']}),
    ]
    list_display = ('id', 'part', 'author', 'title', 'edit_date', 'pub_date', 'was_published_recently', 'is_delete', 'examine')
    list_filter = ['part__name', 'pub_date', 'is_delete', 'examine']
    search_fields = ['title', ]
    list_editable = ['examine', 'is_delete']

    def delete_queryset(self, request, queryset):
        for i in queryset:
            i.is_delete = True
            i.save()

    def save_model(self, request, obj, form, change):
        obj.save()


class CommentAdmin(admin.ModelAdmin):
    def delete_queryset(self, request, queryset):
        for i in queryset:
            i.is_delete = True
            i.save()


admin.site.register(Part)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
