from django.contrib import admin
from .models import Realization, Appointment, Comment
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
import io


class ExportPDFMixin:
    def export_to_pdf(self, request, queryset):
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)

        # Pobierz dane z widoku Django i umieść je w pliku PDF
        if self.model == Realization:
            data = render_to_string('mainapp/realization_pdf_template.html', {'data': queryset})
        elif self.model == Appointment:
            data = render_to_string('mainapp/appointment_pdf_template.html', {'data': queryset})
        elif self.model == Comment:
            data = render_to_string('mainapp/comment_pdf_template.html', {'data': queryset})

        p.drawString(100, 100, data)

        p.showPage()
        p.save()

        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="database_report.pdf"'
        return response

    export_to_pdf.short_description = "Export to PDF"


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


class RealizationAdmin(admin.ModelAdmin, ExportPDFMixin):
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
    actions = ['export_to_pdf']


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


admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Realization, RealizationAdmin)
