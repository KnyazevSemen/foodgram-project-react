from django.http import HttpResponse
from django.db.models import Sum
from django.conf import settings

from recipes.models import AmountIngredient


def download_shopping_list(user):
    ingredients = (
        AmountIngredient.objects
        .filter(recipe__in_carts__user=user)
        .values('ingredients')
        .annotate(total_amount=Sum('amount'))
        .values_list('ingredients__name', 'total_amount',
                     'ingredients__measurement_unit')
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
