from django.contrib import admin

from .models import AIConversation, AIMessage


class AIMessageInline(admin.TabularInline):
    model = AIMessage
    extra = 0
    readonly_fields = ("role", "content", "referenced_products", "disclaimer_shown", "groq_model", "tokens_used")
    can_delete = False


@admin.register(AIConversation)
class AIConversationAdmin(admin.ModelAdmin):
    list_display = ("assistant_type", "user", "title", "created_at")
    list_filter = ("assistant_type",)
    search_fields = ("user__email", "title")
    inlines = [AIMessageInline]
