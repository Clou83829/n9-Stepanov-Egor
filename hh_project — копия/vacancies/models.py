from django.db import models

class Vacancy(models.Model):
    """
    Модель для хранения вакансий из HH API
    Соответствует требованиям задания:
    1. Название вакансии
    2. Название компании
    3. Город
    4. Описание
    5. Диапазон зарплаты
    6. Категория профессии
    """
    
    # 1. Название вакансии
    title = models.CharField(max_length=255, verbose_name="Название вакансии")
    
    # 2. Название компании
    company_name = models.CharField(max_length=255, verbose_name="Компания")
    
    # 3. Город
    city = models.CharField(max_length=100, verbose_name="Город", blank=True, null=True)
    
    # 4. Описание
    description = models.TextField(verbose_name="Описание", blank=True)
    
    # 5. Диапазон зарплаты
    salary_from = models.IntegerField(verbose_name="Зарплата от", null=True, blank=True)
    salary_to = models.IntegerField(verbose_name="Зарплата до", null=True, blank=True)
    
    # 6. Категория профессии
    CATEGORY_CHOICES = [
        ('IT', 'IT и разработка'),
        ('FINANCE', 'Финансы'),
        ('SALES', 'Продажи'),
        ('MARKETING', 'Маркетинг'),
        ('MANAGEMENT', 'Управление'),
        ('OTHER', 'Другое'),
    ]
    profession_category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='OTHER',
        verbose_name="Категория"
    )
    
    # Дополнительные поля для работы с HH API
    hh_id = models.IntegerField(verbose_name="ID на HH", unique=True)
    url = models.URLField(verbose_name="Ссылка на HH")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"{self.title} ({self.company_name})"
    
    def get_salary_display(self):
        """Форматированное отображение зарплаты"""
        if self.salary_from and self.salary_to:
            return f"{self.salary_from} - {self.salary_to} руб."
        elif self.salary_from:
            return f"от {self.salary_from} руб."
        elif self.salary_to:
            return f"до {self.salary_to} руб."
        return "Не указана"
    
    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-created_at']
