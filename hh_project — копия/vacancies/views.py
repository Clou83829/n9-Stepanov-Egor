from django.shortcuts import render, get_object_or_404
from .hh_api import HHAPIClient
from .models import Vacancy

def home(request):
    """Главная страница с формой поиска"""
    message = None
    
    if request.method == "POST":
        search_query = request.POST.get("search_query", "Python")
        client = HHAPIClient()
        saved_count = client.save_vacancies_to_db(search_query)
        message = f"Загружено {saved_count} вакансий по запросу \"{search_query}\""
    
    # Показываем последние 20 вакансий
    vacancies = Vacancy.objects.all().order_by("-id")[:20]
    return render(request, "home.html", {
        "vacancies": vacancies,
        "message": message
    })

def vacancy_detail(request, pk):
    """Страница одной вакансии"""
    vacancy = get_object_or_404(Vacancy, pk=pk)
    return render(request, "vacancy_detail.html", {"vacancy": vacancy})
