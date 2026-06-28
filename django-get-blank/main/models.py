from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts')
    name = models.CharField('Название', max_length=255, default='Список 1')
    ts_created = models.DateTimeField('Дата создания', auto_now_add=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'{self.name} ({self.user.login})'


class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='products')
    link = models.URLField('Ссылка на товар', max_length=2000)
    img_url = models.URLField('URL изображения', max_length=2000, blank=True)
    color = models.CharField('Цвет', max_length=255, blank=True)
    size = models.CharField('Размер', max_length=255, blank=True)
    amount = models.IntegerField('Количество', default=1)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    shop_home_page = models.URLField('Страница магазина', max_length=2000, blank=True)
    cart_order = models.IntegerField('Порядок в корзине', default=0)
    deleted = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f'{self.link[:50]}...'


class Blank(models.Model):
    blank_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blanks')
    blank_filename_original = models.CharField('Имя файла', max_length=500)
    blank_file = models.FileField('Файл бланка', upload_to='blanks/', null=True, blank=True)
    ts_created = models.DateTimeField('Дата создания', auto_now_add=True)
    img_index = models.CharField('Индекс столбца фото', max_length=1, blank=True)
    color_index = models.CharField('Индекс столбца цвета', max_length=1, blank=True)
    size_index = models.CharField('Индекс столбца размера', max_length=1, blank=True)
    amount_index = models.CharField('Индекс столбца количества', max_length=1, blank=True)
    price_index = models.CharField('Индекс столбца цены', max_length=1, blank=True)
    link_index = models.CharField('Индекс столбца ссылки', max_length=1, blank=True)
    caption_row_index = models.IntegerField('Строка заголовка', default=0)
    target_sheet_name = models.CharField('Имя листа', max_length=255, blank=True)

    class Meta:
        verbose_name = 'Бланк'
        verbose_name_plural = 'Бланки'

    def __str__(self):
        return self.blank_filename_original
