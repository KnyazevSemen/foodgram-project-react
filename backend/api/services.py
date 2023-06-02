from django.http import HttpResponse
from django.db.models import Sum

from recipes.models import AmountIngredient
from foodgram.settings import FILE_NAME


def service_download_shopping_cart(request, **kwargs):
    ingredients = (
        AmountIngredient.objects
        .filter(recipe__in_carts__user=request.user)
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
    file['Content-Disposition'] = (f'attachment; filename={FILE_NAME}')

    return file
