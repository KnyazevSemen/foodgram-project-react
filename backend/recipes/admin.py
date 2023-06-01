from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from recipes.models import (
    Ingredient,
    Recipe,
    Tag,
    AmountIngredient,
    Favorites,
    Carts
)


admin.site.site_title = 'Администрирование сайта «Продуктовый помощник»'
admin.site.site_header = 'Администрирование сайта «Продуктовый помощник»'


class IngredientInline(admin.TabularInline):
    model = AmountIngredient
    extra = 0


@admin.register(AmountIngredient)
class LinksAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'measurement_unit',
    )
    search_fields = (
        'name',
    )
    list_filter = (
        'name',
    )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'author', 'get_image', 'count_favorites',
    )
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    search_fields = (
        'name', 'author__username', 'tags__name',
    )
    list_filter = (
        'name', 'author__username', 'tags__name'
    )

    inlines = (IngredientInline,)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    get_image.short_description = 'Изображение'

    def count_favorites(self, obj):
        return obj.in_favorites.count()

    count_favorites.short_description = 'В избранном'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'slug', 'color_code',
    )
    search_fields = (
        'name', 'color'
    )

    @admin.display(description='Colored')
    def color_code(self, obj):
        return format_html(
            '<span style="color: #{};">{}</span>',
            obj.color[1:], obj.color
        )


@admin.register(Favorites)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'recipe', 'date_added'
    )
    search_fields = (
        'user__username', 'recipe__name'
    )


@admin.register(Carts)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'recipe', 'date_added'
    )
    search_fields = (
        'user__username', 'recipe__name'
    )
