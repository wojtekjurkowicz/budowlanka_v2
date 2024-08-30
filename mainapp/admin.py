from django.contrib import admin
from .models import Realization, RealizationImage
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

        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="database_report.pdf"'
        return response

    export_to_pdf.short_description = "Export to PDF"


class RealizationImageInline(admin.TabularInline):
    model = RealizationImage
    extra = 1


# Admin class for Realization model with PDF export functionality
class RealizationAdmin(admin.ModelAdmin, ExportPDFMixin):
    list_display = ('title', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'content')
    ordering = ('-date',)
    inlines = [RealizationImageInline]

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


# Register the models with their respective admin classes
admin.site.register(Realization, RealizationAdmin)
