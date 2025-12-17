from django.contrib import admin
from .models import Vacancy

@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'company_name', 'city', 'salary_from', 'salary_to')
    search_fields = ('title', 'company_name')
    list_filter = ('profession_category', 'city')