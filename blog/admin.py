from django.contrib import admin
from . import models

class CommentInline(admin.StackedInline):
    model = models.Comment

    exclude = (
        'created',
        'updated',
    )

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    can_delete = False


class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )

    prepopulated_fields = {'slug': ('name',)}


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'updated',
    )

    list_filter = (
        'status',
        'topic',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    inlines = [
        CommentInline,
    ]

    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'post',
        'created',
        'updated',
        'approved',
    )

    list_filter = (
        'approved',
    )

    search_fields = (
        'name',
        'email',
        'post',
        'text',
    )



# Register models
admin.site.register(models.Topic, TopicAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Comment, CommentAdmin)
