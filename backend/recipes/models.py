from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ingredient(models.Model):
    """Ингредиенты для рецепта."""

    name = models.CharField(
        verbose_name='Ингредиент',
        max_length=250,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=10,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('name', )
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'measurement_unit'),
                name='unique_for_ingredient'
            ),
        )

    def __str__(self) -> str:
        return self.name


class Tag(models.Model):
    """Тэги для рецептов."""

    name = models.CharField(
        verbose_name='Тэг',
        max_length=250,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет',
        max_length=7,
        unique=True,
        db_index=False,
        validators=[
            RegexValidator(
                '^#([a-fA-F0-9]{6})',
                message='Поле должно содержать HEX-код выбранного цвета.'
            )
        ]
    )
    slug = models.CharField(
        verbose_name='Слаг тэга',
        max_length=250,
        unique=True,
        db_index=False,
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name',)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    """Модель для рецептов."""

    name = models.CharField(
        verbose_name='Название',
        max_length=250,
    )
    author = models.ForeignKey(
        verbose_name='Автор рецепта',
        related_name='recipes',
        to=User,
        on_delete=models.SET_NULL,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги'
    )
    ingredients = models.ManyToManyField(
        verbose_name='Ингредиенты',
        related_name='recipes',
        to=Ingredient,
        through='recipes.AmountIngredient',
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipe_images/',
    )
    text = models.TextField(
        verbose_name='Описание',
        max_length=3000,
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=0,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date', )
        constraints = (
            models.UniqueConstraint(
                fields=('name', 'author'),
                name='unique_for_author',
            ),
        )

    def __str__(self) -> str:
        return self.name


class AmountIngredient(models.Model):
    """Количество ингридиентов в блюде."""

    recipe = models.ForeignKey(
        verbose_name='Рецепт',
        related_name='ingredient',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    ingredients = models.ForeignKey(
        verbose_name='Ингридиент',
        related_name='recipe',
        to=Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        default=0,
    )

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'
        ordering = ('recipe', )
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'ingredients', ),
                name='unique_for_amountingredient',
            ),
        )

    def __str__(self) -> str:
        return self.amount


class Favorite(models.Model):
    """Избранные рецепты."""

    recipe = models.ForeignKey(
        verbose_name='Понравившиеся рецепты',
        related_name='in_favorites',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Пользователь',
        related_name='favorites',
        to=User,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='unique_recipe_for_user_in_favorites',
            ),
        )

    def __str__(self) -> str:
        return self.user


class Cart(models.Model):
    """Корзина"""

    recipe = models.ForeignKey(
        verbose_name='Рецепты в корзине',
        related_name='in_carts',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Покупатель',
        related_name='carts',
        to=User,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='unique_recipe_for_user_in_cart',
            ),
        )

    def __str__(self) -> str:
        return self.user
