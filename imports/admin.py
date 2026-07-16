from django.contrib import admin
from .models import (
    FileUpload,
    FileImportLog,
    FinancialStatementImportHeader,
    NewClientImportHeader,
    CrossSaleImportHeader,
    StationTimeImportHeader,
    NewClientImportRow,
    CrossSaleImportRow,
)


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = (
        "original_filename",
        "file_type_detected",
        "file_format",
        "detected_year",
        "detected_month",
        "status",
        "uploaded_by",
        "created_at",
    )
    list_filter = (
        "file_type_detected",
        "file_format",
        "status",
        "detected_year",
        "detected_month",
    )
    search_fields = ("original_filename", "uploaded_by__username", "uploaded_by__email")
    readonly_fields = (
        "uploaded_by",
        "file_size_bytes",
        "sha256",
        "mime_type",
        "original_filename",
        "detected_year",
        "detected_month",
        "status",
        "error_summary",
        "parsing_notes",
        "created_at",
        "updated_at",
    )
    fields = (
        "stored_file",
        "uploaded_by",
        "original_filename",
        "file_type_detected",
        "file_format",
        "detected_year",
        "detected_month",
        "file_size_bytes",
        "status",
        "error_summary",
        "parsing_notes",
        "created_at",
        "updated_at",
    )

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(FileImportLog)
class FileImportLogAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "level", "step_code", "line_number", "created_at")
    list_filter = ("level", "step_code")
    search_fields = ("file_upload__original_filename", "message")


@admin.register(FinancialStatementImportHeader)
class FinancialStatementImportHeaderAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "une", "year", "month", "statement_type")
    list_filter = ("une", "year", "month", "statement_type")
    search_fields = ("file_upload__original_filename",)


@admin.register(NewClientImportHeader)
class NewClientImportHeaderAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "year", "month")
    list_filter = ("year", "month")
    search_fields = ("file_upload__original_filename",)


@admin.register(CrossSaleImportHeader)
class CrossSaleImportHeaderAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "year", "month")
    list_filter = ("year", "month")
    search_fields = ("file_upload__original_filename",)


@admin.register(StationTimeImportHeader)
class StationTimeImportHeaderAdmin(admin.ModelAdmin):
    list_display = ("file_upload", "year", "month")
    list_filter = ("year", "month")
    search_fields = ("file_upload__original_filename",)


@admin.register(NewClientImportRow)
class NewClientImportRowAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "month",
        "une",
        "client_name",
        "nit",
        "operation_code",
        "previous_contracts",
        "counts_as_new",
        "currency",
        "amount",
    )
    list_filter = (
        "year",
        "month",
        "une",
        "counts_as_new",
        "currency",
    )
    search_fields = (
        "client_name",
        "nit",
        "operation_code",
        "une__code",
        "une__name_es",
        "raw_une_value",
    )
    autocomplete_fields = ("une", "currency")
    list_select_related = ("header", "une", "currency")


@admin.register(CrossSaleImportRow)
class CrossSaleImportRowAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "month",
        "une_origin",
        "une_destination",
        "client_name",
        "operation_code",
        "date",
        "currency",
    )
    list_filter = (
        "year",
        "month",
        "une_origin",
        "une_destination",
        "currency",
    )
    search_fields = (
        "client_name",
        "operation_code",
        "raw_une_origin",
        "raw_une_destination",
        "une_origin__code",
        "une_destination__code",
    )
    autocomplete_fields = ("une_origin", "une_destination", "currency")
    list_select_related = ("header", "une_origin", "une_destination", "currency")