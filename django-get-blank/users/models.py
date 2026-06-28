from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not login:
            raise ValueError('Логин обязателен')
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(login, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = [
        (0, 'Не указан'),
        (1, 'Мужской'),
        (2, 'Женский'),
    ]

    login = models.CharField('Логин', max_length=150, unique=True)
    email = models.EmailField('Email', unique=True)
    name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150, blank=True)
    mail_verified = models.BooleanField('Email подтвержден', default=False)
    gender = models.IntegerField('Пол', choices=GENDER_CHOICES, default=0)
    b_day = models.IntegerField('День рождения', null=True, blank=True)
    b_month = models.IntegerField('Месяц рождения', null=True, blank=True)
    b_year = models.IntegerField('Год рождения', null=True, blank=True)
    balance = models.DecimalField('Баланс', max_digits=10, decimal_places=2, default=0)
    tariff = models.DecimalField('Тариф', max_digits=10, decimal_places=2, default=5)
    date_joined = models.DateTimeField('Дата регистрации', auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.login
