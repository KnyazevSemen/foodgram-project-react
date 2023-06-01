from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    """Пользователи."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=50,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Логин',
        max_length=30,
        unique=True,
        help_text='Укажите уникальный логин',
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=30,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=30,
    )
    password = models.CharField(
        verbose_name=('Пароль'),
        max_length=128,
    )
    is_active = models.BooleanField(
        verbose_name='Активный',
        default=True,
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return f'{self.username}: {self.email}'


class Subscriptions(models.Model):
    """Подписки."""

    author = models.ForeignKey(
        verbose_name='Автор рецепта',
        related_name='subscribers',
        to=MyUser,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Подписчик',
        related_name='subscriptions',
        to=MyUser,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата создания подписки',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'user'),
                name='unique_for_subscription',
            ),
        )

    def __str__(self):
        return f'{self.user.username} -> {self.author.username}'
