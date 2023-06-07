from django.contrib import admin

from .models import Post, Comment

# About Comment
class CommentInline(admin.StackedInline):
    model = Comment
    fields = ["approved_comment", "text", "created_date"]
    extra = 3

# About Post
class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Date information:", {
            "fields":
                ["created_date",
                 "published_date"]
        }),
        ("Post information:", {
            "fields":
                ["title",
                 "text",
                 "active"]
        }),
    ]
    inlines = [CommentInline]

admin.site.register(Post, PostAdmin)

