from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class MealEntry(models.Model):
    class MealType(models.TextChoices):
        BREAKFAST = 'breakfast', 'Завтрак'
        LUNCH = 'lunch', 'Обед'
        DINNER = 'dinner', 'Ужин'
        SNACK = 'snack', 'Перекус'
        IMPULSIVE = 'impulsive', 'Импульсивный'

    class Portion(models.TextChoices):
        SMALL = 'small', 'Маленькая'
        MODERATE = 'moderate', 'Умеренная'
        LARGE = 'large', 'Большая'

    class Rating(models.TextChoices):
        GOOD = 'good', 'Хорошо'
        NORMAL = 'normal', 'Нормально'
        BAD = 'bad', 'Плохо'

    class HungerLevel(models.TextChoices):
        SLIGHTLY = 'slightly', 'Слегка голоден'
        HUNGRY = 'hungry', 'Голоден'
        VERY = 'very', 'Очень голоден'

    # Причины — храним как JSON список до 2 значений
    class Reason(models.TextChoices):
        BOREDOM = 'boredom', 'Скука / отвлечься'
        STRESS = 'stress', 'Стресс / тревога'
        FATIGUE = 'fatigue', 'Усталость'
        SOCIAL = 'social', 'За компанию'
        CRAVING = 'craving', 'Вкусно / захотелось'
        HABIT = 'habit', 'Привычка / по расписанию'
        HUNGER = 'hunger', 'Физический голод'

    class JunkItem(models.TextChoices):
        SWEET = 'sweet', 'Сладкое'
        BAKERY = 'bakery', 'Выпечка'
        FASTFOOD = 'fastfood', 'Фастфуд'
        SNACKS = 'snacks', 'Чипсы / снеки'
        SODA_ALCO = 'soda_alco', 'Газировка / алкоголь'

    class PositiveItem(models.TextChoices):
        VEGGIES = 'veggies', 'Овощи / зелень'
        PROTEIN = 'protein', 'Много белка'
        FIBER = 'fiber', 'Клетчатка'
        WATER = 'water', 'Вода'
        NO_OVEREAT = 'no_overeat', 'Без переедания'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_entries')
    eaten_at = models.DateTimeField(verbose_name='Время приёма')
    meal_type = models.CharField(max_length=20, choices=MealType.choices)
    is_planned = models.BooleanField(default=True, verbose_name='Плановый')
    reasons = models.JSONField(default=list, blank=True, help_text='До 2 значений из Reason')
    hunger_level = models.CharField(max_length=20, choices=HungerLevel.choices, null=True, blank=True)
    portion = models.CharField(max_length=20, choices=Portion.choices)
    junk_items = models.JSONField(default=list, blank=True)
    positive_items = models.JSONField(default=list, blank=True)
    rating = models.CharField(max_length=20, choices=Rating.choices)
    note = models.TextField(blank=True, max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-eaten_at']
        indexes = [models.Index(fields=['user', 'eaten_at'])]

    def __str__(self):
        return f"{self.user} — {self.meal_type} @ {self.eaten_at:%d.%m %H:%M} [{self.rating}]"
