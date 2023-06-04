from django.contrib.auth import get_user_model
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from djoser.views import UserViewSet as DjoserUserViewSet
from django.conf import settings

from recipes.models import (
    Cart,
    Favorite,
    Ingredient,
    Recipe,
    Tag
)
from users.models import Subscription
from api.permissions import (
    BlockedPermission,
    AdminOrReadOnly,
    AuthorAdminOrReadOnly
)
from api.filters import RecipeFilter
from api.paginators import CustomPaginator
from api.mixins import AddedDeleteViewMixin
from api.serializers import (
    IngredientSerializer,
    RecipeSerializer,
    TagSerializer,
    ShortRecipeSerializer,
    SubscribeSerializer
)
from api.services import download_shopping_list

User = get_user_model()


class UserViewSet(DjoserUserViewSet, AddedDeleteViewMixin):
    """Для пользователей."""

    additional_serializer = SubscribeSerializer
    pagination_class = CustomPaginator
    permission_classes = (AllowAny,)

    @action(
        methods=settings.ACTION_METHODS,
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        return self._add_del_obj(id, Subscription, Q(author__id=id))

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        pages = self.paginate_queryset(
            User.objects.filter(subscribers__user=self.request.user)
        )
        serializer = SubscribeSerializer(pages, many=True)
        return self.get_paginated_response(serializer.data)


class TagViewSet(ReadOnlyModelViewSet):
    """Для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (BlockedPermission, AdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    """Для ингридиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (BlockedPermission, AdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    pagination_class = None
    search_fields = ('^name', )


class RecipeViewSet(ModelViewSet, AddedDeleteViewMixin):
    """Для рецептов."""

    queryset = Recipe.objects.select_related('author')
    additional_serializer = ShortRecipeSerializer
    serializer_class = RecipeSerializer
    permission_classes = (BlockedPermission, AuthorAdminOrReadOnly,)
    pagination_class = CustomPaginator
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter

    @action(
        methods=settings.ACTION_METHODS,
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        return self._add_del_obj(pk, Favorite, Q(recipe__id=pk))

    @action(
        methods=settings.ACTION_METHODS,
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        return self._add_del_obj(pk, Cart, Q(recipe__id=pk))

    @action(
        methods=('get',),
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request):
        return download_shopping_list(request.user)
