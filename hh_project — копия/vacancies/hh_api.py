import requests
import time
from django.utils.text import slugify

class HHAPIClient:
    """Клиент для работы с API HeadHunter"""
    
    BASE_URL = 'https://api.hh.ru'
    
    def search_vacancies(self, text="Python", area=1, per_page=20):
        """
        Ищет вакансии по заданным параметрам
        text: поисковый запрос (Python, Java, etc.)
        area: регион (1 - Москва, 2 - СПб)
        per_page: количество результатов
        """
        params = {
            'text': text,
            'area': area,
            'per_page': per_page,
            'only_with_salary': True
        }
        
        try:
            response = requests.get(f'{self.BASE_URL}/vacancies', params=params)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.RequestException as e:
            print(f"Ошибка API: {e}")
            return []
    
    def get_vacancy_details(self, vacancy_id):
        """Получает детальную информацию о вакансии по ID"""
        try:
            response = requests.get(f'{self.BASE_URL}/vacancies/{vacancy_id}')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Ошибка получения деталей: {e}")
            return None
    
    def save_vacancies_to_db(self, search_text="Python"):
        """
        Основной метод: получает вакансии из API и сохраняет в БД
        """
        from .models import Vacancy
        
        vacancies = self.search_vacancies(search_text)
        saved_count = 0
        
        for vac in vacancies:
            # Проверяем, нет ли уже такой вакансии
            if Vacancy.objects.filter(hh_id=vac['id']).exists():
                continue
            
            # Получаем детали
            details = self.get_vacancy_details(vac['id'])
            if not details:
                continue
            
            # Определяем категорию
            category = self._determine_category(details)
            
            # Создаем запись в БД
            vacancy = Vacancy(
                title=vac.get('name', ''),
                company_name=vac.get('employer', {}).get('name', ''),
                city=vac.get('area', {}).get('name', ''),
                description=details.get('description', ''),
                salary_from=vac.get('salary', {}).get('from'),
                salary_to=vac.get('salary', {}).get('to'),
                profession_category=category,
                hh_id=vac['id'],
                url=vac.get('alternate_url', '')
            )
            
            vacancy.save()
            saved_count += 1
            
            # Пауза, чтобы не нагружать API
            time.sleep(0.1)
        
        return saved_count
    
    def _determine_category(self, vacancy_details):
        """Определяет категорию вакансии"""
        specializations = vacancy_details.get('specializations', [])
        
        if not specializations:
            return 'OTHER'
        
        # Берем первую специализацию
        spec_name = specializations[0].get('name', '').lower()
        
        # Простой маппинг категорий
        if any(word in spec_name for word in ['программист', 'разработчик', 'it', 'айти']):
            return 'IT'
        elif any(word in spec_name for word in ['финанс', 'бухгалтер', 'экономист']):
            return 'FINANCE'
        elif any(word in spec_name for word in ['продаж', 'менеджер по продажам']):
            return 'SALES'
        elif any(word in spec_name for word in ['маркетинг', 'реклам', 'smm']):
            return 'MARKETING'
        elif any(word in spec_name for word in ['руководитель', 'директор', 'управлен']):
            return 'MANAGEMENT'
        
        return 'OTHER'
