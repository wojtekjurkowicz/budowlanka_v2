from django.contrib import admin
from .models import Realization, Appointment, Comment
from django.http import HttpResponse
from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


# Mixin class to add PDF export functionality
class ExportPDFMixin:
    def get_model(self, queryset):
        # Get the model class from the queryset
        return queryset.model

    def export_to_pdf(self, request, queryset):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        # Register font Calibri
        pdfmetrics.registerFont(TTFont('Calibri', 'mainapp/static/mainapp/calibri.ttf'))
        p.setFont('Calibri', 12)

        model = self.get_model(queryset)

        # Download date from views Django and change them to PDF
        if model == Realization:
            for obj in queryset:
                p.drawString(100, 750, f"Tytuł: {obj.title}")
                p.drawString(100, 730, f"Opis: {obj.content}")
                p.drawString(100, 710, f"Data: {obj.date.strftime('%Y-%m-%d %H:%M:%S')}")
                p.showPage()

        elif model == Appointment:
            for obj in queryset:
                p.drawString(100, 750, f"Opis projektu: {obj.description}")
                p.drawString(100, 730, f"Data: {obj.date.strftime('%Y-%m-%d %H:%M:%S')}")
                p.showPage()

        elif model == Comment:
            for obj in queryset:
                p.drawString(100, 750, f"Realizacja: {obj.realization}")
                p.drawString(100, 730, f"Autor: {obj.author}")
                p.drawString(100, 710, f"Treść: {obj.content}")
                p.drawString(100, 690, f"Data: {obj.date.strftime('%Y-%m-%d %H:%M:%S')}")
                p.showPage()

        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="database_report.pdf"'
        return response

    export_to_pdf.short_description = "Export to PDF"


# Admin class for Appointment model with PDF export functionality
class AppointmentAdmin(admin.ModelAdmin, ExportPDFMixin):
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
    actions = ['export_to_pdf']


# Admin class for Realization model with PDF export functionality
class RealizationAdmin(admin.ModelAdmin, ExportPDFMixin):
    list_display = ('title', 'content', 'date', 'image')
    list_filter = ('date',)
    search_fields = ('title', 'content')
    ordering = ('-date',)

    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ('Informacje o realizacji', {
            'fields': ('content', 'date', 'image'),
            'description': 'Pola powiązane z realizacją'
        }),
    )
    actions = ['export_to_pdf']


# Admin class for Comment model with PDF export functionality
class CommentAdmin(admin.ModelAdmin, ExportPDFMixin):
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
    actions = ['export_to_pdf']


# Register the models with their respective admin classes
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Realization, RealizationAdmin)
