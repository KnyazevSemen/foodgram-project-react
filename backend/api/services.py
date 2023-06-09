from django.http import HttpResponse
from django.db.models import Sum
from django.conf import settings

from recipes.models import Ingredient


def download_shopping_list(user):
    ingredients = (
        Ingredient.objects
        .filter(recipe__recipe__in_carts__user=user)
        .values(
            'name',
            'measurement_unit'
        )
        .annotate(total_amount=Sum('recipe__amount'))
        .values_list(
            'name',
            'total_amount',
            'measurement_unit'
        )
    )
    file_list = []
    [file_list.append(
        '{} - {} {}.'.format(*ingredient))
        for ingredient in ingredients]

    file = HttpResponse(
        'Cписок покупок:\n' + '\n'.join(file_list),
        content_type='text/plain'
    )
    file['Content-Disposition'] = (
        f'attachment; filename={settings.FILE_NAME}'
    )

    return file
