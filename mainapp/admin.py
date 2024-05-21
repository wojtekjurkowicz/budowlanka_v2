from django.contrib import admin

from .models import Realization, Appointment, Message, Comment


class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('description', 'date')
    list_filter = ('date',)
    search_fields = ('description',)
    ordering = ('date',)
    fieldsets = (
        (None, {
            'fields': ('description',)
        }),
        ('Informacje o dacie', {
            'fields': ('date',),
            'description': 'Pola powiązane z datą wizyty'
        }),
    )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'date')
    list_filter = ('date', 'author')
    search_fields = ('content',)
    ordering = ('-date',)
    fieldsets = (
        (None, {
            'fields': ('author',)
        }),
        ('Informacje o wiadomości', {
            'fields': ('content', 'date'),
            'description': 'Pola powiązane z treścią i datą komentarza'
        }),
    )


class RealizationAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date', 'was_published_recently')
    list_filter = ('date',)
    search_fields = ('title', 'content')
    ordering = ('-date',)
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Informacje o realizacji', {
            'fields': ('content', 'date'),
            'description': 'Pola powiązane z realizacją'
        }),
    )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('realization', 'author', 'content', 'date')
    list_filter = ('date', 'author')
    search_fields = ('content',)
    ordering = ('-date',)
    fieldsets = (
        (None, {
            'fields': ('realization', 'author')
        }),
        ('Informacje o komentarzu', {
            'fields': ('content', 'date'),
            'description': 'Pole powiązane z komentarzem'
        }),
    )


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Realization, RealizationAdmin)
